from VCNL4040 import VCNL4040
import RPi.GPIO as GPIO
import time

v4040 = VCNL4040(debug=False)

# this is called when an interrupt is detected
def int_event(pin):
	check_int()
	print(v4040.read_flags())

int_pin = 14 # BCM pin 14
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) # BCM pin-numbering scheme
GPIO.setup(int_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(int_pin, GPIO.FALLING, callback=int_event)

def check_int():
	if (GPIO.input(int_pin)):
		print("INT pin is high, no interrupt")
	else:
		print("INT pin is low, interrupt is active")

print("--> Restore default values manually")
v4040.restore_default_values()
time.sleep(1)
print("--> Print all non-default values, all sensor data is invalid as sensors are not enabled")
for bit_field in v4040.check_default_values():
	v4040.read_bf_and_print(bit_field)
print("--> Disable White LED (NOT USING IT)")
v4040.i2c_bf_write(v4040.BF_WHITE_EN, v4040.BF_WHITE_EN.TABLE_ENUM["DISABLE"])
print("--> Enable ALS")
v4040.i2c_bf_write(v4040.BF_ALS_IT, v4040.BF_ALS_IT.TABLE_ENUM["320ms"])
v4040.i2c_bf_write(v4040.BF_ALS_SD, v4040.BF_ALS_SD.TABLE_ENUM["ENABLE"])
time.sleep(1)
print("--> Print all non-default values")
for bit_field in v4040.check_default_values():
	v4040.read_bf_and_print(bit_field)
check_int()
print("Check ALS interrupts")
v4040.i2c_bf_write(v4040.BF_ALS_INT_EN, v4040.BF_ALS_INT_EN.TABLE_ENUM["ENABLE"])
time.sleep(1) # expect ALS_IF_H_INT
v4040.i2c_bf_write(v4040.BF_ALS_THDH, 0xFFFF) # set to a high value so that ALS_IF_H_INT doesn't get set anymore
v4040.i2c_bf_write(v4040.BF_ALS_THDL, 0xFFFF) # set to a high value so that we will see the ALS_IF_L_INT
time.sleep(1)  # expect ALS_IF_L_INT
v4040.i2c_bf_write(v4040.BF_ALS_THDL, 0x0000) # set to a low value so that ALS_IF_L_INT doesn't get set anymore
time.sleep(1) # expect nothing
check_int()
print("Check proximity sensor")
v4040.i2c_bf_write(v4040.BF_ALS_SD, v4040.BF_ALS_SD.TABLE_ENUM["DISABLE"])
v4040.i2c_bf_write(v4040.BF_LED_I, v4040.BF_LED_I.TABLE_ENUM["160mA"])
v4040.i2c_bf_write(v4040.BF_PS_CANC, 0x0005)
v4040.i2c_bf_write(v4040.BF_PS_THDH, 0x0001)
v4040.i2c_bf_write(v4040.BF_PS_INT, v4040.BF_PS_INT.TABLE_ENUM["TRIGGER_WHEN_CLOSE_OR_AWAY"])
#v4040.i2c_bf_write(v4040.BF_PS_SMART_PERS, v4040.BF_PS_SMART_PERS.TABLE_ENUM["ENABLE"])
v4040.i2c_bf_write(v4040.BF_PS_SD, v4040.BF_PS_SD.TABLE_ENUM["PS_POWER_ON"])
for n in range(0,100):
	v4040.read_bf_and_print(v4040.BF_PS_DATA)
	time.sleep(0.1)
v4040.i2c_bf_write(v4040.BF_PS_SD, v4040.BF_PS_SD.TABLE_ENUM["PS_SHUT_DOWN"])
print("--> Print all non-default values")
for bit_field in v4040.check_default_values():
	v4040.read_bf_and_print(bit_field)

