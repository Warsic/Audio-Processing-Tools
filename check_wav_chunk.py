import os
import wave
import struct
import argparse

def check_wav_chunks(file_path):
    try:
        with open(file_path, 'rb') as f:
            # 读取RIFF头
            riff_header = f.read(12)
            if len(riff_header) != 12 or riff_header[:4] != b'RIFF' or riff_header[8:] != b'WAVE':
                print(f"{file_path} is not a valid WAV file.")
                return

            chunks = []
            while True:
                chunk_header = f.read(8)
                if len(chunk_header) < 8:
                    break

                chunk_id = chunk_header[:4].decode('ascii', errors='replace')
                chunk_size = struct.unpack('<I', chunk_header[4:])[0]
                chunks.append((chunk_id, chunk_size))

                # 跳过当前块内容，移动到下一个块
                f.seek(chunk_size, 1)

            # 输出所有非 fmt 和 data 的块
            other_chunks = [chunk for chunk in chunks if chunk[0] not in ['fmt ', 'data']]
            if other_chunks:
                print(f"{file_path} contains the following non-fmt/data chunks:")
                for chunk_id, chunk_size in other_chunks:
                    print(f"  Chunk ID: {chunk_id}, Size: {chunk_size} bytes")
            else:
                print(f"{file_path} contains only fmt and data chunks.")
    
    except Exception as e:
        print(f"An error occurred with {file_path}: {e}")

def check_wav_metadata(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".wav"):
                file_path = os.path.join(root, file)
                print(f"Checking {file_path}:")
                check_wav_chunks(file_path)
                print("")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check WAV files for non-fmt/data chunks.")
    parser.add_argument("directory", type=str, help="The directory to check for WAV files.")

    args = parser.parse_args()
    check_wav_metadata(args.directory)
