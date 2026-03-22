# Track Sorter

根据专辑歌单重命名音频文件并连接为全专单轨的 Python CLI 工具。

## 功能简介

Track Sorter 是一个命令行工具，用于：

1. **按歌单顺序重命名音频文件** - 根据提供的曲目列表，为音频文件添加序号前缀
2. **合并为单轨专辑** - 使用 FFmpeg 将所有曲目连接成一个完整的专辑音频文件
3. **支持多种音频格式** - 通过 FFmpeg 支持 FLAC、MP3、WAV 等常见格式

## 安装

本项目使用 `uv` 进行依赖管理：

```bash
# 克隆仓库
git clone <repository-url>
cd track-sorter

# 安装依赖
uv sync

# 安装开发依赖（可选）
uv sync --dev
```

## 使用方法

### 基本用法

```bash
# 使用默认设置（当前目录，tracklist.txt）
uv run track-sorter

# 指定音频目录和歌单文件
uv run track-sorter -d /path/to/audio -l tracklist.txt -o output.flac
```

### 命令行参数

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--audio-dir` | `-d` | 音频文件所在目录 | 当前目录 |
| `--tracklist` | `-l` | 歌单文件路径 | `tracklist.txt` |
| `--output-file` | `-o` | 输出文件路径 | `【目录名】 - Full Album.flac` |

### 完整示例

```bash
# 处理指定目录的音频文件
uv run track-sorter -d ~/Music/Album -l ~/Music/Album/tracklist.txt -o ~/Music/Album/full_album.flac
```

## 歌单文件格式

歌单文件是一个纯文本文件，每行一个曲目标题：

```
第一首歌曲
第二首歌曲
第三首歌曲
...
```

**核心特性：部分匹配**

脚本使用**开头匹配**模式，只需要歌单中的文字与文件名开头匹配即可。你可以：
- 使用完整曲名：`Intro` 匹配 `Intro.flac`
- 使用简称缩写：`I` 匹配 `Intro.flac`，`M` 匹配 `Main Song.flac`
- 只要缩写能唯一确定一个文件即可

**⚠️ 前缀匹配陷阱警告**

如果有多首歌曲共享相同前缀（如 `Hello.wav` 和 `Hello (Live).wav`），仅写 `Hello` 会导致匹配多个文件而报错。此时必须提供足够区分的前缀：

```
Hello.      ← 匹配 Hello.wav（注意末尾的点）
Hello （    ← 匹配 Hello (Live).wav（注意括号和空格）
```

或直接使用完整文件名。

**注意事项：**

- ⚠️ **确保音频文件没有编号前缀** - 本工具用于给**没有编号**的专辑添加编号
- 音频文件名必须以曲目标题为开头（支持部分匹配）
- 曲目名称不能重复
- 文件编码建议使用 UTF-8

### 示例

假设音频目录中有以下**无编号**的音频文件：
```
Intro.flac
Main Song.flac
Outro.flac
```

你可以使用完整曲名创建 `tracklist.txt`：
```
Intro
Main Song
Outro
```

也可以使用简称缩写（更快捷）：
```
I
M
O
```

运行后文件将被重命名为：
```
1 - Intro.flac
2 - Main Song.flac
3 - Outro.flac
```

并生成合并后的单轨文件：`Album - Full Album.flac`

## 依赖要求

- **Python** >= 3.13
- **FFmpeg** - 需要安装 FFmpeg 并添加到系统 PATH
- **Python 依赖包：**
  - `ffmpeg-python` >= 0.2.0
  - `returns` >= 0.26.0

### 安装 FFmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt-get install ffmpeg
```

**Windows:**
从 [FFmpeg 官网](https://ffmpeg.org/download.html) 下载并添加到 PATH。

## 项目结构

```
track-sorter/
├── src/
│   └── track_sorter/
│       ├── __init__.py      # 模块导出
│       ├── __main__.py      # 入口点
│       └── track_sorter.py  # 主实现
├── pyproject.toml           # 项目配置
├── uv.lock                  # 依赖锁定
└── README.md                # 本文档
```

## 开发

```bash
# 运行模块（开发调试）
uv run python -m track_sorter --help

# 构建包
uv build

# 安装到本地环境
uv pip install -e .
```

## 技术特点

- **函数式编程** - 使用 `returns` 库实现函数式错误处理
- **类型安全** - 完整的类型注解支持
- **跨平台** - 支持 Windows、macOS 和 Linux

## 许可证

MIT License
