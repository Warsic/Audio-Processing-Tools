# Audio-Processing-Tools
音频自动化处理工具合集

## rename_files.py
将目录中以“作者-作品名”命名的 wav 文件使用洗牌算法随机编号并重命名为“编号-作品名.wav”。

### 依赖
无

### 参数
- 输入目录路径

## reverse_wav_name.py
将目录中所有以“作者-作品名”命名的wav文件重命名为"作品名 - 作者.wav"。

### 依赖
无

### 参数
- 输入目录路径

## check_wav_chunk.py
检查目录中 wav 文件是否含有非 `fmt` 或 `data` 块。

### 依赖
无

### 参数
- **directory:** 输入目录路径

## check_wav_format.py
输出指定目录中所有 wav 文件的采样率、位深度和声道数。

### 依赖
无

### 参数
- **directory:** 输入目录路径

## check_wav_format_2.py
输出指定目录中所有 wav 文件的采样率、位深度和声道数，支持浮点位精度。

### 依赖
soundfile

### 参数
- **directory:** 输入目录路径

## check_wav_metadata.py
输出指定目录中所有 wav 文件中存在的元数据。

### 依赖
mutagen

### 参数
- **directory:** 输入目录路径

## remove_wav_metadata.py
移除指定目录中所有 wav 文件中所有除 `fmt` 和 `data` 块外的数据，并保存到指定目录。

### 依赖
无

### 参数
- **input_dir:** 输入目录路径
- **output_dir:** 输出目录路径

## convert_wav.py
转换指定目录中所有 wav 文件为指定采样率与位深度，并保存到指定目录。

### 依赖
soundfile numpy librosa

### 参数
- **input_directory:** 输入目录路径
- **output_directory:** 输出目录路径
- **target_rate:** 目标采样率
- **target_depth:** 目标位深度（8, 16, 24, 32）

## check_cd_size.py
统计目录内所有 wav 文件刻录成 CD 光盘需要的总空间及标准 CD 光盘（700MB）数量，目录中文件需符合 CD 格式（44100Hz，16bit）。

### 依赖
soundfile

### 参数
- **input_directory:** 输入目录路径

## merge_grades.py
合并目录中的所有 xlsx 文件，并将相同列的位置相邻排列。

### 依赖
pandas

### 参数
- **input_directory:** 输入目录路径
- **output_file:** 输出文件路径
