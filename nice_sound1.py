#DO RE MI FA SOL , EXAMPLE OF GENERATING NICE SOUNDS BY COMBINING NOTES OF DIFFERENT FREQUENCIES
from machine import I2S, Pin, PWM
import math
import time

def irqhandler(arg):
    print(arg)
    audio_out.write(buf)

# The following is needed for the pmodi2s2 which needs a master clock
pwm = PWM(Pin(0), freq=11289600, duty_u16=32768)

buflen = 2000

audio_out = I2S(0,
                sck=Pin(21),
                ws=Pin(22),
                sd=Pin(23),
                mode=I2S.TX,
                bits=16,
                format=I2S.MONO,
                rate=44100,
                ibuf=buflen)

def generate_waveform(frequency, wave_type='custom', amplitude=32767, rate=44100):
    # Number of samples for one period
    length = int(rate // frequency)  
    buf = bytearray(2 * length)
    for i in range(length):
        if wave_type == 'custom1':
            val = (amplitude * math.sin(2 * math.pi * i / length) +
                   (amplitude // 2) * (1 if i < length / 2 else -1) +
                   (amplitude // 3) * (2 * (i / length) - 1) +
                   (amplitude // 4) * math.sin(2 * 2 * math.pi * i / length) +
                   (amplitude // 5) * math.sin(3 * 2 * math.pi * i / length))
            val = int(val / 2.0)  # Normalize to avoid clipping
        elif wave_type == 'custom2':
            val = (amplitude * math.sin(2 * math.pi * i / length) +
                   (amplitude // 2) * (2 * abs(2 * (i / length) - 1) - 1) +
                   (amplitude // 3) * (2 * (i / length) - 1) +
                   (amplitude // 4) * math.sin(3 * 2 * math.pi * i / length) +
                   (amplitude // 5) * math.sin(4 * 2 * math.pi * i / length))
            val = int(val / 2.0)  # Normalize to avoid clipping
        elif wave_type == 'custom3':
            val = (amplitude * (2 * abs(2 * (i / length) - 1) - 1) +
                   (amplitude // 2) * (1 if i < length / 2 else -1) +
                   (amplitude // 3) * (2 * (i / length) - 1) +
                   (amplitude // 4) * math.sin(2 * 2 * math.pi * i / length) +
                   (amplitude // 5) * math.sin(3 * 2 * math.pi * i / length))
            val = int(val / 2.0)  # Normalize to avoid clipping
        else:
            val = 0

        buf[2 * i] = val & 0xff
        buf[2 * i + 1] = (val >> 8) & 0xff
    return buf

# Note frequencies (in Hz)
note_frequencies = {
    'C4': 261.63,
    'D4': 293.66,
    'E4': 329.63,
    'F4': 349.23,
    'G4': 392.00,
    'A4': 440.00,
    'B4': 493.88,
    'C5': 523.25,
}

# Musical sequence and corresponding waveform types
notes_sequence = [
    # Original "Do, Re, Mi" scale
    ('C4', 'custom1'), ('D4', 'custom2'), ('E4', 'custom3'),
    ('F4', 'custom1'), ('G4', 'custom2'), ('A4', 'custom3'),
    ('B4', 'custom1'), ('C5', 'custom2'),

    # Additional notes in reverse order
    ('B4', 'custom1'),  # TI
    ('A4', 'custom3'),  # La
    ('G4', 'custom1'),  # SOL
    ('F4', 'custom3'),  # FA
	('E4', 'custom2'),  # MI
    ('D4', 'custom1'),  # RE
	('C4', 'custom1'),  # DO
    
]


# Play each note for a specified duration
note_duration = 0.5  # Duration in seconds for each note

for note, wave_type in notes_sequence:
    frequency = note_frequencies[note]
    print(f"Playing {note} ({frequency} Hz) with {wave_type} waveform")
    buf = generate_waveform(frequency, wave_type)

    # Play the note
    start_time = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), start_time) < note_duration * 1000:
        nm = audio_out.write(buf)
        # print(nm)
    print(f"Finished playing {note}")

print("Finished all notes")

