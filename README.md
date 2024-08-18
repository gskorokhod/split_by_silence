# split_by_silence

A very simple python script to split an audio file by periods of silence

## Output format

Chunks are saved as `.mp3` files in the chosen output folder.
Their filenames have the following format: `S<№ of chunk>_<start timestamp>_<end timestamp>`.
Timestamps are in the `hh:mm:ss` format. If the hours value is 0, it is omitted.

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

## Example

```
> split_by_silence -s "00:05:55" -e "00:12:55" -m 800 -k 400 -d 1200 -v audio.mp3 ./chunks
Loaded audio file: 'audio.mp3' (17:54 h:m:s long)
Detecting silence periods...
Done!
Skipping chunk [08:43 - 08:44] as it is too short (879ms < 1200ms)
Skipping chunk [10:55 - 10:56] as it is too short (860ms < 1200ms)
...
Saved chunk: ./chunks/S1_05:58-06:02.mp3
Saved chunk: ./chunks/S2_06:03-06:07.mp3
...
```
