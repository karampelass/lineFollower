from machine import Pin, PWM
import time

# Motor setup
motor_left_a = PWM(Pin(9))  # Left motor forward
motor_left_b = PWM(Pin(8))  # Left motor backward
motor_right_a = PWM(Pin(11)) # Right motor forward
motor_right_b = PWM(Pin(10)) # Right motor backward

motor_left_a.freq(1000)
motor_left_b.freq(1000)
motor_right_a.freq(1000)
motor_right_b.freq(1000)

# Sensor setup
sensor_left = Pin(7, Pin.IN)
sensor_right = Pin(28, Pin.IN)

# Button setup
button_start = Pin(20, Pin.IN, Pin.PULL_UP)
button_stop = Pin(21, Pin.IN, Pin.PULL_UP)

# Helper function to set motor speeds and directions
def set_motors(left_speed, right_speed):
    if left_speed >= 0:
        motor_left_a.duty_u16(left_speed)
        motor_left_b.duty_u16(0)
    else:
        motor_left_a.duty_u16(0)
        motor_left_b.duty_u16(-left_speed)

    if right_speed >= 0:
        motor_right_a.duty_u16(right_speed)
        motor_right_b.duty_u16(0)
    else:
        motor_right_a.duty_u16(0)
        motor_right_b.duty_u16(-right_speed)

# Main loop
running = False
turn_speed = 30000  # Slower speed for turning
forward_speed = int(0.7 * 30000)  # 70% speed for moving forward

while True:
    if button_start.value() == 0:
        running = True
    if button_stop.value() == 0:
        running = False
    
    if running:
        left_value = sensor_left.value()
        right_value = sensor_right.value()

        # Line following logic
        if left_value == 0 and right_value == 0:
            # Detected a horizontal line
            set_motors(0, 0)
        elif left_value == 0 and right_value == 1:
            # Turn right
            set_motors(turn_speed, -turn_speed)
        elif left_value == 1 and right_value == 0:
            # Turn left
            set_motors(-turn_speed, turn_speed)
        elif left_value == 1 and right_value == 1:
            # Move forward
            set_motors(forward_speed, forward_speed)
        else:
            # No line detected, stop
            set_motors(0, 0)
    else:
        set_motors(0, 0)
    
    time.sleep(0.01)
