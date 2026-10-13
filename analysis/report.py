"""对比 ref / before / after 的每区域光流与网格方向，输出表格并画 flow-compare.png"""
import json, cv2, numpy as np
ref = json.load(open('ref_flow.json')); B = json.load(open('rep_flow_before.json')); A = json.load(open('rep_flow_after.json'))
rl = json.load(open('ref_lat.json')); bl = json.load(open('rep_lat.json')); al = json.load(open('rep_lat_after.json'))
ang = lambda a: (a + 180) % 360 - 180
rd = lambda L: next((v['deg'] for v in L if abs(v['deg']-172) < 30), float('nan'))  # 取接近水平的格点向量=字间方向
rows = ["| 区域 | 参考 光流 角度/幅值 | 修正前 角度误差 / 幅值误差 | 修正后 角度误差 / 幅值误差 | 文字行方向 参考 / 前 / 后 |", "|---|---|---|---|---|"]
for k in ref:
    r, b, a = ref[k], B[k], A[k]
    rows.append(f"| {k} | {r['deg']:.1f}° / {r['mag']:.2f} | {ang(b['deg']-r['deg']):+.1f}° / {100*(b['mag']/r['mag']-1):+.0f}% | {ang(a['deg']-r['deg']):+.1f}° / {100*(a['mag']/r['mag']-1):+.0f}% | {rd(rl[k]):.1f}° / {rd(bl[k]):.1f}° / {rd(al[k]):.1f}° |")
def summ(X, XL):
    e = [abs(ang(X[k]['deg']-ref[k]['deg'])) for k in ref]; m = [abs(X[k]['mag']/ref[k]['mag']-1)*100 for k in ref]
    rr = [abs(ang(rd(XL[k])-rd(rl[k]))) for k in ref]; rr = [x for x in rr if x == x]
    return f"光流角度平均误差 {np.mean(e):.2f}°（最大 {max(e):.1f}°），幅值平均误差 {np.mean(m):.1f}%，文字行方向平均误差 {np.mean(rr):.2f}°"
rows += ["", "- 修正前：" + summ(B, bl), "- 修正后：" + summ(A, al)]
open('flow_report.md', 'w').write("\n".join(rows) + "\n"); print("\n".join(rows))
# 箭头图：参考帧底图，绿=参考，红=修正前，青=修正后（箭头长度 ×40）
cap = cv2.VideoCapture('/workspace/motionface_3d_text.mp4'); cap.set(cv2.CAP_PROP_POS_FRAMES, 90); _, img = cap.read()
img = (img * 0.6).astype(np.uint8)
for i, yn in enumerate(["top","mid","bot"]):
    for j, xn in enumerate(["left","center","right"]):
        k = f"{yn}-{xn}"; c = (int((j*2+1)*1920/6), int((i*2+1)*1080/6))
        for X, col, w in [(ref,(80,255,80),7),(B,(60,60,255),3),(A,(255,255,0),3)]:
            e = (int(c[0] + X[k]['dx']*40), int(c[1] + X[k]['dy']*40)); cv2.arrowedLine(img, c, e, col, w, tipLength=0.15)
        cv2.putText(img, k, (c[0]-90, c[1]+40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
cv2.putText(img, "green=reference  red=replica BEFORE  cyan=replica AFTER  (arrow = flow x40 px/frame)", (30, 1050), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255), 2)
cv2.imwrite('../out/flow-compare.png', img); print("out/flow-compare.png")
