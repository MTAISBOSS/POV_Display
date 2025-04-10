from machine import Pin, Timer
from time import sleep, ticks_ms

led_pins = [Pin(i, Pin.OUT) for i in range(7, 15)]
beauty_leds = [Pin(6, Pin.OUT), Pin(15, Pin.OUT)]
hall_sensor = Pin(16, Pin.IN, Pin.PULL_UP)

COLUMN_DELAY = 0.001
DIGIT_SPACE = 2
DIGIT_WIDTH = 5


text_to_show = "ATM"
heart = [
    0b01100000, 0b11110000, 0b11111000, 0b01111100, 0b11111000,0b11110000,0b01100000 # heart fill
    ]
heart_fillout = [
     0b01100000, 0b10010000, 0b10001000, 0b01000100, 0b10001000,0b10010000,0b01100000 # heart fillout
    ]
numbers = [
    [0b01110000, 0b11001000, 0b10101000, 0b10011000, 0b01110000],  # 0
    [0b00000000, 0b10000000, 0b11111000, 0b00000000, 0b00000000],  # 1
    [0b01001000, 0b10011000, 0b10101000, 0b11001000, 0b01001000],  # 2
    [0b10101000, 0b10101000, 0b10101000, 0b10101000, 0b01010000],  # 3
    [0b11100000, 0b00100000, 0b00100000, 0b00100000, 0b11111000],  # 4
    [0b01101000, 0b10101000, 0b10101000, 0b10101000, 0b10110000],  # 5
    [0b01110000, 0b10101000, 0b10101000, 0b10101000, 0b10111000],  # 6
    [0b00000000, 0b10000000, 0b10011000, 0b10100000, 0b01000000],  # 7
    [0b01010000, 0b10101000, 0b10101000, 0b10101000, 0b01010000],  # 8
    [0b01101000, 0b10101000, 0b10101000, 0b10101000, 0b01110000],  # 9
]

characters = {
    "A": [0b11110000, 0b00101000, 0b00101000, 0b00101000, 0b11110000],
    "B": [0b01010000, 0b10101000, 0b10101000, 0b10101000, 0b11111000],
    "C": [0b01010000, 0b10001000, 0b10001000, 0b10001000, 0b01110000],
    "D": [0b00100000, 0b01010000, 0b10001000, 0b10001000, 0b11111000],
    "E": [0b10001000, 0b10101000, 0b10101000, 0b10101000, 0b11111000],
    "F": [0b00001000, 0b00101000, 0b00101000, 0b00101000, 0b11111000],
    "G": [0b01101000, 0b10101000, 0b10101000, 0b10001000, 0b01110000],
    "H": [0b11111000, 0b00100000, 0b00100000, 0b00100000, 0b11111000],
    "I": [0b00000000, 0b00000000, 0b11111000, 0b00000000, 0b00000000],
    "J": [0b01110000, 0b10001000, 0b10001000, 0b10001000, 0b01000000],
    "K": [0b10001000, 0b01010000, 0b00100000, 0b00100000, 0b11111000],
    "L": [0b10000000, 0b10000000, 0b10000000, 0b10000000, 0b11111000],
    "M": [0b11111000, 0b00001000, 0b00110000, 0b00001000, 0b11111000],
    "N": [0b11111000, 0b01000000, 0b00100000, 0b00010000, 0b11111000],
    "O": [0b01110000, 0b10001000, 0b10001000, 0b10001000, 0b01110000],
    "P": [0b00110000, 0b01001000, 0b01001000, 0b01001000, 0b11110000],
    "Q": [0b10110000, 0b01001000, 0b10001000, 0b10001000, 0b01110000],
    "R": [0b10110000, 0b01001000, 0b01001000, 0b01001000, 0b11110000],
    "S": [0b01101000, 0b10101000, 0b10101000, 0b10101000, 0b10110000],
    "T": [0b00001000, 0b00001000, 0b11111000, 0b00001000, 0b00001000],
    "U": [0b01111000, 0b10000000, 0b10000000, 0b10000000, 0b01111000],
    "V": [0b00111000, 0b01000000, 0b10000000, 0b01000000, 0b00111000],
    "W": [0b11111000, 0b01000000, 0b01100000, 0b01000000, 0b11111000],
    "X": [0b10001000, 0b01010000, 0b00100000, 0b01010000, 0b10001000],
    "Y": [0b00001000, 0b00010000, 0b11100000, 0b00010000, 0b00001000],
    "Z": [0b10001000, 0b10011000, 0b10101000, 0b11001000, 0b10001000],
}
hours = 12
minutes = 0
seconds = 0

def update_time(timer):
    global hours, minutes, seconds
    seconds += 1
    if seconds == 60:
        seconds = 0
        minutes += 1
        if minutes == 60:
            minutes = 0
            hours += 1
        if hours == 24:
            hours = 0

time_timer = Timer()
time_timer.init(period=1000, mode=Timer.PERIODIC, callback=update_time)

def send_to_pins(col_data):
    for i, pin in enumerate(led_pins):
        pin.value((col_data >> i) & 1)

def clear_leds():
    for pin in led_pins:
        pin.value(0)
    for pin in beauty_leds:
        pin.value(0)

def display_pattern(pattern):
    for col in pattern:
        clear_leds()
        send_to_pins(col)
        sleep(COLUMN_DELAY)

def add_space():
    for _ in range(DIGIT_SPACE):
        clear_leds()
        sleep(COLUMN_DELAY)

def display_time():
    global hours, minutes, seconds
    if hours < 10:
        display_pattern(numbers[0])
        add_space()
        display_pattern(numbers[hours])
    else:
        display_pattern(numbers[hours // 10])
        add_space()
        display_pattern(numbers[hours % 10])
    add_space()

    display_pattern([0b01010000])
    add_space()


    if minutes < 10:
        display_pattern(numbers[0])
        add_space()
        display_pattern(numbers[minutes])
    else:
        display_pattern(numbers[minutes // 10])
        add_space()
        display_pattern(numbers[minutes % 10])
    add_space()

    display_pattern([0b01010000])
    add_space()

    if seconds < 10:
        display_pattern(numbers[0])
        add_space()
        display_pattern(numbers[seconds])
    else:
        display_pattern(numbers[seconds // 10])
        add_space()
        display_pattern(numbers[seconds % 10])
    add_space()
        
text_displayed = False

    
def display_text(text):
    for char in text:
        if char.isdigit():
            display_pattern(numbers[int(char)])
        elif char.upper() in characters:
            display_pattern(characters[char.upper()])
        add_space()
def display_animation():
    display_pattern([0b01010101])


def display_picture(pic_pattern):
    for col_data in pic_pattern:
        clear_leds()
        send_to_pins(col_data)
        sleep(COLUMN_DELAY)
    add_space()
    add_space()
    add_space()
# Example usage
picture_pattern =[
0b00000000,
0b00000000,
0b00000000,
0b00000000,
0b00000000,
0b00100000,
0b00100000,
0b00100100,
0b00100100,
0b00100100,
0b00100000,
0b00100000,
0b00100000,
0b00100000,
0b00100000,
0b00100000,
0b00100000,
0b00100000,
0b00100000,
0b00100000,
0b00100000,
0b00100000,
0b00100100,
0b00100100,
0b00100000,
0b00100000,
0b00000000,
0b00000000,
0b00000000,
0b00000000,
0b00000000,
0b00000000,
]

def display_picture_full_circle(pic_pattern):
    rotation_time = 0.02 
    num_columns = len(pic_pattern)
    column_delay = rotation_time / num_columns

    for col_data in pic_pattern:
        clear_leds()
        send_to_pins(col_data)
        sleep(column_delay)
 
 # Define lyrics with their timings
lyrics = [
    (23, 24, "TSAL"),          # "LAST" reversed
    (24, 25, "SAMTSIRHC"),       # "CHRISTMAS" reversed
    (25, 25.5, "I"),               # "I" reversed (stays the same)
    (25.5, 26, "EVAG"),          # "GAVE" reversed
    (26, 26.5, "UOY"),           # "YOU" reversed
    (26.5, 27, "YM"),            # "MY" reversed
    (27, 28 ,"TRAEH"),         # "HEART" reversed
    (28,28.5, "TUB"),           # "BUT" reversed
    (28.5,28.8, "EHT"),           # "THE" reversed
    (28.8, 29, "YREV"),          # "VERY" reversed
    (29, 29.5, "TXEN"),          # "NEXT" reversed
    (29.5, 30.5, "YAD"),             # "DAY" reversed
    (30.5, 31, "UOY"),             # "YOU" reversed
    (31, 31.5, "EVAG"),             # "GAVE" reversed
     (31.5, 32.5, "TI"),             # "IT" reversed
     (32.5, 34, "YAWA"),             # "AWAY" reversed
    (34, 36, "SIHT"),             # "THIS" reversed
    (36, 37, "RAEY"),             # "YEAR" reversed
     (37, 37.5, "EVAS OT"),             # "TO SAVE" reversed
    (37.5, 38.5, "MORF EM"),             # "ME FROM" reversed
    (38.5, 39.5, "SRAET"),             # "TEARS" reversed
    (39.5, 39.8, "LL I"),             # "I LL" reversed
    (39.8, 41, "TI EVIG"),             # "GIVE IT" reversed
    (41, 41.5, "OT"),             # "TO" reversed
     (41.5, 42.5, "ENOEMOS"),             # "SOMEONE" reversed
    (42.5, 44, "LAICEPS"),             # "SPECIAL" reversed
    # Add more lyrics as needed
    
    (45.5, 46.5, "TSAL"),
    (46.5, 47.5, "SAMTSIRHC"),
    (47.5, 48.0, "I"),
    (48.0, 48.5, "EVAG"),
    (48.5, 49.0, "UOY"),
    (49.0, 49.5, "YM"),
    (49.5, 50.5, "TRAEH"),
    (50.5, 51.0, "TUB"),
    (51.0, 51.3, "EHT"),
    (51.3, 51.5, "YREV"),
    (51.5, 52.0, "TXEN"),
    (52.0, 53.0, "YAD"),
    (53.0, 53.5, "UOY"),
    (53.5, 54.0, "EVAG"),
    (54.0, 55.0, "TI"),
    (55.0, 56.5, "YAWA"),
    (56.5, 58.5, "SIHT"),
    (58.5, 59.5, "RAEY"),
    (59.5, 60.0, "EVAS OT"),
    (60.0, 61.0, "MORF EM"),
    (61.0, 62.0, "SRAET"),
    (62.0, 62.3, "LL I"),
    (62.3, 63.5, "TI EVIG"),
    (63.5, 64.0, "OT"),
    (64.0, 65.0, "ENOEMOS"),
    (65.0, 66.5, "LAICEPS")
]

def display_lyrics(current_time):
    for start, end, text in lyrics:
        if start <= current_time < end:
            display_text(text)  # Display the reversed text
            break

def hypnotism_pattern():
    """
    Display a hypnotism-like swirling pattern.
    """
    pattern = [
        0b00000001,  # LED 1 on
        0b00000010,  # LED 2 on
        0b00000100,  # LED 3 on
        0b00001000,  # LED 4 on
        0b00010000,  # LED 5 on
        0b00100000,  # LED 6 on
        0b01000000,  # LED 7 on
        0b10001111,  # LED 8 on
    ]
    while True:
        for col in pattern:
            clear_leds()
            send_to_pins(col)
            sleep(COLUMN_DELAY)
        # Reverse the pattern for a swirling effect
        pattern = pattern[::-1]

def ping_pong_effect():
    """
    Display a ping-pong effect where LEDs light up one by one and then reverse.
    """
    leds = [1 << i for i in range(len(led_pins))]  # Create a list of LED patterns (1, 2, 4, 8, 16, 32, 64, 128)
    while True:
        # Move forward
        for led in leds:
            clear_leds()
            send_to_pins(led)
            sleep(COLUMN_DELAY)
        # Move backward
        for led in reversed(leds):
            clear_leds()
            send_to_pins(led)
            sleep(COLUMN_DELAY)

def turn_on_leds_one_by_one():
    """
    Turn on LEDs one by one every second.
    """
    for pin in led_pins:
        pin.value(1)  # Turn on the current LED
        sleep(1)      # Wait for 1 second
    # Turn off all LEDs after reaching the last one
    for pin in led_pins:
        pin.value(0)
 # Main loop
start_time = ticks_ms()
while True:
    for pin in beauty_leds:
        pin.value(1)
        
    current_time = (ticks_ms() - start_time) / 1000  # Convert to seconds

    if hall_sensor.value() == 0 and not text_displayed:
        #display_text(text_to_show)
        #display_time()
          #  display_picture(heart)
         #   display_picture(heart)
         #   display_picture(heart)
        if 0 <= current_time < 15:
            turn_on_leds_one_by_one()
        if  15 <= current_time < 30:
            hypnotism_pattern()
        # Ping-pong effect after a certain time
        if 30 <= current_time < 45:
            ping_pong_effect()
            '''
        display_lyrics(current_time)
        if current_time > 67 and current_time < 74:
            display_picture(heart)
            display_picture(heart)
            display_picture(heart)
            display_picture(heart)
            display_picture(heart)
            display_picture(heart)
        if current_time > 74:
            display_picture(heart_fillout)
            display_picture(heart_fillout)
            display_picture(heart_fillout)
            display_picture(heart_fillout)
            display_picture(heart_fillout)
            display_picture(heart_fillout)'''
        text_displayed = True
    elif hall_sensor.value() == 1:
        clear_leds()
        text_displayed = False

