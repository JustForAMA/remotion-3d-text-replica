// 所有可调参数集中在这里。
// 相机（旋转/透视）与滚动向量由 analysis/fit.py 对参考视频的光流 + 文字网格方向做最小二乘拟合得到；
// 字号、列距按行距同比缩放（目测校准）。
export const P = {
  text: "@DIV",
  color: "#5c5c5c",
  bg: "#000000",
  fontSize: 77,          // 平面坐标系下的字号(px)
  fontWeight: 700,
  fontFamily: "Arial, Helvetica, 'Liberation Sans', sans-serif",
  colGap: 264,           // 列间距（平面坐标）
  rowPitch: 85,          // 行间距（拟合 84.1）
  rowStagger: 3.7,       // 每行水平错位：使“滚动方向”偏离列轴约 2.5°（拟合）
  rows: 70, cols: 30,
  perspective: 2325,
  rotateX: 32.9, rotateY: -1.3, rotateZ: -7.2,
  originX: 960, originY: 540,
  planeOffsetX: -1500, planeOffsetY: -2300,
  rowsPerLoop: 8,        // 6 秒内沿“错位列”滚动 8 行（格点向量 → 无缝循环）
};
