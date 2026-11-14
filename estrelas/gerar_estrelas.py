"""Gera 4 ponteiras de estrela originais (STL) para impressao 3D sem suportes.

Toda a geometria e construida aqui, a partir de formulas. Uso:
    python3 gerar_estrelas.py [pasta_de_saida]
Dependencias: numpy, shapely, trimesh, manifold3d, mapbox_earcut
"""
import sys, os
import numpy as np
import trimesh
from shapely.geometry import Polygon, Point, LineString
from shapely.ops import unary_union
from shapely import affinity

# Encaixe na ponta da arvore (mm)
FURO_D = 15.0      # diametro do furo
FURO_PROF = 55.0   # profundidade do furo
HASTE_L = 22.0     # largura externa da haste
HASTE_H = 20.0     # altura externa da haste


def estrela2d(R, r=None, pontas=5, rot=90.0):
    r = R * 0.40 if r is None else r
    pts = []
    for i in range(pontas * 2):
        a = np.radians(rot + i * 180.0 / pontas)
        q = R if i % 2 == 0 else r
        pts.append((q * np.cos(a), q * np.sin(a)))
    return Polygon(pts)


def extrudar(geom, h, z0=0.0):
    geom = geom.buffer(0).simplify(0.02)
    geoms = [geom] if geom.geom_type == "Polygon" else list(geom.geoms)
    partes = []
    for g in geoms:
        if g.area < 0.5:
            continue
        m = trimesh.creation.extrude_polygon(g, h)
        m.apply_translation([0, 0, z0])
        partes.append(m)
    return unir(partes)


def unir(partes):
    partes = [p for p in partes if p is not None]
    return partes[0] if len(partes) == 1 else trimesh.boolean.union(partes, engine="manifold", check_volume=False)


def haste(y_topo, y_base):
    """Haste com furo, deitada na mesa (imprime sem suporte). Corre ao longo de -Y."""
    L, H, c = HASTE_L, HASTE_H, 6.0
    perfil = Polygon([(-L/2, 0), (L/2, 0), (L/2, H-c), (L/2-c, H), (-L/2+c, H), (-L/2, H-c)])
    comp = y_topo - y_base
    corpo = trimesh.creation.extrude_polygon(perfil, comp)       # eixo Z
    furo = trimesh.creation.cylinder(radius=FURO_D/2, height=FURO_PROF + 1, sections=48)
    furo.apply_translation([0, H/2, (FURO_PROF + 1)/2 - 1])       # abre na base
    pec = trimesh.boolean.difference([corpo, furo], engine="manifold")
    # (x, y, z) -> (x, z_local -> y, y_local -> z): base da haste em y_base
    T = np.array([[1, 0, 0, 0], [0, 0, 1, y_base], [0, 1, 0, 0], [0, 0, 0, 1]], float)
    pec.apply_transform(T)
    pec.fix_normals()
    return pec


def com_haste(corpo, R, r):
    y_topo = -r + 8.0                       # entra no vale entre as duas pontas de baixo
    y_base = -R * np.cos(np.radians(36)) - 30.0
    return unir([corpo, haste(y_topo, y_base)])


# 1) ESPIRAL: cata-vento de 5 bracos curvos com nervura em relevo
def espiral(R=90.0):
    def braco(w0, r0, k):
        t = np.linspace(0, 1, 40)
        rr = r0 + (R - r0) * t
        th = np.radians(90 - 75 + 72 * k) + np.radians(75) * t
        c = np.c_[rr * np.cos(th), rr * np.sin(th)]
        d = np.gradient(c, axis=0); d /= np.linalg.norm(d, axis=1)[:, None]
        n = np.c_[-d[:, 1], d[:, 0]]
        w = (w0 * (1 - t) ** 0.85 + 0.6)[:, None]
        return Polygon(np.r_[c + n * w, (c - n * w)[::-1]]).buffer(0)
    base = unary_union([braco(15, 10, k) for k in range(5)] + [Point(0, 0).buffer(24)])
    nerv = unary_union([braco(5, 14, k) for k in range(5)])
    miolo = estrela2d(17, 7.5)
    corpo = unir([extrudar(base, 5), extrudar(nerv.intersection(base), 8.5), extrudar(miolo, 11)])
    return com_haste(corpo, R, 30.0)


# 2) CONCENTRICA: tres aneis em estrela, em degraus, ligados por raios
def concentrica(R=78.0):
    r = R * 0.42
    def anel(s, esp):
        e = affinity.scale(estrela2d(R, r), s, s, origin=(0, 0))
        return e.difference(e.buffer(-esp, join_style=2))
    fora, meio, dentro = anel(1.0, 5.5), anel(0.66, 5.0), affinity.scale(estrela2d(R, r), 0.30, 0.30, origin=(0, 0))
    raios = []
    for i in range(10):
        a = np.radians(90 + i * 36)
        q = (R if i % 2 == 0 else r) - 2
        raios.append(LineString([(0, 0), (q * np.cos(a), q * np.sin(a))]).buffer(1.6))
    raios = unary_union(raios).intersection(estrela2d(R, r))
    corpo = unir([extrudar(unary_union([fora, raios]), 5), extrudar(meio, 7), extrudar(dentro, 9)])
    return com_haste(corpo, R, r)


# 3) FACETADA: estrela volumetrica classica, 10 facetas, costas planas
def facetada(R=88.0, H=24.0, base=2.0):
    r = R * 0.40
    cont = np.array(estrela2d(R, r).exterior.coords)[:-1]
    n = len(cont)
    v = np.vstack([np.c_[cont, np.full(n, base)], [[0, 0, base + H]], [[0, 0, base]]])
    f = []
    for i in range(n):
        j = (i + 1) % n
        f.append([i, j, n]); f.append([j, i, n + 1])
    piramide = trimesh.Trimesh(v, f); piramide.fix_normals()
    corpo = unir([piramide, extrudar(estrela2d(R, r), base + 0.01)])
    return com_haste(corpo, R, r)


# 4) VAZADA: moldura em estrela preenchida com colmeia hexagonal
def vazada(R=100.0):
    r = R * 0.45
    est = estrela2d(R, r)
    moldura = est.difference(est.buffer(-5.0, join_style=2))
    a = 9.0                                    # lado do hexagono
    linhas = []
    for i in range(-10, 11):
        for j in range(-10, 11):
            cx, cy = a * 1.5 * i, a * np.sqrt(3) * (j + 0.5 * (i % 2))
            hx = [(cx + a * np.cos(np.radians(60 * k)), cy + a * np.sin(np.radians(60 * k))) for k in range(7)]
            linhas.append(LineString(hx))
    colmeia = unary_union(linhas).buffer(1.1).intersection(est)
    miolo = estrela2d(20, 9)
    corpo = unir([extrudar(colmeia, 4), extrudar(moldura, 6), extrudar(miolo, 8)])
    return com_haste(corpo, R, r)


MODELOS = {
    "estrela_espiral": espiral,
    "estrela_concentrica": concentrica,
    "estrela_facetada": facetada,
    "estrela_vazada": vazada,
}

if __name__ == "__main__":
    saida = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
    for nome, fn in MODELOS.items():
        m = fn()
        m.merge_vertices(); m.fix_normals()
        m.export(os.path.join(saida, nome + ".stl"))
        e = m.extents
        print("%-20s %6.1f x %6.1f x %5.1f mm | vol %6.1f cm3 | ~%4.0f g PLA macico | estanque=%s | pecas=%d"
              % (nome, e[0], e[1], e[2], m.volume / 1000, m.volume / 1000 * 1.24, m.is_watertight, m.body_count))
