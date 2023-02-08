REM wait a time period until ADC value finishes changing... Maybe?

symbol char = b0
symbol adc_val = b1
symbol maximum = b2
symbol counter = b3
symbol i2c_adr = $30 * 2 ; Set the address of the i2c keyboard to $30 or $60 in 8-bit space.
symbol time_difference = w2
symbol pulse_counter = b7

init:
	setfreq m64
	hi2csetup i2cslave, i2c_adr ; set up as a slave device.
        tmr3setup %10000000 ; 1:1 Prescale (Each tick is 62.5 ns at 64 MHz) Disabled.
	output C.7 ; Make output pin C.7 (Used for flashing)
	let pulse_counter = 0
	; input C.5
	setint %00100000, %00100000, C

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

Flash:
	low C.7
	high C.7
	return

interrupt:
REM I want this to fire every time the signal goes low.
	let time_difference = timer3 ; Record the time difference
	let timer3 = 0 ;
	let pulse_counter = pulse_counter + 1
	let pulse_counter = pulse_counter % 50 ; mod 50
	if pulse_counter = 0 then
		gosub Flash
	endif

	do while pinC.5 = 1
	loop ; Do nothing 
	setint %00100000, %00100000, C ; Make an interrupt on pin C.6
	return


