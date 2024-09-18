import os
import wave
import argparse
from mutagen.wave import WAVE

def check_wav_metadata(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".wav"):
                file_path = os.path.join(root, file)
                try:
                    # 使用 wave 模块打开 WAV 文件
                    with wave.open(file_path, 'r') as wav_file:
                        params = wav_file.getparams()
                        print(f"Checking {file}:")
                        print(f"  Channels: {params.nchannels}")
                        print(f"  Sample width: {params.sampwidth}")
                        print(f"  Frame rate: {params.framerate}")
                        print(f"  Number of frames: {params.nframes}")

                    # 使用 mutagen 检查 WAV 文件的元数据
                    wav_metadata = WAVE(file_path)
                    if wav_metadata.tags:
                        print(f"  Metadata found: {wav_metadata.tags}")
                    else:
                        print("  No metadata found.")
                except wave.Error as e:
                    print(f"Could not process {file}: {e}")
                except Exception as e:
                    print(f"An error occurred with {file}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check WAV files for metadata.")
    parser.add_argument("directory", type=str, help="The directory to check for WAV files.")

    args = parser.parse_args()
    check_wav_metadata(args.directory)
