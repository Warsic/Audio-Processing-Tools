import os
import pandas as pd
import argparse

def merge_excel_files(input_directory, output_file):
    # 存储所有文件的列数据
    all_data = []

    # 获取目录中所有的 .xlsx 文件
    file_list = [file for file in os.listdir(input_directory) if file.endswith('.xlsx')]

    if not file_list:
        print(f"目录 {input_directory} 中没有找到任何 .xlsx 文件")
        return

    # 读取每个文件并将列位置进行排列
    for file in file_list:
        file_path = os.path.join(input_directory, file)
        # 读取 Excel 文件
        df = pd.read_excel(file_path)
        all_data.append(df)

    # 获取最大列数
    max_columns = max([df.shape[1] for df in all_data])

    # 创建一个空的 DataFrame 来存储合并后的结果
    merged_df = pd.DataFrame()

    # 将每个文件的列根据位置相邻排列
    for i in range(max_columns):
        columns_to_merge = []
        for df in all_data:
            if i < df.shape[1]:  # 如果文件中有这一列
                columns_to_merge.append(df.iloc[:, i].reset_index(drop=True))
        # 将列横向合并
        merged_df = pd.concat([merged_df] + columns_to_merge, axis=1)

    # 将合并后的结果保存为新的 Excel 文件
    merged_df.to_excel(output_file, index=False)

    print(f'所有文件已成功合并并保存到 {output_file}')

if __name__ == "__main__":
    # 使用 argparse 处理命令行参数
    parser = argparse.ArgumentParser(description='合并目录中的所有 .xlsx 文件，并将相同列的位置相邻排列')
    parser.add_argument('input_directory', type=str, help='输入文件所在的目录路径')
    parser.add_argument('output_file', type=str, help='输出的文件路径')

    # 解析参数
    args = parser.parse_args()

    # 调用合并函数
    merge_excel_files(args.input_directory, args.output_file)
