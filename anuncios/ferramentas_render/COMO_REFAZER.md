# Como refazer as imagens e a planilha

Necessário refazer quando um STL mudar (por exemplo, o diâmetro do furo `FURO_D` em `estrelas/gerar_estrelas.py`).

```bash
# 1) gerar STL novos
python3 estrelas/gerar_estrelas.py

# 2) preparar a pasta de render (fora do repositório)
mkdir -p /tmp/render/stl /tmp/render/raw && cp anuncios/ferramentas_render/{index.html,shoot.js,jobs.json} /tmp/render/
cp estrelas/*.stl /tmp/render/stl/ && cd /tmp/render && npm init -y && npm install three@0.160.0
python3 -m http.server 8765 --bind 127.0.0.1 &      # a página carrega os STL por HTTP
NODE_PATH=$(npm root -g) node shoot.js jobs.json   # Playwright + Chromium: 40 PNGs transparentes em raw/

# 3) compor as imagens finais (fundo branco puro, cotas, encaixe)
cd -  && cd anuncios && python3 ferramentas_render/compor_imagens.py /tmp/render/raw . ../estrelas

# 4) planilha (atualize antes os pesos em pesos_fatiador.json se o modelo mudou)
python3 ferramentas_render/gerar_planilha.py
```

Os pesos de `pesos_fatiador.json` vieram do PrusaSlicer 2.7.2 (camada 0,2 mm, 2 paredes, 5 topo / 4 fundo, 15% grade, sem suporte).
