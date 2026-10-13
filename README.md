# 炫酷3D透视文字背景 · Remotion 复刻（学习用）

**原作**：[QC2168](https://motionface.cc/?recording=b5668c83-b03f-4855-8db9-3c5f74e66220) 在 Motion Face 发布的动效片段「炫酷3D透视文字背景」（标签：文字排版）。创意和画面归原作者 QC2168 所有。本仓库只是为了学习而做的逆向复刻，参数都是对照参考视频拟合出来的，不是原工程源码。

## 规格
1920×1080，30 fps，180 帧，6 秒，无音轨，和参考视频一致（用 ffprobe 实测）。分析过程见 [TREATMENT.md](TREATMENT.md)。

## 运行
```bash
export COREPACK_HOME=$HOME/.cache/corepack   # 如果 corepack 缓存目录没有写权限
pnpm install --registry=https://registry.npmmirror.com
pnpm dev                 # Remotion Studio 预览
pnpm run render          # → out/replica.mp4（h264，无音轨）
bash scripts/qa.sh       # 确定性检查：同一帧渲两次逐字节比较，并扫描源码里的 random/Date/CSS 动画
bash scripts/compare.sh /path/to/reference.mp4   # → out/compare.png（上参考、下复刻，0/1/2/3/4/5.97 秒）和 out/compare.mp4（左右并排）
```
参考视频不随项目提供，请自己从原作页面获取。

## 结构
- `src/params.js`：所有可调参数，包括字、颜色、字号、行列间距、三轴旋转、透视、每个循环滚动的行数
- `src/Text3D.jsx`：文字网格放进 CSS 3D 平面（`preserve-3d` 加 `perspective`），`top` 偏移只由 `frame` 计算
- `src/index.jsx`：注册 Composition `Text3D`

## 怎么拟合的
1. 用 ffmpeg 抽关键帧，再用 numpy 相位相关法逐帧测参考视频的位移，结论是全程匀速上移，中心约 3 px/帧。
2. 渲染静帧，和参考帧比较各局部块的 FFT 幅度谱（对平移不敏感），然后随机爬山调旋转、透视、字号和间距。
3. 肉眼并排看，再手动修行列间距和亮度。

## v2：按光流重新拟合（针对反馈“文字流动角度有偏差”）
- `analysis/flow.py`：用 Farneback 光流测 3×3 区域的运动方向和幅值。`analysis/lattice.py`：用自相关测文字网格的字间方向和行步进。
- `analysis/model.py`：CSS 3D 投影的解析模型，和 Text3D.jsx 一致。先用它预测 v1 的光流，与实测相差不到 0.7°，说明模型可靠。`analysis/fit.py` 再用最小二乘拟合旋转、透视、平面内滚动向量和行距。
- 平面内的滚动方向偏离列轴约 2.5°，用每行水平错位 `rowStagger` 实现，同时保持无缝循环。
- 修正前后每个区域的误差见 `analysis/flow_report.md`，箭头对比图见 `out/flow-compare.png`。
- 复现：`cd analysis && python3 flow.py <参考视频> ref_flow.json && python3 lattice.py <参考视频> 90 > ref_lat.json && python3 fit.py`（依赖 opencv-python-headless、scipy）
