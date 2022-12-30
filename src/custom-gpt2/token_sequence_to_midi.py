import collections
import math
import re

import note_seq

from typing import List
from note_seq import constants
from note_seq.performance_lib import PerformanceEvent, Performance
from note_seq.protobuf import music_pb2

# Example file
TOKEN_SEQUENCE_FILE = "../../data/primers/tokens/primers_token_sequences.json"

MAX_MIDI_VELOCITY = 127
VELOCITY_BINS = 32
BIN_SIZE = int(math.ceil(MAX_MIDI_VELOCITY / VELOCITY_BINS))  # Ceil(127 / 32) = 4

STEPS_PER_SECOND = 100
SECONDS_PER_STEP = 1.0 / STEPS_PER_SECOND
INSTRUMENT = 0  # PIANO


def velocity_bin_to_velocity(velocity_bin):
    return 1 + (velocity_bin - 1) * BIN_SIZE


def add_note_to_sequence(sequence, note_pitch, pitch_start_step, current_step, pitch_velocity):
    note = sequence.notes.add()
    note.start_time = pitch_start_step * SECONDS_PER_STEP
    note.end_time = current_step * SECONDS_PER_STEP

    note.pitch = note_pitch
    note.velocity = pitch_velocity
    note.instrument = INSTRUMENT

    if note.end_time > sequence.total_time:
        sequence.total_time = note.end_time

    return sequence


def extract_performance_event_from_token(token):
    if '=' in token:
        event_type, str_value = token.split('=')
        value = int(str_value)

        if event_type == "note_on":
            return PerformanceEvent(event_type=PerformanceEvent.NOTE_ON, event_value=value)
        elif event_type == "note_off":
            return PerformanceEvent(event_type=PerformanceEvent.NOTE_OFF, event_value=value)
        elif event_type == "time_shift":
            return PerformanceEvent(event_type=PerformanceEvent.TIME_SHIFT, event_value=value)
        elif event_type == "velocity":
            return PerformanceEvent(event_type=PerformanceEvent.VELOCITY, event_value=value)
        else:
            raise Exception("Unknown event type: " + event_type)


# Simplified manual approach
def extract_sequence_from_performance_events(performance_event_list):
    current_step = 0
    velocity = 0
    pitch_start_steps_and_velocities = collections.defaultdict(list)

    sequence = music_pb2.NoteSequence()
    sequence.ticks_per_quarter = constants.STANDARD_PPQ

    for event in performance_event_list:
        if event.event_type == PerformanceEvent.TIME_SHIFT:
            current_step += event.event_value

        elif event.event_type == PerformanceEvent.VELOCITY:
            velocity = velocity_bin_to_velocity(event.event_value)

        elif event.event_type == PerformanceEvent.NOTE_ON:
            pitch_start_steps_and_velocities[event.event_value].append((current_step, velocity))

        elif event.event_type == PerformanceEvent.NOTE_OFF:
            pitch_start_step, pitch_velocity = pitch_start_steps_and_velocities[event.event_value][0]

            # Removes the retrieved elements (pitch_start_step, pitch_velocity) from the list
            pitch_start_steps_and_velocities[event.event_value] = (
                pitch_start_steps_and_velocities[event.event_value][1:])

            if current_step == pitch_start_step:
                print('Ignoring note with zero duration at step ' + current_step)
                continue

            sequence = add_note_to_sequence(
                sequence,
                event.event_value,
                pitch_start_step,
                current_step,
                pitch_velocity)
        else:
            raise Exception("Unknown event type: " + event.event_type)

    # There could be remaining pitches that were never ended. End them now and create notes.
    for pitch in pitch_start_steps_and_velocities:
        for pitch_start_step, pitch_velocity in pitch_start_steps_and_velocities[pitch]:

            if current_step == pitch_start_step:
                print('Ignoring note with zero duration at step ' + current_step)
                continue

            sequence = add_note_to_sequence(
                sequence,
                event.event_value,
                pitch_start_step,
                current_step,
                pitch_velocity)

    return sequence


# Original approach using note_seq default Performance library
def create_sequence_from_performance_events(events: List[PerformanceEvent]):
    performance = Performance(
        steps_per_second=STEPS_PER_SECOND,
        start_step=0,
        num_velocity_bins=VELOCITY_BINS,
        instrument=INSTRUMENT
    )

    for performance_event in events:
        performance.append(performance_event)

    sequence = performance.to_sequence(velocity=100, instrument=0, program=None)
    return sequence


def convert_token_sequence_to_notes_sequence(token_sequence):
    tokens = re.split(r'\s+', token_sequence)

    ignore_tokens = ['piece_start', 'piece_end']

    # Extract the performance events from the tokens.
    performance_list = [extract_performance_event_from_token(token) for token in tokens if token not in ignore_tokens]

    # Example of how to create a sequence using note_seq functionalities
    note_seq_sequence = create_sequence_from_performance_events(performance_list)

    return note_seq_sequence


def main():
    # Get the token sequence.
    # Example of how to create a sequence using note_seq functionalities
    token_sequence = open(TOKEN_SEQUENCE_FILE, "r").read()
    note_seq_sequence = convert_token_sequence_to_notes_sequence(token_sequence)
    note_seq.midi_io.note_sequence_to_midi_file(note_seq_sequence,
                                                "resources/midi/add_your_midi.mid")

    # Example of how to create a sequence using simplified manual approach
    # sequence = extract_sequence_from_performance_events(performance_list)
    # note_seq.midi_io.note_sequence_to_midi_file(sequence, "manual_sequence-test.mid")
    print('Token sequence to midi completed')


if __name__ == '__main__':
    main()
