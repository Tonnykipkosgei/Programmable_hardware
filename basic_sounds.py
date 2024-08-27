from machine import I2S, Pin, PWM
import math

def irqhandler(arg):
    print(arg)
    audio_out.write(buf)

# Generate master clock for the pmodi2s2 using PWM
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
                ibuf=buflen,
                )

def generate_triangle_wave(buffer, smlen):
    for i in range(0, smlen // 2):
        val = 2 * i
        buffer[2 * i] = val & 0xff
        buffer[(smlen - 1) - 2 * i] = val & 0xff
        buffer[2 * i + 1] = (val >> 8) & 0xff
        buffer[(smlen - 1) - 2 * i + 1] = (val >> 8) & 0xff

def generate_sine_wave(buffer, smlen):
    for i in range(smlen):
        val = int((math.sin(2 * math.pi * i / smlen) + 1) * 32767)
        buffer[2 * i] = val & 0xff
        buffer[2 * i + 1] = (val >> 8) & 0xff

def generate_square_wave(buffer, smlen):
    for i in range(smlen):
        val = 32767 if i < smlen // 2 else -32768
        buffer[2 * i] = val & 0xff
        buffer[2 * i + 1] = (val >> 8) & 0xff

def generate_sawtooth_wave(buffer, smlen):
    for i in range(smlen):
        val = int((i / smlen) * 65535) - 32768
        buffer[2 * i] = val & 0xff
        buffer[2 * i + 1] = (val >> 8) & 0xff

# Sample length, defines frequency, we can vary it and it generates different tones
smlen = 100 
buf = bytearray(2 * smlen)

# Different basic waveforms
generate_triangle_wave(buf, smlen)
#generate_sine_wave(buf, smlen)
#generate_square_wave(buf, smlen)
#generate_sawtooth_wave(buf, smlen)

print("start")
while True:
    nm = audio_out.write(buf)
    # print(nm)

print("should be non-blocking")
