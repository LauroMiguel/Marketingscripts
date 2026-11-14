"""Monta as imagens finais dos anuncios a partir dos renders brutos (PNG com fundo transparente).

Uso: python3 compor_imagens.py <pasta_raw> <pasta_anuncios> <pasta_stl>
Os renders brutos saem de index.html + shoot.js (three.js no Chromium headless).
"""
import sys, os
import trimesh
from PIL import Image, ImageDraw, ImageFont

RAW, OUT, STL = sys.argv[1], sys.argv[2], sys.argv[3]
W = 1600
F = "/usr/share/fonts/opentype/inter/"
def font(peso, tam): return ImageFont.truetype(F + "Inter-%s.otf" % peso, tam)

TINTA = (40, 40, 46)
CINZA = (120, 120, 128)
COTA = (30, 90, 170)
NOMES = {"espiral": "Estrela Espiral", "concentrica": "Estrela Concentrica",
         "facetada": "Estrela Facetada 3D", "vazada": "Estrela Vazada Colmeia"}
CORES = [("dourado", "Dourado (PLA)"), ("vermelho", "Vermelho (PETG)"), ("azul", "Azul (PETG)")]
AVISO = "Imagem ilustrativa (render 3D do modelo real)"


def crop(path):
    im = Image.open(path).convert("RGBA")
    return im.crop(im.getchannel("A").point(lambda a: 255 if a > 3 else 0).getbbox())


def fit(im, bw, bh):
    s = min(bw / im.width, bh / im.height)
    return im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)


def tela():
    return Image.new("RGBA", (W, W), (255, 255, 255, 255))


def salvar(c, path):
    c.convert("RGB").save(path, optimize=True)


def centro_txt(d, xc, y, txt, f, cor=TINTA):
    w = d.textlength(txt, font=f)
    d.text((xc - w / 2, y), txt, font=f, fill=cor)


def aviso(d):
    centro_txt(d, W / 2, W - 52, AVISO, font("Regular", 26), CINZA)


def simples(src, dst, fill=0.86, com_aviso=False):
    c = tela()
    im = fit(crop(src), W * fill, W * fill * (0.95 if com_aviso else 1))
    c.alpha_composite(im, ((W - im.width) // 2, (W - im.height) // 2 - (20 if com_aviso else 0)))
    if com_aviso:
        aviso(ImageDraw.Draw(c))
    salvar(c, dst)


def seta(d, a, b, cor=COTA, w=4, cab=16):
    """linha de cota com pontas de seta nas duas extremidades"""
    import math
    d.line([a, b], fill=cor, width=w)
    for p, q in ((a, b), (b, a)):
        ang = math.atan2(q[1] - p[1], q[0] - p[0])
        for s in (0.45, -0.45):
            d.line([p, (p[0] + cab * math.cos(ang + s), p[1] + cab * math.sin(ang + s))], fill=cor, width=w)


def tracejado(d, pts, cor, w=3, on=12, off=8):
    import math
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        L = math.hypot(x1 - x0, y1 - y0); t = 0
        while t < L:
            t2 = min(t + on, L)
            d.line([(x0 + (x1 - x0) * t / L, y0 + (y1 - y0) * t / L), (x0 + (x1 - x0) * t2 / L, y0 + (y1 - y0) * t2 / L)], fill=cor, width=w)
            t = t2 + off


def medidas(m, mesh, dst, peso_txt):
    (xmin, ymin, zmin), (xmax, ymax, zmax) = mesh.bounds
    ex, ey, ez = xmax - xmin, ymax - ymin, zmax - zmin
    frente, lado = crop(f"{RAW}/{m}_ortho_frente.png"), crop(f"{RAW}/{m}_ortho_lado.png")
    s = min(960 / ey, (W - 560) / (ex + ez))          # px por mm
    fr, la = frente.resize((round(ex * s), round(ey * s)), Image.LANCZOS), lado.resize((round(ez * s), round(ey * s)), Image.LANCZOS)
    chapado = Image.new("RGBA", la.size, (201, 161, 63, 255)); chapado.putalpha(la.getchannel("A")); la = chapado   # silhueta lateral
    L0 = (W - fr.width - 170 - la.width) // 2 + 40
    T0 = 330
    c = tela(); d = ImageDraw.Draw(c)
    c.alpha_composite(fr, (L0, T0))
    xl = L0 + fr.width + 170
    c.alpha_composite(la, (xl, T0))
    X = lambda x: L0 + (x - xmin) * s
    Y = lambda y: T0 + (ymax - y) * s
    centro_txt(d, W / 2, 50, "Medidas", font("SemiBold", 64))
    centro_txt(d, W / 2, 132, NOMES[m], font("Regular", 34), CINZA)
    fb, fm = font("SemiBold", 40), font("Medium", 30)
    # largura total
    y = T0 - 45; seta(d, (X(xmin), y), (X(xmax), y))
    centro_txt(d, (X(xmin) + X(xmax)) / 2, y - 52, f"{ex/10:.1f} cm".replace(".", ","), fb, COTA)
    # altura total
    x = L0 - 55; seta(d, (x, Y(ymax)), (x, Y(ymin)))
    t = f"{ey/10:.1f} cm".replace(".", ",")
    tw = d.textlength(t, font=fb); txt = Image.new("RGBA", (int(tw) + 10, 56), (0, 0, 0, 0))
    ImageDraw.Draw(txt).text((5, 0), t, font=fb, fill=COTA)
    txt = txt.rotate(90, expand=True); c.alpha_composite(txt, (int(x - 62), int((Y(ymax) + Y(ymin)) / 2 - txt.height / 2)))
    # espessura (vista lateral)
    y = T0 - 45; seta(d, (xl, y), (xl + la.width, y))
    centro_txt(d, xl + la.width / 2, y - 52, f"{ez/10:.1f} cm".replace(".", ","), fb, COTA)
    centro_txt(d, xl + la.width / 2, T0 + la.height + 20, "lateral", fm, CINZA)
    # furo (tracejado sobre a haste) e largura da haste
    hx0, hx1, hy0, hy1 = X(-7.5), X(7.5), Y(ymin), Y(ymin + 55)
    tracejado(d, [(hx0, hy0), (hx0, hy1), (hx1, hy1), (hx1, hy0)], (20, 20, 20), 3)
    y = Y(ymin) + 40; seta(d, (X(-11), y), (X(11), y), w=3, cab=12)
    centro_txt(d, X(0), y + 14, "haste 2,2 cm", fm, COTA)
    # chamada do furo
    ax, ay = hx1 + 6, (hy0 + hy1) / 2
    tx, ty = hx1 + 120, ay + 70
    d.line([(ax, ay), (tx - 8, ty + 18)], fill=TINTA, width=3)
    d.text((tx, ty), "furo interno", font=fm, fill=TINTA)
    d.text((tx, ty + 38), "Ø 1,5 cm x 5,5 cm", font=font("SemiBold", 32), fill=TINTA)
    centro_txt(d, W / 2, W - 140, f"Peso aproximado: {peso_txt}   |   variação normal de ±1 mm na peça impressa", font("Regular", 28))
    aviso(d)
    salvar(c, dst)


def encaixe(m, mesh, dst):
    (xmin, ymin, _), (xmax, ymax, _) = mesh.bounds
    c = tela(); d = ImageDraw.Draw(c)
    centro_txt(d, W / 2, 60, "Encaixe na ponta da árvore", font("SemiBold", 60))
    arv = fit(crop(f"{RAW}/{m}_arvore.png"), 680, 1080)
    c.alpha_composite(arv, (60 + (720 - arv.width) // 2, 180 + (1080 - arv.height) // 2))
    # corte tecnico: silhueta real + furo
    sil = crop(f"{RAW}/{m}_ortho_frente.png")
    ex, ey = xmax - xmin, ymax - ymin
    s = min(640 / ex, 1000 / ey)
    sil = sil.resize((round(ex * s), round(ey * s)), Image.LANCZOS)
    plano = Image.new("RGBA", sil.size, (233, 214, 160, 255)); plano.putalpha(sil.getchannel("A"))
    L0, T0 = 830 + (680 - sil.width) // 2, 200
    c.alpha_composite(plano, (L0, T0))
    X = lambda x: L0 + (x - xmin) * s
    Y = lambda y: T0 + (ymax - y) * s
    d.rectangle([X(-7.5), Y(ymin + 55), X(7.5), Y(ymin)], fill=(255, 255, 255))
    d.rectangle([X(-6.5), Y(ymin + 50), X(6.5), Y(ymin) + 120], fill=(42, 107, 63))   # ponta ilustrativa
    tracejado(d, [(X(-7.5), Y(ymin)), (X(-7.5), Y(ymin + 55)), (X(7.5), Y(ymin + 55)), (X(7.5), Y(ymin))], (20, 20, 20), 3, 10, 6)
    yb = Y(ymin) + 150; seta(d, (X(-7.5), yb), (X(7.5), yb), w=3, cab=10)
    centro_txt(d, X(0), yb + 12, "Ø 1,5 cm", font("SemiBold", 34), COTA)
    xs = X(11) + 40; seta(d, (xs, Y(ymin + 55)), (xs, Y(ymin)), w=3, cab=10)
    d.text((xs + 14, (Y(ymin + 55) + Y(ymin)) / 2 - 20), "5,5 cm", font=font("SemiBold", 34), fill=COTA)
    centro_txt(d, L0 + sil.width / 2, T0 - 10 + sil.height + 230, "corte da haste", font("Medium", 28), CINZA)
    fr = font("Regular", 31)
    linhas = ["• Furo interno: 1,5 cm de diâmetro e 5,5 cm de profundidade.",
              "• Serve em pontas de árvore com até cerca de 1,4 cm de espessura.",
              "• Meça a ponta da sua árvore antes de comprar."]
    for i, t in enumerate(linhas):
        d.text((110, 1350 + i * 50), t, font=fr, fill=TINTA)
    centro_txt(d, W / 2, W - 52, "Imagem ilustrativa. A árvore e os enfeites não acompanham o produto.", font("Regular", 26), CINZA)
    salvar(c, dst)


def cores(m, dst):
    c = tela(); d = ImageDraw.Draw(c)
    centro_txt(d, W / 2, 110, "3 cores disponíveis", font("SemiBold", 60))
    bw = (W - 160) / 3
    for i, (k, rot) in enumerate(CORES):
        im = fit(crop(f"{RAW}/{m}_capa_{k}.png"), bw - 40, 1000)
        x0 = 80 + i * bw
        c.alpha_composite(im, (int(x0 + (bw - im.width) / 2), int(260 + (1000 - im.height) / 2)))
        centro_txt(d, x0 + bw / 2, 1310, rot, font("Medium", 38))
    aviso(d)
    salvar(c, dst)


if __name__ == "__main__":
    import json
    pesos = json.load(open(os.path.join(OUT, "pesos_fatiador.json")))
    for m in NOMES:
        mesh = trimesh.load(f"{STL}/estrela_{m}.stl")
        pasta = os.path.join(OUT, m, "imagens"); os.makedirs(pasta, exist_ok=True)
        for k, _ in CORES:
            simples(f"{RAW}/{m}_capa_{k}.png", f"{pasta}/01_capa_{k}.png")
        cores(m, f"{pasta}/02_cores.png")
        simples(f"{RAW}/{m}_mesa.png", f"{pasta}/03_angulo_mesa.png", com_aviso=True)
        simples(f"{RAW}/{m}_lateral.png", f"{pasta}/04_lateral.png", com_aviso=True)
        simples(f"{RAW}/{m}_costas.png", f"{pasta}/05_costas.png", com_aviso=True)
        simples(f"{RAW}/{m}_detalhe.png", f"{pasta}/06_detalhe_haste.png", com_aviso=True)
        p = pesos[m]
        medidas(m, mesh, f"{pasta}/07_medidas.png", f"{round(p['PLA'])} g (PLA) / {round(p['PETG'])} g (PETG)")
        encaixe(m, mesh, f"{pasta}/08_encaixe.png")
        print("ok", m)
