import json, numpy as np
from scipy.optimize import least_squares
from model import predict
rf = json.load(open('ref_flow.json')); rl = json.load(open('ref_lat.json'))
d = lambda v: np.degrees(np.arctan2(v[1], v[0]))
names = ["rx","ry","rz","P","vx","vy","sy"]
def unpack(x): p = dict(zip(names, x)); p["sx"] = 0; return p
def res(x):
    pr = predict(unpack(x)); r = []
    for k, v in pr.items():
        r += list((v["flow"] - [rf[k]["dx"], rf[k]["dy"]]) * 10)          # 光流误差(px/帧)×10
        a = d(-v["rowdir"]) - rl[k][0]["deg"]; r.append(((a+180)%360-180) * 1.0)  # 行方向(度)
        r.append((np.hypot(*v["step"]) - rl[k][1]["len"]) * 0.3)          # 行距(px)
    return np.array(r)
x0 = [28,-3,-10,1950,0,-3.0,77]
sol = least_squares(res, x0, bounds=([0,-40,-40,600,-5,-8,40],[70,40,40,6000,5,0,140]))
p = unpack(sol.x); print(json.dumps({k: round(float(v),3) for k,v in p.items()}))
json.dump({k: float(v) for k,v in p.items()}, open('fit_params.json','w'))
pr = predict(p)
for k, v in pr.items():
    print(k, 'flow %.1f° %.2f (ref %.1f° %.2f)  row %.1f (ref %.1f)  step %.1f (ref %.1f)' % (d(v['flow']), np.hypot(*v['flow']), rf[k]['deg'], rf[k]['mag'], d(-v['rowdir']), rl[k][0]['deg'], np.hypot(*v['step']), rl[k][1]['len']))
