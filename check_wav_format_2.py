import os
import soundfile as sf
import argparse

def get_wav_info(file_path):
    try:
        with sf.SoundFile(file_path) as wav_file:
            channels = wav_file.channels  # 声道数
            sample_rate = wav_file.samplerate  # 采样率
            sample_width = wav_file.subtype  # 数据格式（例如浮点型）
            return channels, sample_width, sample_rate
    except Exception as e:
        print(f"无法读取文件 {file_path}: {e}")
        return None

def print_wav_info(directory):
    # 遍历目录中的所有文件
    for filename in os.listdir(directory):
        if filename.endswith(".wav"):
            file_path = os.path.join(directory, filename)
            result = get_wav_info(file_path)
            if result:
                channels, sample_width, sample_rate = result
                # 打印文件信息
                print(f"文件: {filename}")
                print(f"  采样率: {sample_rate} Hz")
                print(f"  声道数: {channels}")
                print(f"  数据格式: {sample_width}")
                print("=" * 40)

if __name__ == "__main__":
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description="输出指定目录中所有 wav 文件的采样率、位深度和声道数")
    parser.add_argument("directory", help="目标目录路径")
    
    # 获取传入的目录路径
    args = parser.parse_args()
    
    # 调用打印信息的函数
    print_wav_info(args.directory)
