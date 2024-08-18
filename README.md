# split_by_silence

A very simple python script to split an audio file by periods of silence

## Dependencies

- [pydub](https://github.com/jiaaro/pydub)
- [ffmpeg](http://www.ffmpeg.org/) or [libav](http://libav.org/)

## Installing

- Run install.sh from the root directory of the project
- Ensure that ~/.local/bin is in your PATH

See: [installing ffmpeg](https://github.com/jiaaro/pydub?tab=readme-ov-file#getting-ffmpeg-set-up)

## Usage

```
main.py [-h] [--start START] [--end END] [--silence_thresh SILENCE_THRESH] [--min_silence_len MIN_SILENCE_LEN] [--keep_silence KEEP_SILENCE] [--verbose] audio_file output_folder
```

Split audio file into sentences based on silence.

positional arguments:

  - `audio_file`            Path to the input audio file.
  - `output_folder`         Folder to save the output audio chunks.

options:

  - `-h`, `--help`          Show a help message and exit
  - `-s`, `--start START`         Start timestamp in HH:MM:SS format (default: 00:00:00).
  - `-e`, `--end END`             End timestamp in HH:MM:SS format (default: up to the end of the file).
  - `-t`, `--silence_thresh`      Silence threshold in dB (default: -40).
  - `-m`, `--min_silence_len`     Minimum silence length in ms (default: 500).
  - `-k`, `--keep_silence`        Duration of silence to keep at the start and end of each fragment in ms (default: 100)
  - `-d`, `--min_chunk_duration`  Filter out chunks shorter than this value in ms (default: 0)
