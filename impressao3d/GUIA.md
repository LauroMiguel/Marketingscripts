# Plano de negócio: impressão 3D em Uberlândia (Creality Hi)

## Estoque
| Filamento | Quantidade | Uso |
|---|---|---|
| PLA dourado | 600 g | Enfeites de Natal com nome e estrelas (produto principal) |
| PETG vermelho | ~900 g | Enfeites vermelhos, chaveiros, suportes |
| PETG azul | ~900 g | Chaveiros e suportes de celular |
| PETG preto | 100 g | Reserva |

**Por que Natal:** faltam ~6 semanas. Dourado e vermelho são as cores do Natal, e enfeite com nome é presente barato e personalizado. Loja nenhuma vende isso pronto.

## Produtos e preços
Custo do filamento ≈ R$ 0,10/g. Energia ≈ R$ 0,10 por hora de impressão.

| Produto | Arquivo | Peso | Tempo* | Custo | Preço sugerido |
|---|---|---|---|---|---|
| Enfeite de Natal com nome (dourado) | `enfeite_nome_*.stl` | ~11 g | ~35 min | ~R$ 1,20 | **R$ 12** / kit com 3: **R$ 30** |
| Estrela de Natal | `estrela_natal.stl` | ~8 g | ~20 min | ~R$ 0,90 | **R$ 6** / 5 por **R$ 25** |
| Chaveiro com nome | `chaveiro_*.stl` | ~5 g | ~15 min | ~R$ 0,60 | **R$ 8** / 3 por **R$ 20** |
| Suporte de celular (PETG) | `suporte_celular.stl` | ~30 g | ~1h30 | ~R$ 3,30 | **R$ 25** |

\*Estimativas: o fatiador mostra os números reais. Com 600 g de dourado saem ~50 enfeites. A ~R$ 10 cada, isso dá ~R$ 500.

**Dica de cor:** imprima o enfeite em dourado e, quando chegar na camada do nome, pause e troque para o vermelho (veja o passo 6). O nome fica vermelho sobre o dourado e o enfeite parece bem mais caro.

## Como gerar um nome novo
No computador com Python: `python gerar_modelos.py Pedro Luiza Heitor`. Ou só me mande os nomes aqui no chat que eu gero.

## Fatiar no Creality Print (passo a passo)
1. Baixe o **Creality Print** (grátis, site da Creality) e escolha a impressora **Creality Hi**.
2. Arraste o `.stl` para a tela. Ele deve ficar **deitado** na mesa. O suporte de celular já vem de pé, do jeito certo.
3. À esquerda, escolha o filamento: **Generic PLA** (dourado) ou **Generic PETG** (vermelho/azul).
4. Configurações:
   - Altura de camada: **0,2 mm**
   - Paredes: **3**. Preenchimento: **15%** (suporte de celular: **20%**)
   - Suportes: **desligado** (nenhuma peça precisa)
   - PLA: bico 210 °C, mesa 60 °C. PETG: bico 240 °C, mesa 70 °C, ventoinha 40%.
5. Dá para colocar várias peças de uma vez: clique com o botão direito → **Clonar**, depois em **Organizar** (ícone de grade). Uma mesa cheia de enfeites rende uns 10 por impressão.
6. Para o nome em outra cor: no slider de camadas à direita, vá até a camada de **3,0 mm** e clique no **+** → "Pausa". Quando a impressora parar, troque o filamento e continue.
7. Clique em **Fatiar** e confira o tempo e as gramas. Depois envie por Wi-Fi ou pelo pendrive.
8. **PETG gruda demais:** espere a mesa esfriar e flexione a chapa para soltar a peça.

## Anúncios (grátis: Marketplace + grupos)
Poste no **Facebook Marketplace**, nos grupos **"Compra e venda Uberlândia"**, **"Desapega Uberlândia"** e de bairros, e no **status do WhatsApp** todo dia.

**Anúncio 1: enfeite com nome**
> 🎄 ENFEITE DE NATAL PERSONALIZADO COM NOME 🎄
> Coloque o nome de cada pessoa da família na sua árvore! Dourado com o nome em relevo.
> ✨ 1 por R$ 12 | 3 por R$ 30 | 5 por R$ 45
> 🎁 Ótimo para lembrancinha de amigo secreto, professores e família
> 📍 Entrega em Uberlândia, ou retire no [seu bairro]
> ⏱️ Fica pronto em 1 a 2 dias. Chame no WhatsApp com os nomes!

**Anúncio 2: lembrancinha / amigo secreto**
> 🎁 LEMBRANCINHA DE NATAL A PARTIR DE R$ 6
> Estrelas e enfeites com nome feitos em impressão 3D, aqui em Uberlândia.
> Pedidos para empresa, escola e família: acima de 10 unidades, desconto!
> Chame no WhatsApp 👉 [seu número]

**Anúncio 3: chaveiro com nome**
> 🔑 CHAVEIRO COM NOME: 3 por R$ 20
> Escolha a cor: vermelho ou azul. Resistente (PETG), não quebra fácil.
> Pronto em 24 h, com entrega em Uberlândia.

**Fotos (o que mais vende):** luz de janela, fundo liso (folha branca) e 1 foto do enfeite pendurado numa árvore ou galho. Mostre a peça na mão para dar noção de tamanho.

## Regras para não ter prejuízo
- **Peça sinal de 50% via Pix** em encomendas personalizadas.
- Antes de anunciar, imprima 3 amostras (com nomes da sua família) para fotografar.
- Não use escudos de time nem personagens de marca, porque dá problema de direitos autorais. Cores (vermelho e preto, azul) pode à vontade.
- Reinvista o primeiro lucro em 1 kg de PLA vermelho ou verde e argolas e fitas para os enfeites.
