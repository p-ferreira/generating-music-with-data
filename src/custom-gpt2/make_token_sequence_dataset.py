import os
import math
import copy
import note_seq
import json
from tqdm import tqdm
from typing import List
from note_seq import sequences_lib
from note_seq import constants
from note_seq.performance_lib import PerformanceEvent

# Constants
PRIMERS_PATH = 'data/primers/'

MAX_MIDI_VELOCITY = 127
RAW_TRAINING_DATA_DIR = 'data/interim/maestro/train/'
RAW_VALIDATION_DATA_DIR = 'data/interim/maestro/validation/'


TRAINING_DATA_OUTPUT_DIR = 'data/processed/train_data.txt'
VALIDATION_DATA_OUTPUT_DIR = 'data/processed/validation_data.txt'

# Data hyperparameters
MAX_SHIFTS_STEPS = 100  # maximum number of steps to shift time forward
VELOCITY_BINS = 32
BIN_SIZE = int(math.ceil(MAX_MIDI_VELOCITY / VELOCITY_BINS))  # Ceil(127 / 32) = 4

TRANSPOSITION_RANGE = (list(range(-6, 6)))
STRETCH_RANGE = [0.5, 0.75, 1.0, 1.25, 1.5]


def transpose(sequence, transposition):
    """Transposes a note sequence by the specified transposition."""
    transposed_sequence = copy.deepcopy(sequence)
    for note in transposed_sequence.notes:
        if not note.is_drum:
            note.pitch += transposition
            if note.pitch < constants.MIN_MIDI_PITCH or note.pitch > constants.MAX_MIDI_PITCH:
                print(f'Warning: note {note} out of range. Skipping sequence')
                return None
    return transposed_sequence


def augment_and_quantize_note_sequence(
       note_sequence,
       stretch_factors: List[float],
       transposition_factors: List[int]):
    augmented_sequences = []

    # Stretch sequences accordingly to the stretch factors
    stretched_sequences = \
        [sequences_lib.stretch_note_sequence(note_sequence, stretch_factor) for stretch_factor in stretch_factors]

    for transposition_factor in transposition_factors:
        for stretched_sequence in stretched_sequences:
            transposed_sequence = transpose(stretched_sequence, transposition_factor)
            quantized_transposed_sequence = sequences_lib.quantize_note_sequence_absolute(transposed_sequence, MAX_SHIFTS_STEPS)
            augmented_sequences.append(quantized_transposed_sequence)

    return augmented_sequences


def calculate_velocity_bin(velocity):
    return ((velocity - 1) // BIN_SIZE) + 1


# note event either note on or note off
def extract_timeshift_events(note_event, current_step: int) -> List[PerformanceEvent]:
    time_shift_events = []

    is_future_event = note_event > current_step

    # If note event is in the future
    if is_future_event:
        # Shift time forward from the current step to this event if bigger than MAX_SHIFTS_STEPS.
        # The reason for this is to limit the size of the tokens for the timeshift events
        # So instead of having a sparse set e.g. timeshift=112, timeshift=113, timeshift=114, ...
        # we limit the size to MAX_SHIFTS_STEPS, splitting for example timeshift=112 to (timeshift=100 timeshift=12)
        while note_event > current_step + MAX_SHIFTS_STEPS:
            # We need to move further than the maximum shift size.
            max_timeshift_event = PerformanceEvent(
                event_type=PerformanceEvent.TIME_SHIFT,
                event_value=MAX_SHIFTS_STEPS)

            time_shift_events.append(max_timeshift_event)
            current_step += MAX_SHIFTS_STEPS

        time_shift_from_current_step = int(note_event - current_step)

        time_shift_events.append(
            PerformanceEvent(
                event_type=PerformanceEvent.TIME_SHIFT,
                event_value=time_shift_from_current_step)
        )

    return time_shift_events


def extract_velocity_event(velocity_bin: int) -> PerformanceEvent:
    return PerformanceEvent(
        event_type=PerformanceEvent.VELOCITY,
        event_value=velocity_bin)


def extract_note_event(note_event_step, note_pitch, is_offset):
    # Add a performance event for this note on/off.
    event_type = (PerformanceEvent.NOTE_OFF if is_offset else PerformanceEvent.NOTE_ON)

    return PerformanceEvent(event_type=event_type, event_value=note_pitch)


# extract events from note sequence to text
def extract_performance_events(
        note_event_step,
        current_step,
        note_velocity_bin,
        current_velocity_bin: int,
        note_pitch: int,
        is_offset: bool):
    performance_events = []

    time_shift_events = extract_timeshift_events(note_event_step, current_step)
    performance_events += time_shift_events

    # Only adds a velocity event if it's a note_on event and
    # if its velocity bin is different from the current velocity bin
    if not is_offset and note_velocity_bin != current_velocity_bin:
        velocity_event = extract_velocity_event(note_velocity_bin)
        performance_events.append(velocity_event)

    note_event = extract_note_event(note_event_step, note_pitch, is_offset)

    performance_events.append(note_event)

    return performance_events


def process_note_sequence(quantized_notes) -> List[PerformanceEvent]:
    # Get all notes that start after step 0
    sorted_notes = sorted(quantized_notes.notes, key=lambda note: (note.start_time, note.pitch))

    # Sort all note start and end events by creating a tuple of (step, index, is_offset)
    onsets = [(note.quantized_start_step, idx, False) for idx, note in enumerate(sorted_notes)]
    offsets = [(note.quantized_end_step, idx, True) for idx, note in enumerate(sorted_notes)]
    note_events = sorted(onsets + offsets)

    all_performance_events: List[PerformanceEvent] = []
    current_step = 0
    current_velocity_bin = 0

    for event, idx, is_offset in note_events:
        ### Set arguments to process note event
        note_velocity = sorted_notes[idx].velocity
        note_velocity_bin = calculate_velocity_bin(note_velocity)

        note_pitch = sorted_notes[idx].pitch

        ### Process note event
        events = extract_performance_events(
            event,
            current_step,
            note_velocity_bin,
            current_velocity_bin,
            note_pitch,
            is_offset)

        all_performance_events += events

        ### Update state
        current_step = event

        # Updates velocity bin if it's different from the current one
        if not is_offset and note_velocity_bin != current_velocity_bin:
            current_velocity_bin = note_velocity_bin

    return all_performance_events


def extract_token_from_performance_event(performance_event: PerformanceEvent) -> str:
    if performance_event.event_type == PerformanceEvent.NOTE_ON:
        return 'note_on=' + str(performance_event.event_value)

    elif performance_event.event_type == PerformanceEvent.NOTE_OFF:
        return 'note_off=' + str(performance_event.event_value)

    elif performance_event.event_type == PerformanceEvent.TIME_SHIFT:
        return 'time_shift=' + str(performance_event.event_value)

    elif performance_event.event_type == PerformanceEvent.VELOCITY:
        return 'velocity=' + str(performance_event.event_value)

    else:
        raise ValueError('Unknown performance event type: %s' % performance_event.event_type)


def convert_performance_events_to_token_sequence(performance_events: List[PerformanceEvent]) -> str:
    tokens = []
    for performance_event in performance_events:
        token = extract_token_from_performance_event(performance_event)

        tokens.append(token)

    concatenated_tokens = ' '.join(tokens)

    return concatenated_tokens


def extract_tokens_from_note_sequence(note_sequence) -> str:
    # Example of how to generate a performance directly with note_seq
    # original_conversion_performance_events = Performance(note_sequence,
    #     start_step=0,
    #     num_velocity_bins=VELOCITY_BINS,
    #     instrument=0)

    performance_events = process_note_sequence(note_sequence)
    token_sequence = convert_performance_events_to_token_sequence(performance_events)
        
    # adds start and end token
    token_sequence = "piece_start " + token_sequence + " piece_end"

    return token_sequence


def process_midi_file(midi_file, augment=True, stretch_notes=True):
    notes = note_seq.midi_file_to_note_sequence(midi_file)
    sustained_notes = note_seq.apply_sustain_control_changes(notes)

    # Stretch [1] == no stretching
    stretch_notes_range = STRETCH_RANGE if stretch_notes else [1.0]

    # Transposition [0] == no transposition
    transposition_range = TRANSPOSITION_RANGE if augment else [0]

    augmented_sequences = augment_and_quantize_note_sequence(
        sustained_notes,
        stretch_notes_range,
        transposition_range
    )

    token_sequences = []
    for notes_sequence in augmented_sequences:
        token_sequence = extract_tokens_from_note_sequence(notes_sequence)
        token_sequences.append(token_sequence)

    return token_sequences

def create_dataset(raw_data_path: str, output_file: str):
    # create raw_data_path folder if it doesn't exist
    output_file_path = os.path.dirname(output_file)

    if not os.path.exists(output_file_path):
        os.mkdir(output_file_path)

    problematic_files = []

    # write text to file
    with open(output_file, 'a') as file:
        for root, dirnames, filenames in os.walk(raw_data_path):
            for filename in tqdm(filenames):
                try:
                    if filename.endswith(('.mid', '.midi')):
                        midi_file = os.path.join(root, filename)

                        # print('Processing midi:' + midi_file)
                        token_sequences = process_midi_file(midi_file)
                        joined_sequences = '\n'.join(token_sequences) + '\n'

                        file.write(joined_sequences)

                        # print(midi_file + ' processed successfully')

                except Exception as e:
                    error_message = 'Error processing file ' + midi_file + ': ' + str(e)
                    problematic_files.append(f'{midi_file} {error_message}')
                    print(error_message)
                    continue

    if problematic_files:
        with open('problematic_files.txt', 'a') as p_file:
            p_file.write(problematic_files.join('\n'))
    else:
        print('All files were successfully processed')

# Function to tokenize midi primers
def create_primer_token_sequences():
    primer_token_sequence_dict = {}

    # iterate over files in a directory
    for root, _, filenames in os.walk(f'{PRIMERS_PATH}/midi'):
        for filename in filenames:
            if filename.endswith(('.mid', '.midi')):
                file_path = os.path.join(root, filename)
                token_sequences = process_midi_file(file_path, augment=False, stretch_notes=False)
                # token_sequences should have only one element since we don't augment or stretch
                sequence = token_sequences[0]
                primer_token_sequence_dict[filename] = sequence

    # save dictionary into json file
    with open(f'{PRIMERS_PATH}/tokens/primers_token_sequences.json', 'w') as file:
        json.dump(primer_token_sequence_dict, file)

    print('Primer tokens created successfully')

def main():
    # Easy creation for debugging purposes
    # create_primer_token_sequences()

    print('Creating training dataset...')
    create_dataset(RAW_TRAINING_DATA_DIR, TRAINING_DATA_OUTPUT_DIR)

    print('Creating validation dataset...')
    create_dataset(RAW_VALIDATION_DATA_DIR, VALIDATION_DATA_OUTPUT_DIR)

    print('Token sequence created successfully')


if __name__ == '__main__':
    main()
