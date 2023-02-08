REM A program that causes the strobe light to flash with every 50 pulses on an input pin detected.
symbol pulse_counter = b0

init:
	setfreq m64
	let pulse_counter = 0
	output C.7
	low C.7
	
REM	hintsetup %00000100 ; Setup hardware interrupt on B.1 / pin 17
	REM allows hardware pin setting when B.1 encounters falling edge
REM	setintflags %00000100, %00000100 ; Interrupt only on hint2 / B.1 flag set
	
REM Maybe use hint on hint2 (B.1, 17?)
main:
	goto main

REM Interrupt:
REM 	let flags = %11111011 & flags ; reset hint2
REM 	let pulse_counter = pulse_counter + 1
REM	let pulse_counter = pulse_counter % 50
REM	if pulse_counter = 0 then
REM		low C.7
REM		high C.7
REM	endif

REM	do while pinB.1 = 0
REM	loop

REM	; setint %00100000, %00100000, C
REM	return
