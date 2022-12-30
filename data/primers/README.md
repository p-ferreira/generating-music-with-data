# Primers

This folder contains the primers used for some experiments, both in MIDI and in textual representation.

You can find the MIDI extracts in the `midi` folder, which includes the first seconds of the following musical pieces:

- `c_major_arpeggio.mid`: Arpeggio in C major 
- `c_major_scale.mid`: C major scale
- `clair_de_lune.mid`: First 7 seconds of Clair de Lune by Claude Debussy
- `fur_elise.mid`: First 3 seconds of Fur Elise by Ludwig van Beethoven
- `moonlight_sonata.mid`: First 5 seconds of Moonlight Sonata by Ludwig van Beethoven
- `prelude_in_c_major.mid`: First 4 seconds of Prelude in C major by Johann Sebastian Bach


One can also find the textual representation of the primer MIDI files in the [primers_token_sequences.json](./tokens/primers_token_sequences.json) file,
located at the [tokens](./tokens) folder. 
The textual representation is the output of the pipeline developed for the end-to-end approach, described in the paper. 
The implementation of the pipeline can be found in the file 
[make_token_sequence_dataset.py](../../src/data/make_token_sequence_dataset.py).

Bellow an example of the textual representation of the first 5 events of Clair de lune:
```json
{
  "clair_de_lune.mid": "piece_start time_shift=8 velocity=13 note_on=65 note_on=68..."
}
```