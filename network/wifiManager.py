from __future__ import division
import sqlite3
import logging
#https://wifi.readthedocs.io/en/latest/scanning.html
# from wifi import Scheme


#-------------------------copy from wifi package ----------------------------

import re
import textwrap
import subprocess

try:
	from subprocess import check_output
except Exception:
    # Copyright (c) 2003-2005 by Peter Astrand <astrand@lysator.liu.se>
    #
    # Licensed to PSF under a Contributor Agreement.
    # See http://www.python.org/2.4/license for licensing details.

    def check_output(*popenargs, **kwargs):
        r"""Run command with arguments and return its output as a byte string.

        If the exit code was non-zero it raises a CalledProcessError.  The
        CalledProcessError object will have the return code in the returncode
        attribute and output in the output attribute.

        The arguments are the same as for the Popen constructor.  Example:

        >>> check_output(["ls", "-l", "/dev/null"])
        'crw-rw-rw- 1 root root 1, 3 Oct 18  2007 /dev/null\n'

        The stdout argument is not allowed as it is used internally.
        To capture standard error in the result, use stderr=STDOUT.

        >>> check_output(["/bin/sh", "-c",
        ...               "ls -l non_existent_file ; exit 0"],
        ...              stderr=STDOUT)
        'ls: non_existent_file: No such file or directory\n'
        """
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

def db2dbm(quality):
	"""
	Converts the Radio (Received) Signal Strength Indicator (in db) to a dBm
	value.  Please see http://stackoverflow.com/a/15798024/1013960
	"""
	dbm = int((quality / 2) - 100)
	return min(max(dbm, -100), -50)

class Cell(object):
	"""
	Presents a Python interface to the output of iwlist.
	"""
	cells_re = re.compile(r'Cell \d+ - ')
	quality_re_dict = {'dBm': re.compile(r'Quality[=:](?P<quality>\d+/\d+).*Signal level[=:](?P<siglevel>-\d+) dBm?(.*Noise level[=:](?P<noiselevel>-\d+) dBm)?'),
					   'relative': re.compile(r'Quality[=:](?P<quality>\d+/\d+).*Signal level[=:](?P<siglevel>\d+/\d+)'),
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

	saved_wifi = None

	@staticmethod
	def _save(ssid, psw):
		Cell.saved_wifi[ssid] = psw
		with open('saved.wifi', 'w') as f:
			for k,v in Cell.saved_wifi.items():
				f.write('{}\t{}\n'.format(k,v))

	@staticmethod
	def _get_psw(ssid):
		if Cell.saved_wifi is None:
			Cell.saved_wifi = {}
			with open('saved.wifi', 'r') as f:
				for l in f.read().splitlines():
					ssid, psw = f.split('\t')
					Cell.saved_wifi[ssid] = psw
		if ssid in Cell.saved_wifi:
			return Cell.saved_wifi[ssid]
		return None

	@staticmethod
	def normalize_key(key):
		key = key.strip().lower()

		key = Cell.key_translations.get(key, key)

		return key.replace(' ', '')

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
		if Cell.saved_wifi is None:
			Cell._get_psw('load_saved_profile')



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
		cells = map(Cell.new_from_string, Cell.cells_re.split(iwlist_scan)[1:])

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
							self.signal = db2dbm(int((actual / total) * 100))
						elif re_name == 'absolute':
							self.quality = self.quality + '/100'
							self.signal = db2dbm(int(signal))
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

	def connect_(self):
		pass



#-------------------------copy from wifi package ----------------------------



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
		return [(c.quality, c.ssid, '******', c.encryption_type) for c in self.CELLS]

	def isConnected(self):
		return self.CUR_SSID != None

	def connectDefault(self):
		if self.CELLS is None:
			self.getWifiList()
		self.isConnecting = True
		cells = self.CELLS
		for c in cells:
			scheme = Scheme.find(self.interface, c.ssid)
			if scheme is not None:
				try:
					scheme.activate()
				except Exception as e:
					continue
				else :
					break
		self.isConnecting = False

	def connectWifi(ssid, pwd):
		if self.CELLS is None:
			self.getWifiList()
		for c in self.CELLS :
			if c.ssid == ssid:
				scheme = Scheme.for_cell(self.interface, ssid, c, pwd)
				scheme.activate()
				# try:
				# 	scheme = Scheme.for_cell(self.interface, ssid, c, pwd)
				# 	scheme.activate()
				# except Exception as e:
				# 	raise e
				# 	return False
				# else :
				# 	scheme.save()
				# 	return True

def main():
	man = wifiManager()
	for i in man.getWifiList():
		print(i)
	# print(wifiManager.connectWifi('ddd', '12345678'))


if __name__ == '__main__':
	main()