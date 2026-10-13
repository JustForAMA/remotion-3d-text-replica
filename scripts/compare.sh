#!/bin/bash
# 用法：bash scripts/compare.sh /path/to/reference.mp4
# 产出 out/compare.png（上：参考，下：复刻，同一时刻）和 out/compare.mp4（左右并排）
set -e
REF=${1:-../../motionface_3d_text.mp4}
cd "$(dirname "$0")/.."
SEL="select='eq(n\,0)+eq(n\,30)+eq(n\,60)+eq(n\,90)+eq(n\,120)+eq(n\,179)',scale=480:-1,tile=6x1"
ffmpeg -y -loglevel error -i "$REF" -vf "$SEL" -vsync 0 -frames:v 1 out/_ref.png
ffmpeg -y -loglevel error -i out/replica.mp4 -vf "$SEL" -vsync 0 -frames:v 1 out/_rep.png
ffmpeg -y -loglevel error -i out/_ref.png -i out/_rep.png -filter_complex vstack out/compare.png
ffmpeg -y -loglevel error -i "$REF" -i out/replica.mp4 -filter_complex "[0]scale=960:-2[a];[1]scale=960:-2[b];[a][b]hstack" -c:v libx264 -crf 23 -pix_fmt yuv420p -an out/compare.mp4
rm out/_ref.png out/_rep.png
echo "out/compare.png out/compare.mp4"
