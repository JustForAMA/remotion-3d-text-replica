// 所有可调参数集中在这里（对照参考视频手工拟合）
export const P = {
  text: "@DIV",
  color: "#5c5c5c",
  bg: "#000000",
  fontSize: 70,          // 平面坐标系下的字号(px)
  fontWeight: 700,
  fontFamily: "Arial, Helvetica, 'Liberation Sans', sans-serif",
  colGap: 240,           // 列间距（平面坐标）
  rowPitch: 77,          // 行间距（平面坐标）
  rows: 70, cols: 30,
  perspective: 1950,
  rotateX: 28, rotateY: -3, rotateZ: -10,
  originX: 960, originY: 540,
  planeOffsetX: -1500, planeOffsetY: -2300,
  rowsPerLoop: 7,        // 6 秒内平面滚动的行数（整数 → 无缝循环）
};
