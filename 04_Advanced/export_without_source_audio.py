#!/usr/bin/env python3
"""Export video without its generated soundtrack. Requires ffmpeg and ffprobe.

With --music, use ONLY a separately reviewed instrumental mix (music and optional
non-vocal Foley). This does not detect voices in that replacement file and cannot
fix moving lips or reflections. It does not crop or stretch the picture.
"""
import argparse
import json
import subprocess
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('input', type=Path)
    p.add_argument('output', type=Path)
    p.add_argument('--music', type=Path, help='Separately approved instrumental mix; never the generated soundtrack')
    p.add_argument('--gain', type=float, default=1.0, help='Replacement mix gain; default 1.0')
    a = p.parse_args()
    src, dst = a.input.resolve(), a.output.resolve()
    if not src.is_file(): p.error('Input video does not exist.')
    if src == dst: p.error('Choose a new output file; do not overwrite the input.')
    if dst.exists(): p.error('Output already exists; choose a new name.')
    if dst.suffix.lower() != '.mp4': p.error('Output must end in .mp4.')
    if a.music and not a.music.is_file(): p.error('Replacement mix does not exist.')
    if not 0 <= a.gain <= 2: p.error('Gain must be between 0 and 2.')
    probe = subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(src)], check=True, capture_output=True, text=True)
    meta = json.loads(probe.stdout)
    video = next((s for s in meta['streams'] if s['codec_type'] == 'video' and not s.get('disposition', {}).get('attached_pic')), None)
    if video is None: p.error('No video stream found.')
    duration = float(video.get('duration') or meta['format']['duration'])
    if duration <= 0: p.error('Input has no positive duration.')
    # Source video is selected explicitly; no input-0 audio stream can be mapped.
    cmd = ['ffmpeg', '-v', 'error', '-n', '-i', str(src)]
    if a.music:
        cmd += ['-stream_loop', '-1', '-i', str(a.music.resolve())]
    cmd += ['-map', '0:' + str(video['index']), '-c:v', 'copy', '-map_metadata', '-1', '-map_chapters', '-1']
    if a.music:
        cmd += ['-map', '1:a:0', '-c:a', 'aac', '-b:a', '192k', '-af', 'volume=' + str(a.gain)]
    else:
        cmd += ['-an']
    cmd += ['-t', str(duration), '-sn', '-dn', '-movflags', '+faststart', str(dst)]
    dst.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(cmd, check=True)
    check = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-of', 'json', str(dst)], check=True, capture_output=True, text=True).stdout)
    audio_count = sum(s['codec_type'] == 'audio' for s in check['streams'])
    if audio_count != (1 if a.music else 0): raise RuntimeError('Unexpected output audio stream count.')
    print(json.dumps({'output': str(dst), 'source_audio_included': False, 'replacement_mix': bool(a.music), 'audio_streams': audio_count, 'width': video['width'], 'height': video['height'], 'exact_9_16': video['width'] * 16 == video['height'] * 9, 'visual_quality_checked': False}, indent=2))


if __name__ == '__main__':
    main()
