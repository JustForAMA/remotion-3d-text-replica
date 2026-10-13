"""测量视频运动场：Farneback 光流，3x3 区域中位数，输出每区域的方向(度,屏幕坐标:0=右,90=下)与幅值(px/帧)。
用法：python3 flow.py video.mp4 out.json"""
import sys, json, cv2, numpy as np
cap = cv2.VideoCapture(sys.argv[1]); frames = []
while True:
    ok, f = cap.read()
    if not ok: break
    frames.append(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY))
H, W = frames[0].shape
acc = {}
for f in range(3, len(frames) - 1, 6):
    fl = cv2.calcOpticalFlowFarneback(frames[f], frames[f+1], None, 0.5, 4, 31, 5, 7, 1.5, 0)
    for i, yn in enumerate(["top", "mid", "bot"]):
        for j, xn in enumerate(["left", "center", "right"]):
            y0, x0 = int((i*2+1)*H/6), int((j*2+1)*W/6)
            blk = fl[y0-90:y0+90, x0-150:x0+150].reshape(-1, 2)
            acc.setdefault(f"{yn}-{xn}", []).append(np.median(blk, axis=0))
out = {}
for k, v in acc.items():
    dx, dy = np.median(np.array(v), axis=0)
    out[k] = {"dx": round(float(dx), 3), "dy": round(float(dy), 3),
              "deg": round(float(np.degrees(np.arctan2(dy, dx))), 1), "mag": round(float(np.hypot(dx, dy)), 3)}
json.dump(out, open(sys.argv[2], "w"), indent=1, ensure_ascii=False)
for k, v in out.items(): print(f"{k:14s} deg={v['deg']:7.1f} mag={v['mag']:.2f}")
