# Kit de anúncios: ponteiras de estrela (Mercado Livre)

Tudo aqui usa **somente os 4 modelos próprios** da pasta `estrelas/`. Nenhum arquivo, foto ou desenho do MakerWorld foi usado.

## O que tem nesta pasta

| Arquivo | Para que serve |
|---|---|
| `guia_impressao.md` | **Comece por aqui.** Passo a passo no Creality Print + teste da primeira peça |
| `precos_e_viabilidade.md` | Pesquisa de preços e tarifas, custo, sobra por venda, recomendação e riscos |
| `planilha_precos.xlsx` | A mesma conta com fórmulas. Troque as células amarelas |
| `facetada/anuncio_facetada.txt` | Anúncio 1 (primeira leva): título, categoria, ficha, descrição, FAQ |
| `concentrica/anuncio_concentrica.txt` | Anúncio 2 (primeira leva) |
| `vazada/anuncio_vazada.txt` | Anúncio 3 (segunda leva) |
| `espiral/anuncio_espiral.txt` | Anúncio 4 (segunda leva) |
| `<modelo>/imagens/` | 10 imagens de 1600 × 1600 px por modelo |
| `pesos_fatiador.json` | Pesos e tempos medidos fatiando os STL |
| `ferramentas_render/` | Scripts que geraram as imagens e a planilha (para refazer se o modelo mudar) |

### Imagens de cada modelo

| Arquivo | Conteúdo |
|---|---|
| `01_capa_dourado.png`, `01_capa_vermelho.png`, `01_capa_azul.png` | Capa de cada variação de cor: fundo branco puro, sem texto |
| `02_cores.png` | As 3 cores lado a lado |
| `03_angulo_mesa.png` | Peça deitada, vista de cima em ângulo |
| `04_lateral.png` | Ângulo lateral (mostra a espessura) |
| `05_costas.png` | Costas (planas) |
| `06_detalhe_haste.png` | Boca do furo da haste |
| `07_medidas.png` | Largura, altura, espessura, haste e furo, com cotas tiradas do arquivo STL |
| `08_encaixe.png` | Como encaixa na ponta da árvore + corte do furo |

Todas são **renders 3D feitos a partir dos STL reais**, não geradas por IA. Mostram o formato e as medidas exatos, mas **não são fotos**. A descrição dos anúncios já avisa isso. Depois da primeira impressão, **troque por fotos reais**.

---

## Ordem de trabalho

1. **Meça a ponta de uma árvore de Natal comum** (a sua ou a de alguém).
2. **Imprima a Concêntrica em PLA dourado** seguindo o `guia_impressao.md`.
3. **Teste o encaixe.** Se o furo de 15 mm não servir, **pare e peça o ajuste** antes de publicar.
4. **Imprima uma Facetada em PETG vermelho** para testar o PETG.
5. Tire 2 ou 3 fotos reais (opcional agora, mas ajuda muito).
6. **Publique os anúncios 1 e 2** (passo a passo abaixo).
7. Depois das primeiras vendas, publique os anúncios 3 e 4.

---

## Como publicar pelo aplicativo do Mercado Livre (passo a passo)

> Os nomes das telas podem mudar um pouco entre versões do app. Se algo estiver diferente, o site (mercadolivre.com.br → **Vender**) segue a mesma sequência.

**Antes de começar:** passe as imagens da pasta `<modelo>/imagens/` para o celular (Google Drive, WhatsApp para você mesmo ou cabo USB). Abra o `anuncio_<modelo>.txt` no celular para copiar e colar.

1. Abra o app do **Mercado Livre** → menu → **Vender**.
2. Escolha **Produtos**.
3. **Título:** cole o título da seção 1 do arquivo. O app sugere uma categoria: confira com a seção 2. Se houver uma opção de "Ponteiras", prefira ela.
4. Se o app oferecer um **produto de catálogo** pronto, escolha **"Não encontrei meu produto"** ou "Continuar sem catálogo". A peça é sua, não é de nenhuma marca.
5. **Condição:** Novo.
6. **Variações / Cor:** ative as variações e crie **Dourado**, **Vermelho** e **Azul**.
   - Em cada cor, coloque **primeiro a capa daquela cor** (`01_capa_<cor>.png`) e depois as fotos comuns, na ordem `02` a `08`.
   - Estoque de cada cor: **3** (explicação abaixo).
7. **Ficha técnica:** preencha com a seção 5. Em código universal (GTIN), marque que o produto **não tem código**.
8. **Preço:** coloque o da seção 3. Escolha o anúncio **Clássico**. Nesta tela o app mostra **quanto você recebe**: compare com a planilha. Se for bem diferente, a planilha precisa ser ajustada; confie no app.
9. **Envio:** Mercado Envios. Informe o pacote: **25 × 23 × 6 cm, 0,15 kg**. Pese e meça a primeira embalagem pronta e corrija se precisar.
10. **Prazo de fabricação / disponibilidade:** **3 dias** (seção 7). Isso avisa ao comprador que a peça é feita sob encomenda.
11. **Garantia:** garantia do vendedor, **90 dias**.
12. **Descrição:** cole a seção 6 inteira. Não coloque telefone, e-mail ou links: o ML proíbe.
13. Revise e **publique**.
14. Guarde as **respostas prontas** (seção 8) no celular para responder rápido. Responder rápido ajuda a vender.

### Sobre o estoque (importante)
O filamento é **compartilhado** entre os anúncios. Se você colocar estoque de 9 dourados em cada um dos dois anúncios, pode vender 18 dourados e só conseguir imprimir 9. Por isso:
- comece com **3 unidades por cor em cada anúncio**;
- depois de cada venda, olhe quanto filamento sobrou (pese o carretel) e reponha o estoque aos poucos;
- se o dourado estiver acabando, **zere o dourado** nos anúncios e deixe só vermelho e azul.

### Depois da venda
1. O app avisa a venda. **Imprima a peça** (se ainda não tiver pronta).
2. Embale: plástico bolha em volta da estrela, em caixa firme. As pontas não podem encostar direto no papelão.
3. Imprima a etiqueta pelo app e poste/entregue no prazo indicado.
4. Quando a avaliação chegar, agradeça.

---

## Publicar pela API (opcional)

Dá para eu criar os anúncios direto na sua conta pela API do Mercado Livre, mas **só com um token de acesso da sua conta** para `api.mercadolibre.com`. Se quiser esse caminho:
- **nunca cole o token no chat**: eu peço por um formulário seguro;
- eu crio os anúncios **pausados** e mostro para você conferir antes de ativar.

Pelo app é mais simples e você mantém o controle. É o caminho recomendado.
