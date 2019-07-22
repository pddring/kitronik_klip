from microbit import *
import radio

# Robot controller class
class Robot:
    def stop(self):
        pin13.write_digital(0)
        pin14.write_digital(0)
        pin15.write_digital(0)
        pin16.write_digital(0)

    def set_speed(self, motor, speed):
        if speed > 0:
            if motor == "1":
                pin16.write_digital(0)
                pin15.write_analog(speed)
            if motor == "2":
                pin14.write_digital(0)
                pin13.write_analog(speed)
        else:
            speed = 0-speed
            if motor == "1":
                pin15.write_digital(0)
                pin16.write_analog(speed)
            if motor == "2":
                pin13.write_digital(0)
                pin14.write_analog(speed)

r = Robot()
radio.on()
channel = 1

# Choose channel with B, acccept with A
while True:
    display.show(str(channel))
    if button_a.was_pressed():
        break
    if button_b.was_pressed():
        channel = (channel + 1) % 10
    sleep(50)


while True:
    # Listen for radio messages
    msg = radio.receive()
    if msg != None:
        motor, speed, ch = msg.split("_")
        if ch == str(channel):
            r.set_speed(motor, int(speed) * 1000)
            continue

    # Both buttons means forwards
    if button_a.is_pressed() and button_b.is_pressed():
        r.set_speed("1", 1023)
        radio.send("1_1_" + str(channel))
        r.set_speed("2", 1023)
        radio.send("2_1_" + str(channel))
        while button_a.is_pressed() and button_b.is_pressed():
            sleep(50)
        r.set_speed("1", 0)
        radio.send("1_0_" + str(channel))
        r.set_speed("2", 0)
        radio.send("2_0_" + str(channel))
        continue

    # Button B means motor 2 forwards (right)
    if button_b.is_pressed():
        r.set_speed("1", 1023)
        radio.send("1_1_" + str(channel))
        a = button_a.is_pressed()
        while button_b.is_pressed() and button_a.is_pressed() == a:
            sleep(50)
        r.set_speed("1", 0)
        radio.send("1_0_" + str(channel))
        continue

    # Button A means motor 1 forwards (left)
    if button_a.is_pressed():
        r.set_speed("2", 1023)
        radio.send("2_1_" + str(channel))
        b = button_b.is_pressed()
        while button_a.is_pressed() and button_b.is_pressed() == b:
            sleep(50)
        r.set_speed("2", 0)
        radio.send("2_0_" + str(channel))
        continue

    # Wait for next input
    sleep(50)
