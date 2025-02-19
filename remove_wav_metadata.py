import os
import wave
import shutil
import struct
import argparse

# 读取并移除其他块，只保留 fmt 和 data 块
def remove_other_chunks(wav_path, output_path):
    with open(wav_path, 'rb') as f:
        # 读取 RIFF 头
        riff_header = f.read(4)
        if riff_header != b'RIFF':
            raise ValueError(f"文件 {wav_path} 不是有效的 WAV 文件。")
        
        # 跳过文件大小字段（4字节）
        f.read(4)
        
        # 读取 WAV 格式标识符
        format = f.read(4)
        if format != b'WAVE':
            raise ValueError(f"文件 {wav_path} 不是有效的 WAV 文件。")

        # 创建输出文件
        with open(output_path, 'wb') as out_f:
            # 写入 RIFF 头和格式标识
            out_f.write(riff_header)
            out_f.write(struct.pack('<I', 36))  # 文件大小字段，先假设文件大小为 36 (稍后更新)
            out_f.write(format)
            
            # 读取每个块
            fmt_chunk = None
            data_chunk = None
            while True:
                chunk_id = f.read(4)
                if not chunk_id:
                    break  # 文件结束
                chunk_size_data = f.read(4)
                if len(chunk_size_data) < 4:
                    raise ValueError(f"读取块大小时遇到文件结尾，文件 {wav_path} 可能损坏。")
                chunk_size = struct.unpack('<I', chunk_size_data)[0]

                # 检查是否需要保留块
                if chunk_id == b'fmt ':
                    fmt_chunk = f.read(chunk_size)
                elif chunk_id == b'data':
                    data_chunk = f.read(chunk_size)
                else:
                    # 跳过其他块
                    f.read(chunk_size)
            
            if fmt_chunk is None or data_chunk is None:
                raise ValueError(f"文件 {wav_path} 缺少 fmt 或 data 块。")
            
            # 写入 fmt 和 data 块
            out_f.write(b'fmt ')
            out_f.write(struct.pack('<I', len(fmt_chunk)))
            out_f.write(fmt_chunk)
            
            out_f.write(b'data')
            out_f.write(struct.pack('<I', len(data_chunk)))
            out_f.write(data_chunk)
            
            # 更新文件大小字段
            file_size = os.path.getsize(output_path) - 8  # 8 字节是 RIFF 头（不包括文件大小）
            out_f.seek(4)
            out_f.write(struct.pack('<I', file_size))
            
            print(f"成功保存 {output_path}")

# 主程序
def process_directory(input_dir, output_dir):
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    for filename in os.listdir(input_dir):
        if filename.endswith(".wav"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            
            try:
                remove_other_chunks(input_path, output_path)
            except Exception as e:
                print(f"处理文件 {filename} 时发生错误: {e}")

if __name__ == "__main__":
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description="移除 WAV 文件中所有除 fmt 和 data 块外的数据，并保存到指定目录")
    parser.add_argument("input_dir", help="包含 WAV 文件的目录路径")
    parser.add_argument("output_dir", help="保存修改后 WAV 文件的目录路径")
    
    # 获取传入的目录路径
    args = parser.parse_args()
    
    # 处理目录
    process_directory(args.input_dir, args.output_dir)
