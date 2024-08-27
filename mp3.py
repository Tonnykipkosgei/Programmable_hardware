from machine import I2S, Pin, PWM
import time
import struct

# Setup PWM for I2S master clock
pwm = PWM(Pin(0), freq=11289600, duty_u16=32768)

buflen = 2000  # Buffer length for I2S interface

# Initialize I2S with a placeholder rate (will be updated later)
audio_out = I2S(0,
                sck=Pin(21),
                ws=Pin(22),
                sd=Pin(23),
                mode=I2S.TX,
                bits=16,
                format=I2S.MONO,
                rate=22300,  # Placeholder rate
                ibuf=buflen)

def read_wav_header(filename):
    with open(filename, 'rb') as f:
        header = f.read(44)
        if header[:4] != b'RIFF' or header[8:12] != b'WAVE':
            raise ValueError("Invalid WAV file")

        audio_format, num_channels, sample_rate, byte_rate, block_align, bits_per_sample = struct.unpack('<HHIIHH', header[20:36])

        print(f"Audio Format: {audio_format}, Channels: {num_channels}, Sample Rate: {sample_rate}, Bits per Sample: {bits_per_sample}")

        if audio_format != 1 or bits_per_sample != 16 or num_channels != 1:
            raise ValueError("Unsupported WAV format (only PCM 16-bit mono supported)")

    return sample_rate

def play_wav(filename, sample_rate):
    global audio_out
    audio_out.deinit()
    audio_out = I2S(0,
                    sck=Pin(21),
                    ws=Pin(22),
                    sd=Pin(23),
                    mode=I2S.TX,
                    bits=16,
                    format=I2S.MONO,
                    rate=sample_rate,
                    ibuf=buflen)

    print("Starting playback...")
    start_time = time.ticks_ms()

    with open(filename, 'rb') as f:
        f.seek(44)  # Skip WAV header

        while True:
            chunk = f.read(buflen)
            if not chunk:
                break

            # Write the 16-bit chunk directly to the I2S interface
            audio_out.write(chunk)

    print(f"Playback finished in {time.ticks_diff(time.ticks_ms(), start_time)} ms")
    audio_out.deinit()

# Play WAV file
filename = '/CantinaBand3.wav'  # Your WAV file path
sample_rate = read_wav_header(filename)
play_wav(filename, sample_rate)
