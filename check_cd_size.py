import os
import soundfile as sf
import argparse

# CD标准：16-bit, 44.1 kHz, 2 声道
cd_capacity_mb = 700  # 单个CD的容量 (MB)
cd_capacity_bytes = cd_capacity_mb * 1024 * 1024  # 转换为字节

def get_wav_file_size(file_path):
    try:
        # 读取音频文件的元数据
        data, samplerate = sf.read(file_path)
        
        # 获取文件的 subtype（即位深度）
        file_info = sf.info(file_path)
        file_subtype = file_info.subtype
        
        # 检查位深度：确保是 16-bit PCM
        if file_subtype != 'PCM_16':
            print(f"警告: 文件 {file_path} 不是 16-bit 位深度 (实际为 {file_subtype})")
        
        # 确保音频是标准的 CD 音质：44.1 kHz, 立体声
        if samplerate != 44100:
            print(f"警告: 文件 {file_path} 不是 44.1 kHz 采样率")
        
        # 假设音频是立体声，检查声道数
        if len(data.shape) > 1:
            num_channels = data.shape[1]
        else:
            num_channels = 1  # 单声道
        
        # 计算文件大小：样本数 × 声道数 × 每样本字节数 (16-bit -> 2字节)
        num_samples = data.shape[0]
        file_size_bytes = num_samples * num_channels * 2  # 每个样本2字节 (16-bit)
        
        return file_size_bytes
    
    except Exception as e:
        print(f"读取文件 {file_path} 时出错: {e}")
        return 0

def calculate_total_space(directory):
    total_size_bytes = 0
    for filename in os.listdir(directory):
        if filename.endswith(".wav"):
            file_path = os.path.join(directory, filename)
            file_size = get_wav_file_size(file_path)
            total_size_bytes += file_size
            print(f"{filename}: {file_size / (1024*1024):.2f} MB")
    
    return total_size_bytes

def calculate_cd_count(total_size_bytes):
    # 计算需要多少张CD
    num_cds = total_size_bytes / cd_capacity_bytes
    return num_cds

def main(input_directory):
    total_size_bytes = calculate_total_space(input_directory)
    
    total_size_mb = total_size_bytes / (1024 * 1024)
    print(f"\n总音频大小: {total_size_mb:.2f} MB")
    
    num_cds = calculate_cd_count(total_size_bytes)
    print(f"总共需要 {num_cds:.2f} 张 CD")

if __name__ == "__main__":
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description="统计目录内 WAV 文件刻录成 CD 需要的空间")
    parser.add_argument("input_directory", help="输入目录路径")
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 运行主函数
    main(args.input_directory)
