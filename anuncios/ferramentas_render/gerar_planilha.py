"""Gera anuncios/planilha_precos.xlsx (com formulas) e imprime a tabela calculada."""
import json, os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

AQUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(AQUI, "..")
pesos = json.load(open(os.path.join(OUT, "pesos_fatiador.json")))

# ---------- premissas: (chave, rotulo, valor, unidade, origem) ----------
PREM = [
    ("pla_kg", "Preço do PLA dourado (1 kg)", 100.0, "R$", "ESTIMATIVA - troque pelo que você pagou"),
    ("petg_kg", "Preço do PETG (1 kg)", 100.0, "R$", "ESTIMATIVA - troque pelo que você pagou"),
    ("estoque_pla", "Estoque PLA dourado", 600, "g", "informado pelo usuário"),
    ("estoque_petg", "Estoque PETG por cor (vermelho e azul)", 1000, "g", "informado pelo usuário"),
    ("aproveit", "Aproveitamento do rolo (sobra, ponta, purga)", 0.95, "fração", "ESTIMATIVA"),
    ("falha", "Margem para peças perdidas/falhas", 0.10, "fração", "ESTIMATIVA (iniciante: pode ser maior)"),
    ("kwh", "Tarifa de energia", 0.95, "R$/kWh", "ESTIMATIVA - confira sua conta de luz"),
    ("watts", "Consumo médio da impressora imprimindo", 150, "W", "ESTIMATIVA (mesa aquecida + bico)"),
    ("embal", "Embalagem (caixa + plástico bolha + fita)", 4.50, "R$", "ESTIMATIVA"),
    ("com_cla", "Tarifa de venda Clássico (Casa e Decoração)", 0.14, "fração", "PESQUISADO: 12-14% (blogs, nov/2026) - usei o teto"),
    ("com_pre", "Tarifa de venda Premium (Casa e Decoração)", 0.19, "fração", "PESQUISADO: 17-19% (blogs, nov/2026) - usei o teto"),
    ("env_19_49", "Custo de envio p/ vendedor, preço R$19-48,99, pacote 0,5-1 kg", 7.15, "R$", "PESQUISADO: tabela ML ajuda 40538 citada em 13/11/2026"),
    ("env_49_79", "Custo de envio p/ vendedor, preço R$49-78,99, pacote 0,5-1 kg", 8.45, "R$", "PESQUISADO: idem"),
]
# modelos: nome, pesos do fatiador, tempo, preco sugerido
MODELOS = [
    ("Facetada 3D", "facetada", 39.90),
    ("Concêntrica", "concentrica", 34.90),
    ("Vazada Colmeia", "vazada", 44.90),
    ("Espiral", "espiral", 39.90),
]
CORES = [("Dourado", "PLA"), ("Vermelho", "PETG"), ("Azul", "PETG")]

wb = Workbook()
H = Font(bold=True, color="FFFFFF"); HF = PatternFill("solid", fgColor="2F4A7A")
IN = PatternFill("solid", fgColor="FFF6D6"); fina = Side(style="thin", color="CCCCCC")
B = Border(left=fina, right=fina, top=fina, bottom=fina)

def cab(ws, linha, cols):
    for i, c in enumerate(cols, 1):
        x = ws.cell(linha, i, c); x.font = H; x.fill = HF; x.alignment = Alignment(wrap_text=True, vertical="center"); x.border = B

# ---- aba Premissas ----
ws = wb.active; ws.title = "Premissas"
ws["A1"] = "Premissas (células amarelas podem ser alteradas)"; ws["A1"].font = Font(bold=True, size=13)
cab(ws, 3, ["Item", "Valor", "Unidade", "Origem do dado"])
REF = {}
for i, (k, rot, val, un, orig) in enumerate(PREM, start=4):
    ws.cell(i, 1, rot); c = ws.cell(i, 2, val); c.fill = IN; ws.cell(i, 3, un); ws.cell(i, 4, orig)
    if un == "fração": c.number_format = "0%"
    elif un.startswith("R$"): c.number_format = '"R$" #,##0.00'
    for j in range(1, 5): ws.cell(i, j).border = B
    REF[k] = f"Premissas!$B${i}"
for col, w in zip("ABCD", (52, 12, 10, 62)): ws.column_dimensions[col].width = w

# ---- aba Custos ----
wc = wb.create_sheet("Custo por peça")
cab(wc, 1, ["Modelo", "Cor", "Material", "Peso (g) fatiador", "Tempo (fatiador)", "Filamento R$", "Filamento c/ falhas R$",
            "Energia R$", "Embalagem R$", "CUSTO TOTAL R$", "Peças por rolo (estoque)"])
linha = 2; CUSTO = {}
for nome, k, _ in MODELOS:
    for cor, mat in CORES:
        p = pesos[k][mat]; t = pesos[k]["tempo_" + mat]
        h = int(t.split("h")[0]) + int(t.split("h")[1]) / 60
        kg = REF["pla_kg"] if mat == "PLA" else REF["petg_kg"]
        est = REF["estoque_pla"] if mat == "PLA" else REF["estoque_petg"]
        r = linha
        vals = [nome, cor, mat, round(p, 2), t, f"=D{r}/1000*{kg}", f"=F{r}*(1+{REF['falha']})",
                f"={h:.3f}*{REF['watts']}/1000*{REF['kwh']}", f"={REF['embal']}", f"=G{r}+H{r}+I{r}",
                f"=ROUNDDOWN({est}*{REF['aproveit']}/(D{r}*(1+{REF['falha']})),0)"]
        for j, v in enumerate(vals, 1):
            c = wc.cell(r, j, v); c.border = B
            if j in (6, 7, 8, 9, 10): c.number_format = '"R$" #,##0.00'
        CUSTO[(k, cor)] = f"'Custo por peça'!J{r}"
        linha += 1
for i, w in enumerate((16, 10, 9, 10, 10, 11, 12, 10, 11, 12, 14), 1): wc.column_dimensions[get_column_letter(i)].width = w
wc.cell(linha + 1, 1, "Peças por rolo: (estoque x aproveitamento) / (peso x (1+falhas)). O dourado tem só 600 g.").font = Font(italic=True)
wc.cell(linha + 2, 1, "O filamento já foi comprado: o custo aqui é o de REPOSIÇÃO, para você saber se a venda paga um rolo novo.").font = Font(italic=True)

# ---- aba Preço e margem ----
wp = wb.create_sheet("Preço e margem")
cab(wp, 1, ["Modelo", "Cor", "Tipo de anúncio", "Preço de venda R$", "Tarifa %", "Tarifa R$", "Custo de envio R$",
            "Você recebe R$", "Custo da peça R$", "SOBRA por venda R$", "Sobra % do preço", "Preço mínimo sem prejuízo R$"])
r = 2
for nome, k, preco in MODELOS:
    for cor, _ in CORES:
        for tipo, kc in (("Clássico", "com_cla"), ("Premium", "com_pre")):
            pv = preco if tipo == "Clássico" else round(preco + 5, 2)
            env = f"=IF(D{r}<49,{REF['env_19_49']},IF(D{r}<79,{REF['env_49_79']},\"acima de R$79: frete grátis pago por você - recalcule\"))"
            vals = [nome, cor, tipo, pv, f"={REF[kc]}", f"=D{r}*E{r}", env, f"=D{r}-F{r}-G{r}", f"={CUSTO[(k, cor)]}",
                    f"=H{r}-I{r}", f"=J{r}/D{r}", f"=(G{r}+I{r})/(1-E{r})"]
            for j, v in enumerate(vals, 1):
                c = wp.cell(r, j, v); c.border = B
                if j in (4, 6, 7, 8, 9, 10, 12): c.number_format = '"R$" #,##0.00'
                if j in (5, 11): c.number_format = "0%"
            wp.cell(r, 4).fill = IN
            r += 1
for i, w in enumerate((16, 10, 12, 12, 9, 10, 12, 12, 12, 13, 11, 14), 1): wp.column_dimensions[get_column_letter(i)].width = w
nota = ["'Sobra' NÃO é lucro garantido: não inclui seu tempo, impostos (MEI/DAS), devoluções, nem peças que não venderem.",
        "Tarifa e custo de envio: confira no simulador do Mercado Livre ao criar o anúncio; os valores mudam e dependem da sua reputação.",
        "Abaixo de R$ 79 o Mercado Livre oferece frete grátis ao comprador e cobra do vendedor o 'custo de envio' da tabela.",
        "Pacote considerado na faixa 0,5-1 kg por segurança (caixa ~25x23x6 cm pode contar peso cúbico); se cair em até 0,3 kg, sobra um pouco mais."]
for i, t in enumerate(nota): wp.cell(r + 1 + i, 1, t).font = Font(italic=True)

# ---- aba Fontes ----
wf = wb.create_sheet("Fontes")
fontes = [
    ("Tabela de custo de envio ML 2026 (cita ajuda oficial 40538, consulta 13/11/2026)", "https://hunterhub.com.br/blog/tabela-de-frete-mercado-livre/"),
    ("Tarifas por categoria 2026 (Casa e decoração 12-14% / 17-19%)", "https://vendedorix.com.br/blog/mercado-livre-tarifas-2026-tabela-completa"),
    ("Taxas ML 2026: Clássico 10-14%, Premium 15-19%, custo por unidade < R$79", "https://lider10.com.br/blog/taxas-mercado-livre-2026/"),
    ("Busca ML: ponteira estrela árvore de Natal (preços R$15-26 nas comuns)", "https://lista.mercadolivre.com.br/ponteira-estrela-arvore-de-natal"),
    ("Ponteira estrela 3D dourada 29 cm Magizi (R$ 59,90; algodão e ferro)", "https://www.mercadolivre.com.br/ponteira-estrela-3d-dourada-29cm-p-arvore-de-natal-magizi-cor-dourado/p/MLB29286812"),
    ("Busca ML: estrela 3D (inclui estrela impressa em 3D ~R$ 29)", "https://lista.mercadolivre.com.br/estrela-3d"),
    ("Pesos e tempos: PrusaSlicer 2.7.2, camada 0,2 mm, 2 paredes, 5 topo/4 fundo, 15% grade, sem suporte", "(fatiado nesta sessão)"),
]
cab(wf, 1, ["Fonte", "Link"])
for i, (a, b) in enumerate(fontes, 2): wf.cell(i, 1, a); wf.cell(i, 2, b)
wf.column_dimensions["A"].width = 90; wf.column_dimensions["B"].width = 100
wb.save(os.path.join(OUT, "planilha_precos.xlsx"))

# ---- calculo espelhado em Python (para conferir e para o relatorio) ----
P = {k: v for k, _, v, _, _ in PREM}
print("CUSTOS")
for nome, k, preco in MODELOS:
    for cor, mat in CORES:
        p = pesos[k][mat]; t = pesos[k]["tempo_" + mat]; h = int(t.split("h")[0]) + int(t.split("h")[1]) / 60
        kg = P["pla_kg"] if mat == "PLA" else P["petg_kg"]; est = P["estoque_pla"] if mat == "PLA" else P["estoque_petg"]
        fil = p / 1000 * kg * (1 + P["falha"]); en = h * P["watts"] / 1000 * P["kwh"]; custo = fil + en + P["embal"]
        un = int(est * P["aproveit"] // (p * (1 + P["falha"])))
        res = []
        for tipo, kc, pv in (("Cla", "com_cla", preco), ("Pre", "com_pre", preco + 5)):
            env = P["env_19_49"] if pv < 49 else P["env_49_79"]
            sobra = pv - pv * P[kc] - env - custo
            res.append(f"{tipo} R${pv:.2f}: recebe {pv - pv*P[kc] - env:.2f} sobra {sobra:.2f} ({sobra/pv:.0%})")
        print(f"{nome:15s} {cor:8s} {p:5.1f} g  custo {custo:5.2f}  pecas/rolo {un:2d} | " + " | ".join(res))
