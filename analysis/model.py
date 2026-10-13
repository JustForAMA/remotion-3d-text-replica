"""CSS 3D 投影解析模型：与 Text3D.jsx 一致（perspective 于 (960,540)，平面先 rotateZ 再 rotateY 再 rotateX）。"""
import numpy as np
def R(rx, ry, rz):
    a, b, c = np.radians([rx, ry, rz])
    X = np.array([[1,0,0],[0,np.cos(a),-np.sin(a)],[0,np.sin(a),np.cos(a)]])
    Y = np.array([[np.cos(b),0,np.sin(b)],[0,1,0],[-np.sin(b),0,np.cos(b)]])
    Z = np.array([[np.cos(c),-np.sin(c),0],[np.sin(c),np.cos(c),0],[0,0,1]])
    return X @ Y @ Z
def proj(p, M, P):
    q = M @ np.array([p[0], p[1], 0.0]); s = P / (P - q[2]); return np.array([960 + q[0]*s, 540 + q[1]*s])
def plane_at(screen, M, P):
    # 解平面坐标，使投影=screen（牛顿迭代）
    u = np.array([screen[0]-960, screen[1]-540], float)
    for _ in range(30):
        f = proj(u, M, P) - screen
        J = np.stack([(proj(u+[1e-3,0],M,P)-proj(u,M,P))/1e-3, (proj(u+[0,1e-3],M,P)-proj(u,M,P))/1e-3], 1)
        u = u - np.linalg.solve(J, f)
    return u
REG = {f"{yn}-{xn}": ((j*2+1)*1920/6, (i*2+1)*1080/6) for i, yn in enumerate(["top","mid","bot"]) for j, xn in enumerate(["left","center","right"])}
def predict(p):
    """p: rx,ry,rz,P, scroll_dx, scroll_dy (平面 px/帧), rowstep (sx, sy) 平面行步进向量"""
    M = R(p["rx"], p["ry"], p["rz"]); out = {}
    for k, s in REG.items():
        u = plane_at(np.array(s), M, p["P"]); base = proj(u, M, p["P"])
        fl = proj(u + [p["vx"], p["vy"]], M, p["P"]) - base
        rowdir = proj(u + [1, 0], M, p["P"]) - base
        st = proj(u + [p["sx"], p["sy"]], M, p["P"]) - base
        out[k] = dict(flow=fl, rowdir=rowdir, step=st)
    return out
