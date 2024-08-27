from machine import I2S, Pin, PWM
import math
import time

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

# Function to convert MIDI note to frequency
def midi_to_frequency(midi_note):
    return 440.0 * (2 ** ((midi_note - 69) / 12.0))

# JSON data with MIDI notes, durations, and velocities
# Sample MIDI data
midi_data = [
    {
            "duration": 0.21428574999999994,
            "durationTicks": 240,
            "midi": 76,
            "name": "E5",
            "ticks": 960,
            "time": 0.857143,
            "velocity": 0.5590551181102362
          },
          {
            "duration": 0.21428575000000016,
            "durationTicks": 240,
            "midi": 75,
            "name": "D#5",
            "ticks": 1200,
            "time": 1.07142875,
            "velocity": 0.2992125984251969
          },
          {
            "duration": 0.21428574999999994,
            "durationTicks": 240,
            "midi": 76,
            "name": "E5",
            "ticks": 1440,
            "time": 1.2857145,
            "velocity": 0.44881889763779526
          },
          {
            "duration": 0.21428574999999994,
            "durationTicks": 240,
            "midi": 75,
            "name": "D#5",
            "ticks": 1680,
            "time": 1.50000025,
            "velocity": 0.5511811023622047
          },
          {
            "duration": 0.21428574999999994,
            "durationTicks": 240,
            "midi": 76,
            "name": "E5",
            "ticks": 1920,
            "time": 1.714286,
            "velocity": 0.5984251968503937
          },
          {
            "duration": 0.21428574999999994,
            "durationTicks": 240,
            "midi": 71,
            "name": "B4",
            "ticks": 2160,
            "time": 1.92857175,
            "velocity": 0.5984251968503937
          },
          {
            "duration": 0.21428575000000016,
            "durationTicks": 240,
            "midi": 74,
            "name": "D5",
            "ticks": 2400,
            "time": 2.1428575,
            "velocity": 0.5984251968503937
          },
          {
            "duration": 0.21428575000000016,
            "durationTicks": 240,
            "midi": 72,
            "name": "C5",
            "ticks": 2640,
            "time": 2.35714325,
            "velocity": 0.6535433070866141
          },
          {
            "duration": 0.6428572499999996,
            "durationTicks": 720,
            "midi": 69,
            "name": "A4",
            "ticks": 2880,
            "time": 2.571429,
            "velocity": 0.7007874015748031
          },
          {
            "duration": 0.21428574999999972,
            "durationTicks": 240,
            "midi": 45,
            "name": "A2",
            "ticks": 2880,
            "time": 2.571429,
            "velocity": 0.5039370078740157
          },
          {
            "duration": 0.21428575000000016,
            "durationTicks": 240,
            "midi": 52,
            "name": "E3",
            "ticks": 3120,
            "time": 2.78571475,
            "velocity": 0.5039370078740157
          },
          {
            "duration": 0.21428574999999972,
            "durationTicks": 240,
            "midi": 57,
            "name": "A3",
            "ticks": 3360,
            "time": 3.0000005,
            "velocity": 0.5511811023622047
          },
          {
            "duration": 0.21428575000000016,
            "durationTicks": 240,
            "midi": 60,
            "name": "C4",
            "ticks": 3600,
            "time": 3.21428625,
            "velocity": 0.5984251968503937
          },
          {
            "duration": 0.21428575000000016,
            "durationTicks": 240,
            "midi": 64,
            "name": "E4",
            "ticks": 3840,
            "time": 3.428572,
            "velocity": 0.5984251968503937
          },
          {
            "duration": 0.21428574999999972,
            "durationTicks": 240,
            "midi": 69,
            "name": "A4",
            "ticks": 4080,
            "time": 3.64285775,
            "velocity": 0.5984251968503937
          },
          {
            "duration": 0.64285725,
            "durationTicks": 720,
            "midi": 71,
            "name": "B4",
            "ticks": 4320,
            "time": 3.8571435,
            "velocity": 0.6535433070866141
          },
          {
            "duration": 0.21428574999999972,
            "durationTicks": 240,
            "midi": 40,
            "name": "E2",
            "ticks": 4320,
            "time": 3.8571435,
            "velocity": 0.5039370078740157
          },
          {
            "duration": 0.21428575000000016,
            "durationTicks": 240,
            "midi": 52,
            "name": "E3",
            "ticks": 4560,
            "time": 4.0714292499999996,
            "velocity": 0.5039370078740157
          },
          {
            "duration": 0.21428575000000016,
            "durationTicks": 240,
            "midi": 56,
            "name": "G#3",
            "ticks": 4800,
            "time": 4.285715,
            "velocity": 0.5511811023622047
          },
          {
            "duration": 0.21428575000000016,
            "durationTicks": 240,
            "midi": 64,
            "name": "E4",
            "ticks": 5040,
            "time": 4.50000075,
            "velocity": 0.5984251968503937
          },
          {
            "duration": 0.21428575000000016,
            "durationTicks": 240,
            "midi": 68,
            "name": "G#4",
            "ticks": 5280,
            "time": 4.7142865,
            "velocity": 0.5984251968503937
          },
          {
            "duration": 0.21428575000000016,
            "durationTicks": 240,
            "midi": 71,
            "name": "B4",
            "ticks": 5520,
            "time": 4.92857225,
            "velocity": 0.5984251968503937
          },
          {
            "duration": 0.6428572499999996,
            "durationTicks": 720,
            "midi": 72,
            "name": "C5",
            "ticks": 5760,
            "time": 5.142858,
            "velocity": 0.6535433070866141
          },
          {
            "duration": 0.21428574999999928,
            "durationTicks": 240,
            "midi": 45,
            "name": "A2",
            "ticks": 5760,
            "time": 5.142858,
            "velocity": 0.5039370078740157
          },
          {
            "duration": 0.21428575000000016,
            "durationTicks": 240,
            "midi": 52,
            "name": "E3",
            "ticks": 6000,
            "time": 5.35714375,
            "velocity": 0.5511811023622047
          },
          {
            "duration": 0.21428575000000016,
            "durationTicks": 240,
            "midi": 57,
            "name": "A3",
            "ticks": 6240,
            "time": 5.5714295,
            "velocity": 0.5984251968503937
          },
          {
            "duration": 0.21428575000000016,
            "durationTicks": 240,
            "midi": 64,
            "name": "E4",
            "ticks": 6480,
            "time": 5.78571525,
            "velocity": 0.5984251968503937
          },
          {
            "duration": 0.21428575000000016,
            "durationTicks": 240,
            "midi": 76,
            "name": "E5",
            "ticks": 6720,
            "time": 6.000001,
            "velocity": 0.5984251968503937
          },
          {
            "duration": 0.21428574999999928,
            "durationTicks": 240,
            "midi": 75,
            "name": "D#5",
            "ticks": 6960,
            "time": 6.21428675,
            "velocity": 0.5039370078740157
          },
          {
            "duration": 0.21428575000000016,
            "durationTicks": 240,
            "midi": 76,
            "name": "E5",
            "ticks": 7200,
            "time": 6.4285725,
            "velocity": 0.5984251968503937
          },
          {
            "duration": 0.21428575000000016,
            "durationTicks": 240,
            "midi": 75,
            "name": "D#5",
            "ticks": 7440,
            "time": 6.64285825,
            "velocity": 0.5511811023622047
          },
          {
            "duration": 0.21428575000000016,
            "durationTicks": 240,
            "midi": 76,
            "name": "E5",
            "ticks": 7680,
            "time": 6.857144,
            "velocity": 0.5984251968503937
          },
          {
            "duration": 0.21428575000000016,
            "durationTicks": 240,
            "midi": 71,
            "name": "B4",
            "ticks": 7920,
            "time": 7.07142975,
            "velocity": 0.5984251968503937
          },
          {
            "duration": 0.21428574999999928,
            "durationTicks": 240,
            "midi": 74,
            "name": "D5",
            "ticks": 8160,
            "time": 7.2857155,
            "velocity": 0.5984251968503937
          },
          {
            "duration": 0.21428575000000016,
            "durationTicks": 240,
            "midi": 72,
            "name": "C5",
            "ticks": 8400,
            "time": 7.5000012499999995,
            "velocity": 0.5984251968503937
          },
          {
            "duration": 0.6428572499999996,
            "durationTicks": 720,
            "midi": 69,
            "name": "A4",
            "ticks": 8640,
            "time": 7.714287,
            "velocity": 0.6535433070866141
          },
          {
            "duration": 0.21428575000000016,
            "durationTicks": 240,
            "midi": 45,
            "name": "A2",
            "ticks": 8640,
            "time": 7.714287,
            "velocity": 0.44881889763779526
          },
          {
            "duration": 0.21428574999999928,
            "durationTicks": 240,
            "midi": 52,
            "name": "E3",
            "ticks": 8880,
            "time": 7.92857275,
            "velocity": 0.5039370078740157
          },
          {
            "duration": 0.21428575000000016,
            "durationTicks": 240,
            "midi": 57,
            "name": "A3",
            "ticks": 9120,
            "time": 8.142858499999999,
            "velocity": 0.5511811023622047
          },
          {
            "duration": 0.21428575000000016,
            "durationTicks": 240,
            "midi": 60,
            "name": "C4",
            "ticks": 9360,
            "time": 8.35714425,
            "velocity": 0.5984251968503937
          },
          {
            "duration": 0.21428575000000016,
            "durationTicks": 240,
            "midi": 64,
            "name": "E4",
            "ticks": 9600,
            "time": 8.57143,
            "velocity": 0.5984251968503937
          },
          {
            "duration": 0.21428575000000016,
            "durationTicks": 240,
            "midi": 69,
            "name": "A4",
            "ticks": 9840,
            "time": 8.78571575,
            "velocity": 0.5984251968503937
          },
          {
            "duration": 0.6428572500000005,
            "durationTicks": 720,
            "midi": 71,
            "name": "B4",
            "ticks": 10080,
            "time": 9.0000015,
            "velocity": 0.6535433070866141
          },
          {
            "duration": 0.21428575000000016,
            "durationTicks": 240,
            "midi": 40,
            "name": "E2",
            "ticks": 10080,
            "time": 9.0000015,
            "velocity": 0.5039370078740157
          },
          {
            "duration": 0.21428575000000016,
            "durationTicks": 240,
            "midi": 52,
            "name": "E3",
            "ticks": 10320,
            "time": 9.21428725,
            "velocity": 0.5511811023622047
          },
          {
            "duration": 0.21428575000000016,
            "durationTicks": 240,
            "midi": 56,
            "name": "G#3",
            "ticks": 10560,
            "time": 9.428573,
            "velocity": 0.5984251968503937
          },
          {
            "duration": 0.21428575000000016,
            "durationTicks": 240,
            "midi": 64,
            "name": "E4",
            "ticks": 10800,
            "time": 9.64285875,
            "velocity": 0.5984251968503937
          },
          {
            "duration": 0.21428575000000016,
            "durationTicks": 240,
            "midi": 72,
            "name": "C5",
            "ticks": 11040,
            "time": 9.8571445,
            "velocity": 0.5984251968503937
          },
          {
            "duration": 0.21428575000000016,
            "durationTicks": 240,
            "midi": 71,
            "name": "B4",
            "ticks": 11280,
            "time": 10.07143025,
            "velocity": 0.5984251968503937
          },
          {
            "duration": 0.6428572499999987,
            "durationTicks": 720,
            "midi": 69,
            "name": "A4",
            "ticks": 11520,
            "time": 10.285716,
            "velocity": 0.6535433070866141
          },
          {
            "duration": 0.2142857499999984,
            "durationTicks": 240,
            "midi": 45,
            "name": "A2",
            "ticks": 11520,
            "time": 10.285716,
            "velocity": 0.5039370078740157
          },
          {
            "duration": 0.21428575000000016,
            "durationTicks": 240,
            "midi": 52,
            "name": "E3",
            "ticks": 11760,
            "time": 10.50000175,
            "velocity": 0.5511811023622047
          },
          {
            "duration": 0.21428575000000016,
            "durationTicks": 240,
            "midi": 57,
            "name": "A3",
            "ticks": 12000,
            "time": 10.7142875,
            "velocity": 0.5511811023622047
          },
          {
            "duration": 0.21428575000000016,
            "durationTicks": 240,
            "midi": 76,
            "name": "E5",
            "ticks": 12480,
            "time": 11.142859,
            "velocity": 0.5039370078740157
          },
          {
            "duration": 0.21428575000000016,
            "durationTicks": 240,
            "midi": 75,
            "name": "D#5",
            "ticks": 12720,
            "time": 11.35714475,
            "velocity": 0.5511811023622047
          },
          {
            "duration": 0.21428575000000016,
            "durationTicks": 240,
            "midi": 76,
            "name": "E5",
            "ticks": 12960,
            "time": 11.5714305,
            "velocity": 0.5511811023622047
          },
          {
            "duration": 0.21428575000000016,
            "durationTicks": 240,
            "midi": 75,
            "name": "D#5",
            "ticks": 13200,
            "time": 11.78571625,
            "velocity": 0.5039370078740157
          },
          {
            "duration": 0.21428575000000016,
            "durationTicks": 240,
            "midi": 76,
            "name": "E5",
            "ticks": 13440,
            "time": 12.000002,
            "velocity": 0.5984251968503937
          },
          {
            "duration": 0.21428575000000016,
            "durationTicks": 240,
            "midi": 71,
            "name": "B4",
            "ticks": 13680,
            "time": 12.21428775,
            "velocity": 0.5984251968503937
          },
          {
            "duration": 0.2142857499999984,
            "durationTicks": 240,
            "midi": 74,
            "name": "D5",
            "ticks": 13920,
            "time": 12.4285735,
            "velocity": 0.5984251968503937
          },
          {
            "duration": 0.21428575000000016,
            "durationTicks": 240,
            "midi": 72,
            "name": "C5",
            "ticks": 14160,
            "time": 12.642859249999999,
            "velocity": 0.5984251968503937
          },
          {
            "duration": 0.6428572500000005,
            "durationTicks": 720,
            "midi": 69,
            "name": "A4",
            "ticks": 14400,
            "time": 12.857145,
            "velocity": 0.5984251968503937
          },
          {
            "duration": 0.21428575000000016,
            "durationTicks": 240,
            "midi": 45,
            "name": "A2",
            "ticks": 14400,
            "time": 12.857145,
            "velocity": 0.5984251968503937
          },
          {
            "duration": 0.21428575000000016,
            "durationTicks": 240,
            "midi": 52,
            "name": "E3",
            "ticks": 14640,
            "time": 13.07143075,
            "velocity": 0.5984251968503937
          },
          {
            "duration": 0.21428575000000016,
            "durationTicks": 240,
            "midi": 57,
            "name": "A3",
            "ticks": 14880,
            "time": 13.2857165,
            "velocity": 0.5984251968503937
          }
]

# Play each MIDI note from the JSON data
for note in midi_data:
    frequency = midi_to_frequency(note["midi"])
    duration = note["duration"]
    velocity = note["velocity"]
    
    #playing the midi notes using our customized waves 
    wave_type = 'custom1'  
    print(f"Playing MIDI {note['midi']} -> {frequency:.2f} Hz, Duration: {duration:.3f}s, Velocity: {velocity}")
    
    buf = generate_waveform(frequency, wave_type)
    
    # Play the note
    start_time = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), start_time) < duration * 1000:
        nm = audio_out.write(buf)
        # print(nm)
    
    print(f"Finished playing MIDI {note['midi']}")

print("Finished all notes")
