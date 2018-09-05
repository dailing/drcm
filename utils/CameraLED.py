try:
	from gpiozero import LED
	from gpiozero import PWMLED as pwm
except Exception as e:
	pass
#13,26

class ViewFixationLED():
	LED_GPIO_SERIAL_NUM = [5,6,13,19,26,16,20,21]
	LED_NUM = len(LED_GPIO_SERIAL_NUM)
	DUTY_CYCLE = 0.1
	@staticmethod
	def in_range(idx):
		return idx>=0 and idx < LED_NUM

	def __init__(self):
		self.LED_INSTANCE = [pwm(l) for l in LED_GPIO_SERIAL_NUM]

	def numOfLED(self):
		return ViewFixationLED.LED_NUM

	def offAll(self) :
		for l in self.LED_INSTANCE:
			l.value = 0

	def onAll(self):
		for l in self.LED_INSTANCE:
			l.value = ViewFixationLED.DUTY_CYCLE

	def off(self, idx):
		if not ViewFixationLED.in_range(idx):
			return False
		self.LED_INSTANCE[idx].value = 0.0

	def on(self, idx):
		if not ViewFixationLED.in_range(idx):
			return False
		self.LED_INSTANCE[idx].value = ViewFixationLED.DUTY_CYCLE

class Infrared_LED():
	def __init__(self, arg):
		self.infraredLed = LED(4)
		
	def on(self):
		self.infraredLed.on()

	def off(self):
		self.infraredLed.off()
class Flash_LED():
	DUTY_CYCLE = 0.01
	def __init__(self):
		pass
		self.flashLed = pwm(17)

	def on(self):
		self.flashLed.value = Flash_LED.DUTY_CYCLE

	def off(self):
		self.flashLed.value = 0.0