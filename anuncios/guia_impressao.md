# Guia de impressão: estrelas na Creality Hi (para quem nunca fatiou)

> **Antes de tudo, um aviso honesto:** nenhuma destas estrelas foi impressa ainda. Os pesos e tempos abaixo saíram de outro fatiador (PrusaSlicer 2.7.2) com a mesma configuração. Servem de referência, mas o Creality Print vai dar números um pouco diferentes. Os nomes de botões e menus abaixo valem para o **Creality Print 6.x**. Não consegui abrir o programa aqui para conferir tela por tela, então algum nome pode estar um pouco diferente na sua versão. O conceito é o mesmo.

---

## Parte 1 · Preparar o programa (uma vez só)

1. **Instale o Creality Print** (versão 6 ou mais nova) pelo site da Creality. A página de suporte da Creality Hi indica o Creality Print 5.1 ou mais novo.
2. Na primeira abertura, o programa pede para **escolher a impressora**: marque **Creality Hi** com **bico 0,4 mm**.
3. Ele também pede os **filamentos**. Marque um perfil de **PLA** (por exemplo "Generic PLA" ou "Hyper PLA") e um de **PETG** ("Generic PETG" ou "Hyper PETG").
   - Regra de ouro: **para PETG, comece SEMPRE do perfil de PETG**, nunca de um perfil de PLA editado. Os perfis já trazem temperatura, ventilação e retração certas para cada material.
4. Conecte a impressora pela rede (Wi-Fi) se quiser mandar o arquivo direto. Se preferir, salve em pendrive ou cartão. Siga o assistente do próprio programa.

---

## Parte 2 · Abrir a estrela e colocar na mesa

1. Clique em **Importar** (ícone de cubo com "+", ou atalho **Ctrl+I**) e escolha o arquivo, por exemplo `estrelas/estrela_concentrica.stl`. Também dá para arrastar o arquivo para dentro da janela.
2. A estrela aparece **deitada na mesa, com a parte plana (as costas) para baixo**. É assim mesmo: ela foi desenhada para imprimir nessa posição, **sem suporte**.
3. Se ela aparecer em pé ou torta: selecione a peça, use a ferramenta **"Colocar na face"** (atalho **F**) e clique na face plana de trás.
4. Clique em **Organizar** (atalho **A**) para centralizar na mesa.
5. Confira o tamanho: todas cabem na mesa de 260 × 260 mm, mas **só uma estrela por vez**. A maior, a Vazada, tem 190 × 211 mm.
6. **Não mude a escala.** As medidas do anúncio são as do arquivo.

---

## Parte 3 · Configurações (perfil "Estrela")

No painel da direita, deixe assim. Se não achar alguma opção, procure a chave **"Avançado"/"Expert"** no topo do painel para mostrar todas.

| Onde | Opção | Valor |
|---|---|---|
| Qualidade | Altura de camada | **0,20 mm** |
| Qualidade | Altura da primeira camada | **0,20 mm** |
| Resistência | Voltas de parede (paredes) | **2** |
| Resistência | Camadas sólidas superiores (topo) | **5** |
| Resistência | Camadas sólidas inferiores (fundo) | **4** |
| Resistência | Densidade de preenchimento | **15%** |
| Resistência | Padrão de preenchimento | **Grade** (ou o padrão do programa; tanto faz para a estrela) |
| Suporte | Habilitar suporte | **DESLIGADO** |
| Adesão | Borda (brim) | **Desligado** (ligue só se as pontas descolarem, ver Parte 6) |
| Adesão | Saia (skirt) | 1 volta (opcional, ajuda a "limpar" o bico) |

Depois de ajustar, salve como predefinição (ícone de disquete ao lado do nome do perfil) com o nome **"Estrela 0,2"**. Assim não precisa repetir.

### Temperaturas

| | PLA dourado | PETG vermelho / azul |
|---|---|---|
| Bico | **210-220 °C** | **235-245 °C** |
| Mesa | **55-60 °C** | **70-80 °C** |
| Ventoinha da peça | 100% (depois da 1ª camada) | **30-50%** |
| Velocidade | a do perfil | a do perfil, ou 20% mais lenta se sair fio ou bolha |

> Estas faixas são as usuais para cada material, não valores oficiais da Creality para a Hi. Se o perfil de filamento que o programa escolheu já trouxer valores dentro delas, **mantenha os do perfil**. Se o fabricante do seu filamento imprimir outra faixa na caixa ou no rolo, **use a do fabricante**.

### Cuidados específicos de PETG
- **Mesa limpa** com álcool isopropílico antes de cada impressão.
- O PETG gruda forte demais em placa **lisa**. Se a sua placa for lisa (não texturizada), passe uma camada fina de **cola bastão** antes, que funciona como desmoldante. Em placa texturizada não precisa.
- Se sair muito "fiapo" ou estalo no bico, o filamento pode estar úmido. Seque a cerca de 60 °C por 4 a 6 horas (desidratadora ou secador de filamento).

---

## Parte 4 · Fatiar e conferir tempo e peso

1. Clique em **Fatiar placa** (botão no canto inferior direito).
2. O programa troca para a **pré-visualização**. Num quadro de resumo aparecem **tempo estimado** e **filamento usado** (em metros e em gramas).
3. Compare com a referência (15% de preenchimento, camada 0,2 mm):

| Modelo | PLA (dourado) | PETG (verm./azul) | Tempo de referência* |
|---|---|---|---|
| Concêntrica | ~36 g | ~37 g | ~1h20 |
| Vazada Colmeia | ~41 g | ~42 g | ~2h00 |
| Espiral | ~46 g | ~47 g | ~1h30 |
| Facetada 3D | ~52 g | ~53 g | ~1h25-1h40 |

\* O tempo veio do PrusaSlicer com velocidades aproximadas. O Creality Print sabe a velocidade real da Hi e pode mostrar menos ou mais tempo. **O peso deve ficar perto (±10%).** Se der muito mais, por exemplo 80 g, alguma configuração ficou errada (preenchimento ou número de paredes).

4. Na pré-visualização, arraste a barra de camadas (lateral direita) devagar de baixo para cima e veja se:
   - não aparece **nenhuma estrutura de suporte** (normalmente em outra cor);
   - o **furo da haste** aparece como um túnel. Nas últimas camadas, o "teto" do túnel fecha em ponte, e isso é normal.
5. Envie para a impressora (**Imprimir** pela rede, ou **Exportar G-code** para pendrive ou cartão).

---

## Parte 5 · A primeira peça de teste

**Qual imprimir primeiro:** a **Concêntrica em PLA dourado**. É a mais rápida, a mais leve (~36 g) e o PLA é o material mais fácil. Depois, uma **Facetada em PETG vermelho**, para testar o PETG.

Durante a impressão, **fique perto nos primeiros 10 minutos**:
- [ ] A primeira camada está grudando bem, achatada e sem enrolar? Se descolar, pare, limpe a mesa e tente de novo.
- [ ] As pontas finas (principalmente da Espiral e da Vazada) estão grudando?

Quando terminar, espere a mesa esfriar (o PLA solta sozinho; o PETG, às vezes, só com a placa flexionada) e confira:

- [ ] **Peso na balança de cozinha:** perto do da tabela?
- [ ] **Furo da haste:** o teto do furo pode ter ficado com "fios caídos" (é o trecho que foi impresso em ponte). Passe um estilete ou uma lixa enrolada num lápis para limpar.
- [ ] **ENCAIXE NA ÁRVORE (o teste mais importante).** O furo foi desenhado com **15 mm**, mas esse valor é uma **suposição**: nunca foi testado numa árvore de verdade.
  1. Meça a ponta de uma árvore comum. Se tiver paquímetro, melhor; senão, enrole um papel na ponta, marque a volta e divida o comprimento por 3,14.
  2. Encaixe a estrela. Ela deve **entrar sem forçar** e **ficar em pé sem tombar**.
  3. Se ficar **frouxa demais** ou **não entrar**, me avise com a medida da ponta. O furo é um número no script (`FURO_D` em `estrelas/gerar_estrelas.py`) e dá para gerar os arquivos de novo em segundos. **Não publique os anúncios antes deste teste**, ou ajuste o texto do anúncio para a medida real.
- [ ] **Medidas:** confira largura e altura com uma régua. Devem bater com o anúncio (±1 mm).
- [ ] **Aparência:** tire **fotos reais** com luz de janela, em fundo branco (uma folha A3 ou cartolina), e troque as imagens ilustrativas do anúncio assim que puder.
- [ ] **Teste de queda leve:** solte de ~50 cm sobre um tapete. Se alguma ponta quebrar, me avise. Dá para engrossar no arquivo.

---

## Parte 6 · Problemas comuns

| Problema | O que fazer |
|---|---|
| Pontas descolando da mesa | Limpe a mesa com álcool; ligue **Borda (brim)** de 3 mm (depois corte com estilete) |
| Muitos fios entre as partes vazadas (PETG) | Seque o filamento; baixe o bico em 5 °C |
| Teto do furo da haste caído | Normal em pequena quantidade; limpe com estilete. Se fechar o furo, baixe a temperatura e confira se a ventoinha está ligada |
| PETG não solta da mesa | Espere esfriar totalmente e flexione a placa. Da próxima vez, use cola bastão como desmoldante |
| Peso muito acima da tabela | Confira preenchimento 15% e 2 paredes |
| Impressão parou no meio | Veja se o filamento enroscou no carretel |

---

## Parte 7 · Quantas peças o seu estoque rende

Considerando ~95% de aproveitamento do rolo e 10% de margem para falhas (veja a aba "Custo por peça" da planilha):

| Modelo | Dourado (600 g) | Vermelho (1 kg) | Azul (1 kg) |
|---|---|---|---|
| Concêntrica | 14 | 23 | 23 |
| Vazada Colmeia | 12 | 20 | 20 |
| Espiral | 11 | 18 | 18 |
| Facetada 3D | 9 | 16 | 16 |

**Atenção:** o filamento é o mesmo para todos os modelos. Se vender 5 Facetadas douradas, sobra menos dourado para as outras. O **dourado é o gargalo**: com 600 g, dá no total **algo entre 9 e 14 peças douradas**, já descontando os testes.

**Ritmo de produção:** uma peça por vez, ~1h30 cada, mais limpeza e troca. De forma realista, **5 a 8 peças por dia** se você estiver em casa para trocar.
