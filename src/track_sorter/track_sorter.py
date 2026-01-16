import pathlib
import ffmpeg
from returns.result import Result, Failure, Success

def find_target(track: str, audio_dir: pathlib.Path) -> Result[pathlib.Path, str]:
    matched = [*filter(lambda x: x.name.startswith(track), audio_dir.iterdir())]
    if len(matched) > 1:
        return Failure(f"找到多个匹配的音频文件: {', '.join([x.name for x in matched])}")
    if len(matched) == 0:
        return Failure(f"未找到匹配的音频文件: {track}")
    print(f"找到匹配的音频文件：{track} = {matched[0].name}")
    return Success(matched[0])

def sort_tracks(tracklist: list[str], audio_dir: pathlib.Path) -> Result[list[pathlib.Path], str]:
    if len(set(tracklist)) != len(tracklist):
        return Failure("歌单中包含重复的曲目")

    index_digits = len(str(len(tracklist)))
    renaming_files: list[tuple[pathlib.Path, str]] = []
    for i, track in enumerate(tracklist, start=1):
        index = str(i).zfill(index_digits)
        target = find_target(track, audio_dir)
        if isinstance(target, Failure):
            print(f"错误：{target.failure()}")
            print("有错误发生，没有任何文件被重命名。")
            return Failure(target.failure())
        renaming_files.append((target.unwrap(), f"{index} - {target.unwrap().name}"))
    
    for target, new_name in renaming_files:
        print(f"{target.name} ==> {new_name}")
        try:
            target.rename(audio_dir / new_name)
        except Exception as e:
            print(f"错误：{e}；文件重命名中发生错误，请检查文件名情况。")
            return Failure(str(e))
    
    return Success([audio_dir / new_name for _, new_name in renaming_files])

def concat_tracks(tracklist: list[pathlib.Path], output_file: pathlib.Path) -> Result[None, str]:
    try:
        # 为每个输入文件明确选择音频流
        audio_streams = []
        for track in tracklist:
            input_file = ffmpeg.input(str(track.resolve()))
            # 明确选择第一个音频流
            audio_streams.append(input_file['a:0'])
        
        # 使用ffmpeg.concat连接所有音频流，并设置专辑名元数据
        (
            ffmpeg.concat(*audio_streams, v=0, a=1)
            .output(str(output_file.resolve()), metadata=f"title={output_file.stem}")
            .run()
        )
    except Exception as e:
        return Failure(str(e))
    return Success(None)

def cli():
    import argparse
    import pathlib

    parser = argparse.ArgumentParser(
        prog=__file__,
        description="根据专辑歌单重命名音频文件并连接为全专单轨"
    )
    parser.add_argument(
        "-d", "--audio-dir",
        type=pathlib.Path,
        help="音频文件所在目录，确保所有音频文件名都以其曲目标题为开头，默认当前目录",
        default=pathlib.Path.cwd()
    )
    parser.add_argument(
        "-l", "--tracklist",
        type=pathlib.Path,
        help="专辑歌单文件路径，每行一个曲目标题，默认为曲目目录下的“tracklist.txt”",
    )
    parser.add_argument(
        "-o", "--output-file",
        type=pathlib.Path,
        help="输出文件路径，将重命名后的音频文件连接为全专单轨，默认为“【目录名】 - Full Album.mp3”",
    )
    args = parser.parse_args()
    audio_dir = args.audio_dir
    tracklist = args.tracklist or (audio_dir / "tracklist.txt")
    output_file = args.output_file or (audio_dir / f"{audio_dir.name} - Full Album.flac")

    print(f"正在处理目录：{audio_dir}")
    print(f"正在使用歌单文件：{tracklist}")
    print(f"全专单轨将被连接到：{output_file}")

    try:
        with open(tracklist, "r", encoding="utf-8") as f:
            tracklist = f.read().strip().splitlines()
    except Exception as e:
        print(f"错误：{e}；无法读取专辑歌单文件，请检查文件路径和编码情况。")
        exit(1)

    sorted_tracks = sort_tracks(tracklist, audio_dir)
    if isinstance(sorted_tracks, Failure):
        print(f"排序文件时发生错误：{sorted_tracks.failure()}")
        exit(1)

    concat_result = concat_tracks(sorted_tracks.unwrap(), output_file)
    if isinstance(concat_result, Failure):
        print(f"连接文件时发生错误：{concat_result.failure()}")
        exit(1)

__all__ = [
    "find_target",
    "sort_tracks",
    "concat_tracks",
    "cli"
]