import smbus
import time

class VCNL4040:
	
	def __init__(self, slave_id=0x60, debug=False):
		self.slave_id  = slave_id
		self.bus       = smbus.SMBus(1)
		self.debug     = debug

	class bitfield_type:
		def __init__(self, NAME       = "",
		                   ADDRESS    = 0x00,
		                   RST_VAL    = 0x0000,
		                   WIDTH      = 0,
		                   OFFSET     = 0,
		                   ACCESS     = "",
		                   TABLE_ENUM = {},
		                   OTHER      = "" ):

			self.NAME        = NAME
			self.ADDRESS     = ADDRESS
			self.RST_VAL     = RST_VAL
			self.WIDTH       = WIDTH
			self.OFFSET      = OFFSET
			self.ACCESS      = ACCESS
			self.TABLE_ENUM  = TABLE_ENUM
			self.OTHER       = OTHER
			self.BIT_MASK    = int(2 ** self.WIDTH - 1) << self.OFFSET

	######################################
	# COMMAND REGISTER 0x00
	######################################

	BF_ALS_SD = bitfield_type (
	NAME       = "ALS_SD",
	ADDRESS    = 0x00,
	RST_VAL    = 0x01,
	WIDTH      = 1,
	OFFSET     = 0,
	ACCESS     = "RW",
	TABLE_ENUM = { "ENABLE" : 0, "DISABLE" : 1 } )
	
	BF_ALS_INT_EN = bitfield_type (
	NAME       = "ALS_INT_EN",
	ADDRESS    = 0x00,
	RST_VAL    = 0x00,
	WIDTH      = 1,
	OFFSET     = 1,
	ACCESS     = "RW",
	TABLE_ENUM = { "DISABLE" : 0, "ENABLE" : 1 } )

	BF_ALS_PERS = bitfield_type (
	NAME       = "ALS_PERS",
	ADDRESS    = 0x00,
	RST_VAL    = 0x00,
	WIDTH      = 2,
	OFFSET     = 2,
	ACCESS     = "RW",
	TABLE_ENUM = { "SETTING_1" : 0, "SETTING_2" : 1, "SETTING_4" : 2, "SETTING_8" : 3 } )
	
	BF_ALS_IT = bitfield_type (
	NAME       = "ALS_IT",
	ADDRESS    = 0x00,
	RST_VAL    = 0x00,
	WIDTH      = 2,
	OFFSET     = 6,
	ACCESS     = "RW",
	TABLE_ENUM = { "80ms" : 0, "160ms" : 1, "320ms" : 2, "640ms" : 3 } )

	######################################
	# COMMAND REGISTER 0x01
	######################################

	# ALS high interrupt threshold 2 bytes
	BF_ALS_THDH = bitfield_type (
	NAME       = "ALS_THDH",
	ADDRESS    = 0x01,
	RST_VAL    = 0x0000,
	WIDTH      = 16,
	OFFSET     = 0,
	ACCESS     = "RW",
	TABLE_ENUM = { } )
	
	######################################
	# COMMAND REGISTER 0x02
	######################################
	
	# ALS low interrupt threshold LSB byte
	BF_ALS_THDL = bitfield_type (
	NAME       = "ALS_THDL",
	ADDRESS    = 0x02,
	RST_VAL    = 0x0000,
	WIDTH      = 16,
	OFFSET     = 0,
	ACCESS     = "RW",
	TABLE_ENUM = { } )

	######################################
	# COMMAND REGISTER 0x03
	######################################

	BF_PS_SD = bitfield_type (
	NAME       = "PS_SD",
	ADDRESS    = 0x03,
	RST_VAL    = 0x01,
	WIDTH      = 1,
	OFFSET     = 0,
	ACCESS     = "RW",
	TABLE_ENUM = { "PS_POWER_ON" : 0, "PS_SHUT_DOWN" : 1 } )
	
	# PS integration time setting
	BF_PS_IT = bitfield_type (
	NAME       = "PS_IT",
	ADDRESS    = 0x03,
	RST_VAL    = 0x00,
	WIDTH      = 3,
	OFFSET     = 1,
	ACCESS     = "RW",
	TABLE_ENUM = { "1T" : 0, "1.5T" : 1, "2T" : 2, "2.5T" : 3, "3T" : 4, "3.5T" : 5, "4T" : 6, "8T" : 7 } )

	BF_PS_PERS = bitfield_type (
	NAME       = "PS_PERS",
	ADDRESS    = 0x03,
	RST_VAL    = 0x00,
	WIDTH      = 2,
	OFFSET     = 4,
	ACCESS     = "RW",
	TABLE_ENUM = { "SETTING_1" : 0, "SETTING_2" : 1, "SETTING_3" : 2, "SETTING_4" : 3 } )

	# PS IRED on / off duty ratio setting
	BF_PS_DUTY = bitfield_type (
	NAME       = "PS_DUTY",
	ADDRESS    = 0x03,
	RST_VAL    = 0x00,
	WIDTH      = 2,
	OFFSET     = 6,
	ACCESS     = "RW",
	TABLE_ENUM = { "1/40" : 0, "1/80" : 1, "1/160" : 2, "1/320" : 3 } )

	BF_PS_INT = bitfield_type (
	NAME       = "PS_INT",
	ADDRESS    = 0x03,
	RST_VAL    = 0x00,
	WIDTH      = 2,
	OFFSET     = 8,
	ACCESS     = "RW",
	TABLE_ENUM = { "DISABLE" : 0, "TRIGGER_WHEN_CLOSE" : 1, "TRIGGER_WHEN_AWAY" : 2, "TRIGGER_WHEN_CLOSE_OR_AWAY" : 3 } )

	BF_PS_HD = bitfield_type (
	NAME       = "PS_HD",
	ADDRESS    = 0x03,
	RST_VAL    = 0x00,
	WIDTH      = 1,
	OFFSET     = 10,
	ACCESS     = "RW",
	TABLE_ENUM = { "PS_OUTPUT_IS_12BIT" : 0, "PS_OUTPUT_IS_16BIT" : 1 } )

	######################################
	# COMMAND REGISTER 0x04
	######################################

	BF_PS_SC_EN = bitfield_type (
	NAME       = "PS_SC_EN",
	ADDRESS    = 0x04,
	RST_VAL    = 0x00,
	WIDTH      = 1,
	OFFSET     = 0,
	ACCESS     = "RW",
	TABLE_ENUM = { "PS_SUNLIGHT_DISABLE" : 0, "PS_SUNLIGHT_ENABLE" : 1 } )

	BF_PS_TRIG = bitfield_type (
	NAME       = "PS_TRIG",
	ADDRESS    = 0x04,
	RST_VAL    = 0x00,
	WIDTH      = 1,
	OFFSET     = 2,
	ACCESS     = "RW",
	TABLE_ENUM = { "NO_PS_ACTIVE_FORCE_MODE_TRIGGER" : 0, "TRIGGER_ONE_TIME_CYCLE" : 1 } )

	BF_PS_AF = bitfield_type (
	NAME       = "PS_AF",
	ADDRESS    = 0x04,
	RST_VAL    = 0x00,
	WIDTH      = 1,
	OFFSET     = 3,
	ACCESS     = "RW",
	TABLE_ENUM = { "ACTIVE_FORCE_MODE_DISABLE" : 0, "ACTIVE_FORCE_MODE_ENABLE" : 1 } )

	BF_PS_SMART_PERS = bitfield_type (
	NAME       = "PS_SMART_PERS",
	ADDRESS    = 0x04,
	RST_VAL    = 0x00,
	WIDTH      = 1,
	OFFSET     = 4,
	ACCESS     = "RW",
	TABLE_ENUM = { "DISABLE" : 0, "ENABLE" : 1 } )

	BF_PS_MPS = bitfield_type (
	NAME       = "PS_MPS",
	ADDRESS    = 0x04,
	RST_VAL    = 0x00,
	WIDTH      = 2,
	OFFSET     = 5,
	ACCESS     = "RW",
	TABLE_ENUM = { "1_MULTI_PULSE" : 0, "2_MULTI_PULSE" : 1, "4_MULTI_PULSE" : 2, "8_MULTI_PULSE" : 3 } )

	BF_LED_I = bitfield_type (
	NAME       = "LED_I",
	ADDRESS    = 0x04,
	RST_VAL    = 0x00,
	WIDTH      = 3,
	OFFSET     = 8,
	ACCESS     = "RW",
	TABLE_ENUM = { "50mA" : 0, "75mA" : 1, "100mA" : 2, "120mA" : 3, "140mA" : 4, "160mA" : 5, "180mA" : 6, "200mA" : 7 } )

	BF_PS_MS = bitfield_type (
	NAME       = "PS_MS",
	ADDRESS    = 0x04,
	RST_VAL    = 0x00,
	WIDTH      = 1,
	OFFSET     = 14,
	ACCESS     = "RW",
	TABLE_ENUM = { "PROXIMITY_NORMAL_WITH_INTERRUPT_FUNCTION" : 0, "PROXIMITY_DETECTION_LOGIC_OUTPUT_MODE_ENABLE" : 1 } )

	BF_WHITE_EN = bitfield_type (
	NAME       = "WHITE_EN",
	ADDRESS    = 0x04,
	RST_VAL    = 0x00,
	WIDTH      = 1,
	OFFSET     = 15,
	ACCESS     = "RW",
	TABLE_ENUM = { "ENABLE" : 0, "DISABLE" : 1 } )

	######################################
	# COMMAND REGISTER 0x05
	######################################

	# PS cancellation level setting 2 bytes
	BF_PS_CANC = bitfield_type (
	NAME       = "PS_CANC",
	ADDRESS    = 0x05,
	RST_VAL    = 0x0000,
	WIDTH      = 16,
	OFFSET     = 0,
	ACCESS     = "RW",
	TABLE_ENUM = { } )

	######################################
	# COMMAND REGISTER 0x06
	######################################

	# PS interrupt low threshold setting 2 bytes
	BF_PS_THDL = bitfield_type (
	NAME       = "PS_THDL",
	ADDRESS    = 0x06,
	RST_VAL    = 0x0000,
	WIDTH      = 16,
	OFFSET     = 0,
	ACCESS     = "RW",
	TABLE_ENUM = { } )

	######################################
	# COMMAND REGISTER 0x07
	######################################

	# PS interrupt high threshold setting 2 bytes
	BF_PS_THDH = bitfield_type (
	NAME       = "PS_THDH",
	ADDRESS    = 0x07,
	RST_VAL    = 0x0000,
	WIDTH      = 16,
	OFFSET     = 0,
	ACCESS     = "RW",
	TABLE_ENUM = { } )

	######################################
	# COMMAND REGISTER 0x08
	######################################

	# PS LSB output data 2 bytes
	BF_PS_DATA = bitfield_type (
	NAME       = "PS_DATA",
	ADDRESS    = 0x08,
	RST_VAL    = 0x0000,
	WIDTH      = 16,
	OFFSET     = 0,
	ACCESS     = "RO",
	TABLE_ENUM = { } )

	######################################
	# COMMAND REGISTER 0x09
	######################################

	# ALS LSB output data 2 bytes
	BF_ALS_DATA = bitfield_type (
	NAME       = "ALS_DATA",
	ADDRESS    = 0x09,
	RST_VAL    = 0x0000,
	WIDTH      = 16,
	OFFSET     = 0,
	ACCESS     = "RO",
	TABLE_ENUM = { } )

	######################################
	# COMMAND REGISTER 0x0A
	######################################

	BF_WHITE_DATA = bitfield_type (
	NAME       = "WHITE_DATA",
	ADDRESS    = 0x0A,
	RST_VAL    = 0x0000,
	WIDTH      = 16,
	OFFSET     = 0,
	ACCESS     = "RO",
	TABLE_ENUM = { } )

	######################################
	# COMMAND REGISTER 0x0B
	######################################
	
	#!!! All bits in this register are cleared with a single read !!!#

	# PS drops below PS_THDL INT trigger event
	BF_PS_IF_AWAY_INT = bitfield_type (
	NAME       = "PS_IF_AWAY_INT",
	ADDRESS    = 0x0B,
	RST_VAL    = 0x00,
	WIDTH      = 1,
	OFFSET     = 8,
	ACCESS     = "RO",
	TABLE_ENUM = { } )

	BF_PS_IF_CLOSE_INT = bitfield_type (
	NAME       = "PS_IF_CLOSE_INT",
	ADDRESS    = 0x0B,
	RST_VAL    = 0x00,
	WIDTH      = 1,
	OFFSET     = 9,
	ACCESS     = "RO",
	TABLE_ENUM = { } )

	# ALS crossing high THD INT trigger event
	BF_ALS_IF_H_INT = bitfield_type (
	NAME       = "ALS_IF_H_INT",
	ADDRESS    = 0x0B,
	RST_VAL    = 0x00,
	WIDTH      = 1,
	OFFSET     = 12,
	ACCESS     = "RO",
	TABLE_ENUM = { } )
	
	# ALS crossing low THD INT trigger event
	BF_ALS_IF_L_INT = bitfield_type (
	NAME       = "ALS_IF_L_INT",
	ADDRESS    = 0x0B,
	RST_VAL    = 0x00,
	WIDTH      = 1,
	OFFSET     = 13,
	ACCESS     = "RO",
	TABLE_ENUM = { } )
	
	# PS entering protection mode
	BF_PS_SPFLAG_INT = bitfield_type (
	NAME       = "PS_SPFLAG_INT",
	ADDRESS    = 0x0B,
	RST_VAL    = 0x00,
	WIDTH      = 1,
	OFFSET     = 14,
	ACCESS     = "RO",
	TABLE_ENUM = { } )

	######################################
	# COMMAND REGISTER 0x0C
	######################################

	# 86H for MP version sample, device ID LSB byte
	BF_ID_L = bitfield_type (
	NAME       = "ID_L",
	ADDRESS    = 0x0C,
	RST_VAL    = 0x86,
	WIDTH      = 8,
	OFFSET     = 0,
	ACCESS     = "RO",
	TABLE_ENUM = { } )

	# device ID MSB byte
	BF_ID_M = bitfield_type (
	NAME       = "ID_M",
	ADDRESS    = 0x0C,
	RST_VAL    = 0x01,
	WIDTH      = 8,
	OFFSET     = 8,
	ACCESS     = "RO",
	TABLE_ENUM = { } )

	LIST_OF_BIT_FIELDS            = [ BF_ALS_SD, BF_ALS_INT_EN, BF_ALS_PERS, BF_ALS_IT, BF_ALS_THDH, BF_ALS_THDL, BF_PS_SD, BF_PS_IT, BF_PS_PERS, BF_PS_DUTY, BF_PS_INT, BF_PS_HD, BF_PS_SC_EN, BF_PS_TRIG, BF_PS_AF, BF_PS_SMART_PERS, BF_PS_MPS, BF_LED_I, BF_PS_MS, BF_WHITE_EN, BF_PS_CANC, BF_PS_THDL, BF_PS_THDH, BF_PS_DATA, BF_ALS_DATA, BF_WHITE_DATA, BF_PS_IF_AWAY_INT, BF_PS_IF_CLOSE_INT, BF_ALS_IF_H_INT, BF_ALS_IF_L_INT, BF_PS_SPFLAG_INT, BF_ID_L, BF_ID_M ]
	LIST_OF_INT_STATUS_BIT_FIELDS = [ BF_PS_IF_AWAY_INT, BF_PS_IF_CLOSE_INT, BF_ALS_IF_H_INT, BF_ALS_IF_L_INT, BF_PS_SPFLAG_INT ]

	def i2c_bf_read(self, bit_field):
		try:
			address  = 0xFF & bit_field.ADDRESS
			bf_read_data = ( self.bus.read_word_data(self.slave_id, address) & bit_field.BIT_MASK ) >> bit_field.OFFSET 
			if (self.debug):
				print("Read bit_field {} address 0x{:02x}, bit mask is 0x{:04x}, value is 0x{:02x}".format(bit_field.NAME, address, bit_field.BIT_MASK, bf_read_data))
			return bf_read_data
		except:
			print("ERROR with i2c_bf_read")
	
	def i2c_bf_write(self, bit_field, bf_wdata):
		try:
			address = 0xFF & bit_field.ADDRESS
			read_data = self.bus.read_word_data(self.slave_id, address)
			wdata = ( read_data & ~bit_field.BIT_MASK) | ((bf_wdata << bit_field.OFFSET) & bit_field.BIT_MASK)
			self.bus.write_word_data(self.slave_id, address, wdata)
			if (self.debug):
				print("Wrote bit_field {} address 0x{:02x}, bit mask is 0x{:04x}, data 0x{:02x}".format(bit_field.NAME, address, bit_field.BIT_MASK, bf_wdata))
		except:
			print("ERROR with i2c_bf_write")
	
	def read_flags(self):
		list_of_flags = []
		try:
			word_read = self.bus.read_word_data(self.slave_id, 0x0B)
			for bit_field in self.LIST_OF_INT_STATUS_BIT_FIELDS:
				if (2 ** bit_field.OFFSET & word_read):
					list_of_flags.append(bit_field.NAME)
			if (self.debug):
				print("Flag raw data is 0x{:04x}".format(word_read))
				print(*list_of_flags)
			return list_of_flags
		except:
			print("ERROR with read_flags")
		
	def check_default_values(self):
		list_of_bit_fields = []
		for bit_field in self.LIST_OF_BIT_FIELDS:
			if (self.i2c_bf_read(bit_field) != bit_field.RST_VAL):
				list_of_bit_fields.append(bit_field)
				if (self.debug):
					print(bit_field.NAME)
		return list_of_bit_fields

	def restore_default_values(self):
		for bit_field in self.LIST_OF_BIT_FIELDS:
			if (bit_field.ACCESS == "RW"):
				self.i2c_bf_write(bit_field, bit_field.RST_VAL)

	def get_key(self, val, my_dict):
		for key, value in my_dict.items():
			if val == value:
				return key

	def read_bf_and_print(self, bit_field):
		value = self.i2c_bf_read(bit_field)
		if (len(bit_field.TABLE_ENUM) != 0):
			print("Bit Field {} is {}".format(bit_field.NAME, self.get_key(value,bit_field.TABLE_ENUM)))
		else:
			print("Bit Field {} has value 0x{:04x}".format(bit_field.NAME, value))
