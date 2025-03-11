from gpiozero import Button
from time import sleep

button = Button(26)

while True:
	if button.is_pressed:
		print("Pressed")
	else:
		print("not")
	sleep(2)
