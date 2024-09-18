import os
import random
import sys

def rename_files(directory):
    # 获取目录中的所有符合条件的 .wav 文件
    files = [f for f in os.listdir(directory) if f.endswith('.wav') and '-' in f]
    
    # 随机生成编号的列表，从1开始，且不超过文件数量
    random_numbers = list(range(1, len(files) + 1))
    random.shuffle(random_numbers)

    for i, filename in enumerate(files):
        # 拆分文件名为作者和作品名
        parts = filename.rsplit('-', 1)
        if len(parts) == 2:
            author, work = parts
            # 获取对应的随机编号
            random_number = str(random_numbers[i])
            # 生成新文件名
            new_filename = f"{random_number}-{work}"
            # 获取完整路径
            old_file = os.path.join(directory, filename)
            new_file = os.path.join(directory, new_filename)
            # 重命名文件
            os.rename(old_file, new_file)
            print(f"Renamed: {filename} -> {new_filename}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python rename_files.py <directory_path>")
    else:
        directory_path = sys.argv[1]
        rename_files(directory_path)
