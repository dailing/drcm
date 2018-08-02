import logging
# https://wifi.readthedocs.io/en/latest/scanning.html
# from wifi import Scheme
import pickle

# -------------------------copy from wifi package ----------------------------

import re
import textwrap
import subprocess
from subprocess import Popen, PIPE, CalledProcessError

try:
    from subprocess import check_output
except ImportError:
    def check_output(*popenargs, **kwargs):
        if 'stdout' in kwargs:
            raise ValueError('stdout argument not allowed, it will be overridden.')
        process = Popen(stdout=PIPE, *popenargs, **kwargs)
        output, unused_err = process.communicate()
        retcode = process.poll()
        if retcode:
            cmd = kwargs.get("args")
            if cmd is None:
                cmd = popenargs[0]
            raise CalledProcessError(retcode, cmd, output=output)
        return output


class InterfaceError(Exception):
    pass


class Cell(object):
    """
    Presents a Python interface to the output of iwlist.
    """
    cells_re = re.compile(r'Cell \d+ - ')
    quality_re_dict = {'dBm': re.compile(
        r'Quality[=:](?P<quality>\d+/\d+).*Signal level[=:](?P<siglevel>-\d+) dBm?(.*Noise level[=:](?P<noiselevel>-\d+) dBm)?'),
        'relative': re.compile(
            r'Quality[=:](?P<quality>\d+/\d+).*Signal level[=:](?P<siglevel>\d+/\d+)'),
        'absolute': re.compile(r'Quality[=:](?P<quality>\d+).*Signal level[=:](?P<siglevel>\d+)')}
    frequency_re = re.compile(r'^(?P<frequency>[\d\.]+ .Hz)(?:[\s\(]+Channel\s+(?P<channel>\d+)[\s\)]+)?$')

    identity = lambda x: x

    key_translations = {
        'encryption key': 'encrypted',
        'essid': 'ssid',
    }

    normalize_value = {
        'ssid': lambda v: v.strip('"'),
        'encrypted': lambda v: v == 'on',
        'address': identity,
        'mode': identity,
        'channel': int,
    }

    _saved_wifi = None
    _wifi_file_name = 'save.wifi.bin'

    @staticmethod
    def _save(ssid, psw):
        if Cell._saved_wifi is None:
            Cell._get_psw(None)
        Cell._saved_wifi[ssid] = psw
        with open(Cell._wifi_file_name, 'w+') as f:
            pickle.dump(Cell._saved_wifi, f)

    @staticmethod
    def _get_psw(ssid):
        if Cell._saved_wifi is None:
            try:
                with open(Cell._wifi_file_name, 'r') as f:
                    Cell._saved_wifi = pickle.load(f)
            except Exception as e:
                Cell._saved_wifi = {}
                print(str(e))
        if ssid in Cell._saved_wifi:
            return Cell._saved_wifi[ssid]
        return None

    @staticmethod
    def normalize_key(key):
        key = key.strip().lower()

        key = Cell.key_translations.get(key, key)

        return key.replace(' ', '')

    @staticmethod
    def db2dbm(quality):
        """
        Converts the Radio (Received) Signal Strength Indicator (in db) to a dBm
        value.  Please see http://stackoverflow.com/a/15798024/1013960
        """
        dbm = int((quality / 2) - 100)
        return min(max(dbm, -100), -50)

    @staticmethod
    def split_on_colon(string):
        key, _, value = map(lambda s: s.strip(), string.partition(':'))

        return key, value

    def __init__(self):
        self.ssid = None
        self.bitrates = []
        self.address = None
        self.channel = None
        self.encrypted = False
        self.encryption_type = None
        self.frequency = None
        self.mode = None
        self.quality = None
        self.signal = None
        self.noise = None
        self.interface = None

    def __repr__(self):
        return 'Cell(ssid={ssid})'.format(**vars(self))

    @staticmethod
    def all(interface):
        """
        Returns a list of all cells extracted from the output of iwlist.
        """
        try:
            iwlist_scan = check_output(['/sbin/iwlist', interface, 'scan'],
                                       stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            raise InterfaceError(e.output.strip())
        else:
            iwlist_scan = iwlist_scan.decode('utf-8')
        iwlist_scan = Cell.cells_re.split(iwlist_scan)[1:]
        cells = {}
        for line in iwlist_scan:
            cell = Cell.new_from_string(line)
            cell.interface = interface
            cells[cell.ssid] = cell
        return cells

    @staticmethod
    def new_from_string(cell_string):
        cell = Cell()
        cell.from_string(cell_string)
        return cell

    def from_string(self, cell_block):
        """
        Parses the output of iwlist scan for one cell and returns a Cell
        object for it.
        """
        # The cell blocks come in with every line except the first indented at
        # least 20 spaces.  This removes the first 20 spaces off of those lines.
        lines = textwrap.dedent(' ' * 20 + cell_block).splitlines()
        cell = Cell()

        while lines:
            line = lines.pop(0)

            if line.startswith('Quality'):
                for re_name, quality_re in Cell.quality_re_dict.items():
                    match_result = quality_re.search(line)
                    if match_result is not None:
                        groups = match_result.groupdict()
                        self.quality = groups['quality']
                        signal = groups['siglevel']
                        noise = groups.get('noiselevel')
                        if re_name == 'relative':
                            actual, total = map(int, signal.split('/'))
                            self.signal = Cell.db2dbm(int((actual / total) * 100))
                        elif re_name == 'absolute':
                            self.quality = self.quality + '/100'
                            self.signal = Cell.db2dbm(int(signal))
                        else:
                            self.signal = int(signal)
                        if noise is not None:
                            self.noise = int(noise)
                        break

            elif line.startswith('Bit Rates'):
                values = Cell.split_on_colon(line)[1].split('; ')

                # consume next line of bit rates, because they are split on
                # different lines, sometimes...
                if lines:
                    while lines[0].startswith(' ' * 10):
                        values += lines.pop(0).strip().split('; ')

                self.bitrates.extend(values)
            elif ':' in line:
                key, value = Cell.split_on_colon(line)
                key = Cell.normalize_key(key)

                if key == 'ie':
                    if 'Unknown' in value:
                        continue

                    # consume remaining block
                    values = [value]
                    while lines and lines[0].startswith(' ' * 4):
                        values.append(lines.pop(0).strip())

                    if 'WPA2' in value:
                        self.encryption_type = 'wpa2'
                    elif 'WPA' in value:
                        self.encryption_type = 'wpa'
                if key == 'frequency':
                    matches = self.frequency_re.search(value)
                    self.frequency = matches.group('frequency')
                    if matches.group('channel'):
                        self.channel = int(matches.group('channel'))
                elif key in Cell.normalize_value:
                    setattr(self, key, Cell.normalize_value[key](value))

        # It seems that encryption types other than WEP need to specify their
        # existence.
        if self.encrypted and not self.encryption_type:
            self.encryption_type = 'wep'
        return self

    @property
    def saved(self):
        return Cell._get_psw(self.ssid) is not None

    @staticmethod
    def _try_cmd(cmd):
        try:
            out = check_output(["bash", "-c", cmd], stderr=subprocess.STDOUT)
            print('CMD:', cmd, ' output:', out)
        except CalledProcessError as c:
            print('ERROR CMD:', c.cmd, ' OUTPUT: ', c.output)
            return False
        return True

    def connect(self, psw=None):
        # shut down all wpa_supplicant process
        try:
            out = check_output(['/usr/bin/killall', 'wpa_supplicant'], stderr=subprocess.STDOUT)
            print('Killing wpa_supplicant processe:', out)
        except CalledProcessError as e:
            o = e.output
            # print(o,type(o), '**', o.find('no process found'))
            if e.output.find('no process found') < 0:
                # Error happened. Cannot kill process
                print(o)
                return False
        # Set link down and up again
        if not Cell._try_cmd('ip link set {} down'.format(self.interface)):
            return False
        if not Cell._try_cmd('ip link set {} up'.format(self.interface)):
            return False
        # Check if there is any saved password
        if psw is None:
            psw = Cell._get_psw(self.ssid)
            print('Got password:', psw, 'for wifi:',self.ssid)
        if self.encryption_type in ['wpa2', 'wpa']:
            cmd = "wpa_supplicant -D nl80211 -i {interface} -B -c <(wpa_passphrase '{ssid}' '{psw}')".format(
                interface=self.interface,
                ssid=self.ssid,
                psw=psw
            )
            if not Cell._try_cmd(cmd): return False
        elif self.encryption_type is None:
            cmd = 'iw dev {interface} connect "{ssid}"'.format(
                interface=self.interface,
                ssid=self.ssid,
            )
            if not Cell._try_cmd(cmd): return False
        else:
            print('ERROR: encryption_type not supported')
            return False
        # must be a successful if the code made is here
        Cell._save(ssid=self.ssid, psw=psw)
        return True


logger = logging.getLogger('root.wifiManager')


class wifiManager():
    """manage wifi connection"""

    def __init__(self, interface_name='wlan0'):
        self.CUR_SSID = None
        self.CELLS = None
        self.isConnecting = False
        self.interface = 'wlan0'

    def getWifiList(self):
        self.CELLS = Cell.all(self.interface)
        return [(c.quality, c.ssid, '******' if c.saved else "-----", c.encryption_type) for c in self.CELLS.values()]

    def isConnected(self):
        return self.CUR_SSID != None

    def getCurrentWifi(self):
        return self.CUR_SSID



    def connectWifi(self, ssid, pwd=None):
        print ('connect to wifi', ssid)
        if self.CELLS is None:
            self.getWifiList()
        if ssid in self.CELLS:
            if self.CELLS[ssid].connect(pwd):
                self.CUR_SSID = ssid
                return True
            else:
                return False
        else:
            print('Not in range')
        return False


def main():
    man = wifiManager()
    for i in man.getWifiList():
        print(i)
    # # Try a WEP2 network
    # man.connectWifi('California Nights', 'mooshmooshak')
    # man.connectWifi('California Nights')
    # # Try a not encrypted network
    # man.connectWifi('ddy7')
    # Try a wpa network
    man.connectWifi('JinJiangHotel', '4008209999')
    # Connect again Using saved password
    # man.connectWifi('ddy8')


# print(wifiManager.connectWifi('ddd', '12345678'))


if __name__ == '__main__':
    main()
