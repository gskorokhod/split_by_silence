import argparse
import os

from pydub import AudioSegment
from pydub.silence import detect_nonsilent


def to_ms(hh, mm, ss):
    return (hh * 3600 * 1000) + (mm * 60 * 1000) + (ss * 1000)


def to_hms(ms):
    total_seconds = ms // 1000

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    return (hours, minutes, seconds)


def format_timestamp(hh, mm, ss):
    if hh == 0:
        return f"{mm:02}:{ss:02}"

    return f"{hh:02}:{mm:02}:{ss:02}"


def split_audio_by_silence(
    audio_file,
    output_folder,
    start_timestamp=(0, 0, 0),
    end_timestamp=None,
    silence_thresh=-40,
    min_silence_len=500,
    keep_silence_ms=100,
    verbose=False,
):
    # Load the audio file
    audio = AudioSegment.from_file(audio_file)

    # Convert start and end timestamps to milliseconds
    start_ms = to_ms(*start_timestamp)

    if end_timestamp is None:
        end_ms = len(audio)
    else:
        end_ms = min(to_ms(*end_timestamp), len(audio))

    if verbose:
        print(
            f"Loaded audio file: '{audio_file}' ({format_timestamp(*to_hms(len(audio)))} h:m:s long)"
        )

    if start_ms >= len(audio):
        start_mmss = format_timestamp(*to_hms(start_ms))
        audio_len = format_timestamp(*to_hms(len(audio)))

        print(
            f"Start timestamp set to {start_mmss}, but the audio file is only {audio_len} h:m:s long"
        )

        exit(1)

    # Slice the audio to the desired range
    audio_segment = audio[start_ms:end_ms]

    if verbose:
        print("Detecting silence periods...")

    # Split the audio into chunks based on silence
    chunk_timestamps = detect_nonsilent(
        audio_segment, min_silence_len=min_silence_len, silence_thresh=silence_thresh
    )

    if verbose:
        print("Done!")

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    for i, (chunk_start_ms, chunk_end_ms) in enumerate(chunk_timestamps):
        chunk_start_ms = max(0, chunk_start_ms - keep_silence_ms)
        chunk_end_ms = min(len(audio_segment), chunk_end_ms + keep_silence_ms)

        chunk = audio_segment[chunk_start_ms:chunk_end_ms]

        start_h, start_m, start_s = to_hms(chunk_start_ms + start_ms)
        end_h, end_m, end_s = to_hms(chunk_end_ms + start_ms)

        start_ts = format_timestamp(start_h, start_m, start_s)
        end_ts = format_timestamp(end_h, end_m, end_s)

        filename = f"S{i + 1}_{start_ts}-{end_ts}.mp3"
        filepath = os.path.join(output_folder, filename)

        chunk.export(filepath, format="mp3")

        if verbose:
            print(f"Saved chunk: {filepath}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Split audio file into sentences based on silence."
    )
    parser.add_argument("audio_file", type=str, help="Path to the input audio file.")
    parser.add_argument(
        "output_folder", type=str, help="Folder to save the output audio chunks."
    )
    parser.add_argument(
        "--start",
        type=str,
        default="00:00:00",
        help="Start timestamp in HH:MM:SS format (default: 00:00:00).",
    )
    parser.add_argument(
        "--end",
        type=str,
        default="",
        help="End timestamp in HH:MM:SS format (default: up to the end of the file).",
    )
    parser.add_argument(
        "--silence_thresh",
        type=int,
        default=-40,
        help="Silence threshold in dB (default: -40).",
    )
    parser.add_argument(
        "--min_silence_len",
        type=int,
        default=500,
        help="Minimum silence length in ms (default: 500).",
    )
    parser.add_argument(
        "--keep_silence",
        type=int,
        default=100,
        help="Duration of silence to keep at the start and end of each fragment in ms (default: 100)",
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Print extra information"
    )

    args = parser.parse_args()

    # Convert start and end timestamps from MM:SS to tuples (minutes, seconds)
    start_timestamp = tuple(map(int, args.start.split(":")))

    if args.end == "":
        end_timestamp = None
    else:
        end_timestamp = tuple(map(int, args.end.split(":")))

    # Call the function to split the audio
    split_audio_by_silence(
        audio_file=args.audio_file,
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp,
        output_folder=args.output_folder,
        silence_thresh=args.silence_thresh,
        min_silence_len=args.min_silence_len,
        keep_silence_ms=args.keep_silence,
        verbose=args.verbose,
    )
