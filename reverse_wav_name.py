import os
import glob
import sys

def rename_wav_files(directory):
    # 获取所有以“作者-歌名.wav”命名的文件
    wav_files = glob.glob(os.path.join(directory, "*.wav"))

    for file_path in wav_files:
        # 提取文件名和扩展名
        file_name = os.path.basename(file_path)
        file_name_without_extension, extension = os.path.splitext(file_name)

        # 判断文件名是否符合 "作者-歌名" 格式
        if '-' in file_name_without_extension:
            author, song = file_name_without_extension.split('-', 1)
            new_file_name = f"{song.strip()} - {author.strip()}{extension}"

            # 生成新文件路径
            new_file_path = os.path.join(directory, new_file_name)

            # 重命名文件
            os.rename(file_path, new_file_path)
            print(f"已重命名: {file_name} -> {new_file_name}")

if __name__ == "__main__":
    # 从命令行参数中获取目录路径
    if len(sys.argv) != 2:
        print("请提供目录路径作为参数.")
        sys.exit(1)

    directory = sys.argv[1]

    # 检查目录是否存在
    if not os.path.isdir(directory):
        print(f"错误: 目录 '{directory}' 不存在.")
        sys.exit(1)

    # 执行重命名操作
    rename_wav_files(directory)
