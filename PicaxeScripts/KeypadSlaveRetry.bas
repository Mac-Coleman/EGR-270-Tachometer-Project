REM wait a time period until ADC value finishes changing... Maybe?

symbol char = b0
symbol adc_val = b1
symbol maximum = b2
symbol counter = b3
symbol i2c_adr = $30 * 2 ; Set the address of the i2c keyboard to $30 or $60 in 8-bit space.

init:
	setfreq m32
	hi2csetup i2cslave, i2c_adr ; set up as a slave device.

main:
	do
		readadc 1, adc_val
		char = 0
		put 0, char
		put 1, adc_val
	loop until adc_val > 10

	gosub ReadKeypad

	do
		readadc 1, adc_val
		put 0, char
		put 1, adc_val
	loop until adc_val < 10
	goto main

ReadKeypad:
	
	maximum = 0
	for counter = 0 to 128
		readadc 1, adc_val;
		if adc_val > maximum then
			maximum = adc_val
		endif
	next
	
	select case maximum
		case 0 to 66;
			char = 0
		case 67 to 135 ; #
			char = "#"
		case 136 to 141 ; 0
			char = "0"
		case 142 to 147 ; *
			char = "*"
		case 148 to 154 ; 9
			char = "9"
		case 155 to 162 ; 8
			char = "8"
		case 163 to 171 ; 7
			char = "7"
		case 172 to 181 ; 6
			char = "6"
		case 182 to 191 ; 5
			char = "5"
		case 192 to 202 ; 4
			char = "4"
		case 203 to 214 ; 3
			char = "3"
		case 215 to 229 ; 2
			char = "2"
		case 230 to 255 ; 1
			char = "1"
		else ; shrug
	endselect

	put 0, char
	put 1, adc_val

	pause 500
	return
