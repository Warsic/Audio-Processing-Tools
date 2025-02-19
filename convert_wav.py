import os
import soundfile as sf
import numpy as np
import librosa
import argparse

def convert_wav(input_path, output_path, target_rate, target_depth):
    try:
        # 读取音频文件，soundfile 默认会支持多声道
        data, samplerate = sf.read(input_path)
        
        # 重采样到目标采样率
        if samplerate != target_rate:
            #print(f"转换采样率: {samplerate} -> {target_rate}")
            # 使用 librosa 进行重采样，确保数据和声道数保持一致
            data = librosa.resample(data.T, orig_sr=samplerate, target_sr=target_rate).T  # 转置保证维度正确

        # 根据目标位深度转换数据格式
        if target_depth == 8:
            data = (data * 127).astype(np.int8)  # 8-bit PCM
            subtype = "PCM_U8"
        elif target_depth == 16:
            data = (data * 32767).astype(np.int16)  # 16-bit PCM
            subtype = "PCM_16"
        elif target_depth == 24:
            data = (data * 8388607).astype(np.int32)  # 24-bit PCM（需要 32-bit 存储）
            subtype = "PCM_24"
        elif target_depth == 32:
            data = (data * 2147483647).astype(np.int32)  # 32-bit PCM
            subtype = "PCM_32"
        else:
            print(f"不支持的位深度: {target_depth}，请使用 8、16、24 或 32")
            return
        
        # 写入转换后的 WAV 文件
        sf.write(output_path, data, target_rate, subtype=subtype)
        print(f"已转换并保存: {output_path}")

    except Exception as e:
        print(f"转换文件 {input_path} 时出错: {e}")

def convert_directory(input_directory, output_directory, target_rate, target_depth):
    # 确保输出目录存在
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # 遍历目录中的所有 .wav 文件
    for filename in os.listdir(input_directory):
        if filename.endswith(".wav"):
            input_path = os.path.join(input_directory, filename)
            output_path = os.path.join(output_directory, filename)
            
            # 转换并保存到目标目录
            convert_wav(input_path, output_path, target_rate, target_depth)

if __name__ == "__main__":
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description="转换目录中的 wav 文件到指定采样率和位深度")
    parser.add_argument("input_directory", help="输入目录路径")
    parser.add_argument("output_directory", help="输出目录路径")
    parser.add_argument("target_rate", type=int, help="目标采样率")
    parser.add_argument("target_depth", type=int, help="目标位深度（8, 16, 24, 32）")
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 运行转换函数
    convert_directory(args.input_directory, args.output_directory, args.target_rate, args.target_depth)
