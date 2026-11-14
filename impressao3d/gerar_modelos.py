"""Gera os STLs dos produtos. Uso: python gerar_modelos.py [NOME1 NOME2 ...]"""
import sys, math, numpy as np, trimesh
from shapely.geometry import Polygon, Point, box
from shapely.ops import unary_union
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
OUT = "stl/"

def ext(poly, h, z=0):
    parts = list(poly.geoms) if hasattr(poly, "geoms") else [poly]
    m = trimesh.util.concatenate([trimesh.creation.extrude_polygon(p, h) for p in parts if p.area > 0.01])
    m.apply_translation([0,0,z]); return m

def text_poly(txt, size):
    tp = TextPath((0,0), txt, size=size, prop=FontProperties(family="DejaVu Sans", weight="bold"))
    polys = [Polygon(p) for p in tp.to_polygons() if len(p) > 2]
    polys.sort(key=lambda p: -p.area)
    res = Polygon()
    for p in polys:  # buracos (ex.: "A","O") são subtraídos
        res = res.difference(p) if res.contains(p) else res.union(p)
    return res

def star(r_out=35, r_in=15, n=5):
    pts = [((r_out if i%2==0 else r_in)*math.sin(i*math.pi/n), (r_out if i%2==0 else r_in)*math.cos(i*math.pi/n)) for i in range(2*n)]
    return Polygon(pts)

# 1) Estrela de Natal com furo para fita (70 mm)
s = star().buffer(1.5, join_style=1).difference(Point(0,27).buffer(2.5))
ext(s, 4).export(OUT+"estrela_natal.stl")

# 2) Enfeite com nome (bola de Natal plana, 70 mm) - texto em relevo
def enfeite_nome(nome):
    base = Point(0,0).buffer(34, 128).union(box(-6,30,6,40)).difference(Point(0,36).buffer(2.5))
    t = text_poly(nome.upper(), 10)
    minx,miny,maxx,maxy = t.bounds; w = maxx-minx
    esc = min(1.0, 54/w)
    from shapely import affinity
    t = affinity.scale(t, esc, esc, origin=(0,0))
    minx,miny,maxx,maxy = t.bounds
    t = affinity.translate(t, -(minx+maxx)/2, -(miny+maxy)/2)
    m = trimesh.boolean.union([ext(base,3), ext(t,1.6,2.99)])
    m.export(OUT+f"enfeite_nome_{nome.lower()}.stl")

# 3) Chaveiro com nome (placa 60 x 18 mm)
def chaveiro(nome):
    from shapely import affinity
    t = text_poly(nome.upper(), 10)
    minx,miny,maxx,maxy = t.bounds
    esc = min(1.0, 44/(maxx-minx)); t = affinity.scale(t, esc, esc, origin=(0,0))
    minx,miny,maxx,maxy = t.bounds; t = affinity.translate(t, -(minx+maxx)/2+4, -(miny+maxy)/2)
    base = box(-26,-9,30,9).buffer(3, join_style=1).difference(Point(-24,0).buffer(3))
    trimesh.boolean.union([ext(base,3), ext(t,1.4,2.99)]).export(OUT+f"chaveiro_{nome.lower()}.stl")

# 4) Suporte de celular (perfil extrudado, 70 mm de largura)
perfil = Polygon([(0,0),(90,0),(90,6),(30,6),(68,95),(62,98),(18,8),(14,8),(14,22),(6,22),(6,6),(0,6)]).buffer(1,join_style=1).buffer(-1,join_style=1)
m = ext(perfil, 70); m.apply_transform(trimesh.transformations.rotation_matrix(math.pi/2,[1,0,0]))
m.apply_translation(-m.bounds[0]); m.export(OUT+"suporte_celular.stl")

for n in (sys.argv[1:] or ["Maria","Joao","Ana"]):
    enfeite_nome(n); chaveiro(n)
for f in __import__("glob").glob(OUT+"*.stl"):
    mm = trimesh.load(f); print(f, "estanque:", mm.is_watertight, "volume cm3: %.1f" % (mm.volume/1000), "tamanho mm:", np.round(mm.extents,1))
