#!/bin/bash
# 确定性检查：同一帧渲染两次，逐字节比较
set -e; cd "$(dirname "$0")/.."
for f in 0 90 179; do
  npx remotion still src/index.jsx Text3D out/qa_a.png --frame=$f >/dev/null
  npx remotion still src/index.jsx Text3D out/qa_b.png --frame=$f >/dev/null
  cmp -s out/qa_a.png out/qa_b.png && echo "✓ 帧 $f 两次一致" || { echo "✗ 帧 $f 不一致"; exit 1; }
done
grep -nE "Math\.random|Date\.now|transition|animation" src/*.jsx src/*.js && echo "⚠ 发现非确定性写法" || echo "✓ 源码无 random/Date/CSS 动画"
rm -f out/qa_a.png out/qa_b.png
