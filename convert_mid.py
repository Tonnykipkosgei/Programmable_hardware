import mido
import json
from mido import MidiFile

NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def midi_note_to_name(midi):
    """Convert MIDI note number to note name."""
    octave = (midi // 12) - 1
    note = midi % 12
    return f"{NOTE_NAMES[note]}{octave}"

def midi_to_json(midi_file_path, json_file_path):
    midi = MidiFile(midi_file_path)
    midi_data = []

    ticks_per_beat = midi.ticks_per_beat
    tempo = 500000  # Default tempo in microseconds per beat (120 BPM)

    for track in midi.tracks:
        time_seconds = 0
        ticks = 0
        note_on_events = {}

        for msg in track:
            ticks += msg.time
            time_seconds += mido.tick2second(msg.time, ticks_per_beat, tempo)

            if msg.type == 'set_tempo':
                tempo = msg.tempo

            elif msg.type == 'note_on' and msg.velocity > 0:
                note_on_events[msg.note] = {
                    "ticks": ticks,
                    "time": time_seconds,
                    "velocity": msg.velocity / 127.0
                }

            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                if msg.note in note_on_events:
                    note_on_event = note_on_events.pop(msg.note)
                    duration_ticks = ticks - note_on_event["ticks"]
                    duration = time_seconds - note_on_event["time"]

                    note_data = {
                        "duration": duration,
                        "durationTicks": duration_ticks,
                        "midi": msg.note,
                        "name": midi_note_to_name(msg.note),
                        "ticks": note_on_event["ticks"],
                        "time": note_on_event["time"],
                        "velocity": note_on_event["velocity"]
                    }

                    midi_data.append(note_data)

    with open(json_file_path, 'w') as json_file:
        json.dump(midi_data, json_file, indent=4)

    print(f"JSON data written to {json_file_path}")

# Example usage:
midi_file_path = 'elise.mid'  # Replace with your MIDI file path
json_file_path = 'output.json'  # Replace with your desired output JSON file path

midi_to_json(midi_file_path, json_file_path)
