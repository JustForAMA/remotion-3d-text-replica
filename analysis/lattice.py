"""测量静态文字网格：每区域 FFT 自相关找最近的两个格点向量（行内相邻词 & 相邻行）。用法：python3 lattice.py video.mp4 frame"""
import sys, cv2, numpy as np, json
cap = cv2.VideoCapture(sys.argv[1]); cap.set(cv2.CAP_PROP_POS_FRAMES, int(sys.argv[2])); ok, f = cap.read()
g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY).astype(float); H, W = g.shape; out = {}
for i, yn in enumerate(["top", "mid", "bot"]):
    for j, xn in enumerate(["left", "center", "right"]):
        y0, x0 = int((i*2+1)*H/6), int((j*2+1)*W/6)
        a = g[y0-170:y0+170, x0-300:x0+300]; a = a - a.mean()
        F = np.fft.fft2(a); ac = np.fft.fftshift(np.fft.ifft2(np.abs(F)**2).real); ac /= ac.max()
        yy, xx = np.mgrid[-170:170, -300:300]; r = np.hypot(yy, xx)
        m = ac.copy(); m[r < 35] = -1
        # 局部极大
        loc = (m == cv2.dilate(m, np.ones((15, 15)))) & (m > 0.08) & (r < 165)
        pts = sorted([(r[p], yy[p], xx[p], m[p]) for p in zip(*np.nonzero(loc))])
        vecs = []
        for d, y, x, v in pts:
            if y < 0 or (y == 0 and x < 0): continue  # 半平面去对称
            if all(abs(x*vy - y*vx) > 0.25*d*np.hypot(vx, vy) for vx, vy in vecs):
                vecs.append((int(x), int(y)))
            if len(vecs) == 2: break
        out[f"{yn}-{xn}"] = [{"v": v, "deg": round(float(np.degrees(np.arctan2(v[1], v[0]))), 1), "len": round(float(np.hypot(*v)), 1)} for v in vecs]
print(json.dumps(out, ensure_ascii=False))
