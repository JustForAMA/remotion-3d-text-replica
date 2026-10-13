import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { P as P0 } from "./params.js";

// 画面 = f(frame)：只用帧号算滚动量，无 random / Date / CSS 动画
export const Text3D = (props) => {
  const P = { ...P0, ...props };
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const k = (frame / durationInFrames) * P.rowsPerLoop; // 已滚动的行数（线性匀速）
  const scrollY = k * P.rowPitch, scrollX = k * P.rowStagger; // 沿错位列方向滚动
  const rows = [];
  for (let r = 0; r < P.rows; r++) {
    const cells = [];
    for (let c = 0; c < P.cols; c++) {
      cells.push(
        <span key={c} style={{ position: "absolute", left: c * P.colGap, top: 0 }}>{P.text}</span>
      );
    }
    rows.push(<div key={r} style={{ position: "absolute", left: r * P.rowStagger, top: r * P.rowPitch }}>{cells}</div>);
  }
  return (
    <AbsoluteFill style={{ backgroundColor: P.bg, perspective: P.perspective, perspectiveOrigin: `${P.originX}px ${P.originY}px`, overflow: "hidden" }}>
      <div style={{
        position: "absolute", left: 960, top: 540, width: 0, height: 0,
        transformStyle: "preserve-3d",
        transform: `rotateX(${P.rotateX}deg) rotateY(${P.rotateY}deg) rotateZ(${P.rotateZ}deg)`,
      }}>
        <div style={{
          position: "absolute", left: P.planeOffsetX - scrollX, top: P.planeOffsetY - scrollY,
          color: P.color, fontFamily: P.fontFamily, fontWeight: P.fontWeight, fontSize: P.fontSize,
          lineHeight: 1, whiteSpace: "nowrap",
        }}>{rows}</div>
      </div>
    </AbsoluteFill>
  );
};
