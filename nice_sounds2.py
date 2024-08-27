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
    length = int(rate // frequency)  # Number of samples for one period
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

# Note frequencies (in Hz)"My Heart Will Go On – Celine Dion "
note_frequencies = {
    'G': 392.00,
    'F#': 370.00,
    'A': 440.00,
    'B': 493.88,
    'C': 261.63,
    'D': 293.66,
    '^C': 523.25,  # C5
    '^D': 587.33,  # D5
}

# Musical sequence and corresponding waveform types
notes_sequence = [
    ('G', 'custom1'), ('G', 'custom1'), ('G', 'custom1'), ('G', 'custom1'), ('F#', 'custom2'), ('G', 'custom1'),
    ('G', 'custom1'), ('F#', 'custom2'), ('G', 'custom1'), ('A', 'custom3'), ('B', 'custom2'), ('A', 'custom3'),
    ('G', 'custom1'), ('G', 'custom1'), ('G', 'custom1'), ('G', 'custom1'), ('F#', 'custom2'), ('G', 'custom1'), ('G', 'custom1'), ('D', 'custom3'),

    ('G', 'custom1'), ('G', 'custom1'), ('G', 'custom1'), ('G', 'custom1'), ('F#', 'custom2'), ('G', 'custom1'),
    ('G', 'custom1'), ('F#', 'custom2'), ('G', 'custom1'), ('A', 'custom3'), ('B', 'custom2'), ('A', 'custom3'),
    ('G', 'custom1'), ('G', 'custom1'), ('G', 'custom1'), ('G', 'custom1'), ('F#', 'custom2'), ('G', 'custom1'), ('G', 'custom1'), ('D', 'custom3'),

    ('G', 'custom1'), ('A', 'custom3'), ('D', 'custom2'), ('^D', 'custom2'), ('^C', 'custom1'), ('B', 'custom2'), ('A', 'custom3'),
    ('B', 'custom2'), ('^C', 'custom1'), ('B', 'custom2'), ('A', 'custom3'), ('G', 'custom1'), ('F#', 'custom2'), ('G', 'custom1'), ('G', 'custom1'), ('D', 'custom3'),

    ('G', 'custom1'), ('A', 'custom3'), ('D', 'custom2'), ('^D', 'custom2'), ('^C', 'custom1'), ('B', 'custom2'), ('A', 'custom3'),
    ('B', 'custom2'), ('^C', 'custom1'), ('B', 'custom2'), ('A', 'custom3'), ('G', 'custom1'), ('F#', 'custom2'), ('G', 'custom1'),
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

