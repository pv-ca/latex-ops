<div align="center">

[English](../../README.md) · **Português (Brasil)**

# latex-ops

### LaTeX acadêmico com cara de publicado, não de exportado.

[![Agent Skills](https://img.shields.io/badge/Agent_Skills-SKILL.md-5c4ee5?style=flat-square)](https://agentskills.io)
[![Claude Code](https://img.shields.io/badge/Claude_Code-skill-d97757?style=flat-square)](#instalação)
[![Codex](https://img.shields.io/badge/Codex-skill-10a37f?style=flat-square)](#instalação)
[![CI: Linux · Windows](https://github.com/pv-ca/latex-ops/actions/workflows/ci.yml/badge.svg)](https://github.com/pv-ca/latex-ops/actions/workflows/ci.yml)
![Windows · macOS · Linux](https://img.shields.io/badge/Windows_·_macOS_·_Linux-compatível-2f6f8f?style=flat-square)
[![ABNT](https://img.shields.io/badge/ABNT-abnTeX2-009c3b?style=flat-square)](#o-que-vem-incluído)
[![Licença MIT](https://img.shields.io/badge/licença-MIT-f4c430?style=flat-square)](../../LICENSE)

[Instalação](#instalação) · [O que faz](#o-que-faz) · [Exemplos](#exemplos) · [O que vem incluído](#o-que-vem-incluído) · [Requisitos](#requisitos) · [Avaliação](#avaliação) · [Perguntas frequentes](#perguntas-frequentes)

<code>npx skills add https://github.com/pv-ca/latex-ops --skill latex-ops</code>

<br><br>

<img src="../showcase/paper.png" alt="Duas páginas de uma nota de pesquisa feita com latex-ops: teorema, prova, algoritmo, gráfico e tabela" width="760">

</div>

---

Você pede ao seu agente um artigo, um capítulo de tese, notas de aula ou uma lista de exercícios. Ele escreve um LaTeX que compila, diz que o PDF está pronto, e ao abrir você encontra uma tabela saindo da página, um título sozinho no pé da página, um gráfico com a legenda em cima dos dados ou uma citação inventada.

O **latex-ops** é uma [Agent Skill](https://agentskills.io) que muda a forma como o agente trabalha com LaTeX. Ele escolhe uma estrutura de documento e um estilo visual adequados ao leitor, escreve o código com a matemática e a estatística feitas do jeito certo, compila, renderiza as páginas e olha cada uma, corrige o que encontra e diz exatamente o que conferiu. Ele nunca inventa uma citação, um número ou uma exigência que não recebeu.

O foco é o trabalho acadêmico (artigos, artigos de conferência, teses, trabalhos na ABNT, propostas, relatórios, notas de aula, listas de exercícios, pôsteres e apresentações), e ele também cobre os documentos profissionais do seu conjunto de templates. Funciona onde as Agent Skills funcionam, no Windows, no macOS e no Linux.

## Instalação

Com a CLI [`skills`](https://www.npmjs.com/package/skills), que instala no Claude Code, no Codex e nos outros agentes que ela suporta:

```bash
npx skills add https://github.com/pv-ca/latex-ops --skill latex-ops
```

Ou copiando a pasta à mão:

```bash
git clone https://github.com/pv-ca/latex-ops
cp -r latex-ops/skills/latex-ops ~/.claude/skills/      # Claude Code
cp -r latex-ops/skills/latex-ops ~/.agents/skills/      # Codex
```

No Windows, copie `skills\latex-ops` para `%USERPROFILE%\.claude\skills\` ou `%USERPROFILE%\.agents\skills\`. Abra uma sessão nova depois. Você também precisa de uma distribuição TeX: veja [Requisitos](#requisitos); na primeira vez a skill diz o que está faltando.

## O que faz

```text
seu pedido ─▶ escolhe template + preset ─▶ escreve o código ─▶ compila (build.py)
                                                                     │
       relata o que conferiu ◀── corrige e recompila ◀── renderiza e olha (preview.py)
```

- **Duas coordenadas para cada documento.** Um *template funcional* define o que o documento precisa fazer (um artigo de conferência, uma lista de exercícios, uma resposta aos revisores) e um *preset visual* define a aparência (Minimal Research, Tufte Editorial, Kao Textbook…). O kit oficial da revista ou da universidade sempre prevalece sobre os dois.
- **Ciclo fechado.** O agente compila, lê o log, renderiza as páginas e procura os defeitos que o compilador não aponta: tabelas estourando a margem, títulos isolados, páginas quase vazias, legendas sobre os dados, caracteres faltando.
- **Nada inventado.** O que falta fica marcado com `% [CONTENT: ...]` no lugar certo. Citações precisam ser de fontes conferidas. Números de tabelas e gráficos vêm dos seus dados ou de uma fórmula declarada. "Compilou", "conferi" e "acessível" só são ditos quando a verificação aconteceu de fato.
- **Matemática e estatística bem feitas.** Ambientes de equação, deduções alinhadas, sistema de teoremas, operadores declarados, `siunitx`, `pgfplots` lendo CSV, tabelas de regressão geradas pelo seu código de análise, resultados com tamanho de efeito e intervalo de confiança.
- **Consertos sem efeito colateral.** Num build quebrado, ele encontra o arquivo principal, corrige o primeiro erro real com a menor mudança possível, nunca edita arquivos de classe oficiais e mostra o diff.

## Exemplos

Todos foram feitos com a skill, compilados e conferidos página por página. Os fontes estão em [`examples/`](../../examples/).

| Lista de exercícios com gabarito no mesmo arquivo | Proposta de pesquisa com orçamento ainda não definido |
| --- | --- |
| <img src="../showcase/problem-set.png" alt="Lista de exercícios" width="380"> | <img src="../showcase/proposal.png" alt="Proposta de pesquisa" width="380"> |

<img src="../showcase/slides.png" alt="Apresentação em Beamer" width="760">

Pedidos que você pode fazer:

```text
Monte a estrutura do meu TCC nas normas ABNT com capa, folha de rosto, resumo e abstract.
```
```text
Formate este artigo no template de conferência do IEEE e me diga quais requisitos ainda não atende.
```
```text
Escreva notas de aula sobre a desigualdade de Cauchy–Schwarz com a prova completa, dois exemplos e três exercícios.
```
```text
Aqui está o resultados.csv. Faça um relatório estatístico de duas páginas com tabela de regressão e gráfico de dispersão.
```
```text
Minha tese parou de compilar depois que coloquei o fontspec. Conserta sem mexer no resto.
```

## O que vem incluído

| Área | Templates |
| --- | --- |
| Pesquisa | Artigo de pesquisa · Artigo de conferência (revisão e versão final) · Revisão de literatura · Proposta de pesquisa · Resposta aos revisores · Pôster científico |
| Teses | Tese clássica · Tese técnica · **Trabalho acadêmico ABNT** com abnTeX2 (TCC, monografia, dissertação, tese) |
| Dados e laboratório | Relatório estatístico (pgfplots a partir de CSV) · Relatório de laboratório (unidades e incerteza) |
| Ensino | Notas de aula (sistema de teoremas) · Lista de exercícios (chave de gabarito) · Plano de curso · Relatório de avaliação · Livro / guia |
| Profissional | Currículo · Carta formal · Resumo executivo · Memorando · Proposta · Fatura e orçamento · Contrato · Ata de reunião · Manual técnico · POP · Referência de uma página · Formulário · Revista · Folheto · Portfólio |
| Presets visuais | Minimal Research · Classic Editorial · Tufte Editorial · Kao Textbook · Swiss Minimal · Modern Report · Legal Minimal · Magazine Editorial · Minimal Beamer |

São 31 templates de documento e 9 presets, cada um um `.tex` que compila e serve de referência: o agente adapta, não copia.

| Referência que o agente lê quando precisa | Cobre |
| --- | --- |
| [`design-rules.md`](../../skills/latex-ops/references/design-rules.md) | Tipografia, classes e pacotes, componentes, acessibilidade, artigos acadêmicos e kits de revistas, Beamer |
| [`math.md`](../../skills/latex-ops/references/math.md) | Fontes e motores, ambientes de equação, alinhamento, notação, teoremas, matrizes, unidades, algoritmos, gráficos, conferência das contas, erros comuns |
| [`statistics.md`](../../skills/latex-ops/references/statistics.md) | De onde vêm os números, relato de testes e modelos, tabelas alinhadas na vírgula decimal, tabelas de regressão, gráficos estatísticos |
| [`integrations.md`](../../skills/latex-ops/references/integrations.md) | Python, R, Julia, Quarto, Pandoc, sistemas de diagramas TikZ, Overleaf |
| [`platforms.md`](../../skills/latex-ops/references/platforms.md) | TeX Live, TinyTeX, MiKTeX, pacotes do Linux, particularidades do Windows, fontes |

| Script (Python 3.8+, só biblioteca padrão) | Faz |
| --- | --- |
| `check_env.py` | Detecta a distribuição, os motores, o latexmk, o renderizador de PDF e os pacotes que faltam; `--install` mostra o comando de instalação e `--install --yes` executa depois que você concorda |
| `build.py arquivo.tex` | Compila com latexmk, ou com o motor mais biber/bibtex até as referências estabilizarem; shell escape desligado; mostra erros com arquivo e linha, referências indefinidas, caracteres faltando e caixas estouradas |
| `preview.py arquivo.pdf --pages 1-3` | Converte páginas em PNG com pdftoppm, mutool ou Ghostscript para o agente poder olhar |

## Requisitos

- Uma distribuição TeX com LuaLaTeX: **TeX Live** ou **TinyTeX** recomendados; **MiKTeX** funciona.
- Python 3.8 ou mais novo para os scripts.

A skill roda o `check_env.py` na primeira vez e quando um build falha por motivo externo ao documento, e diz o que fazer:

| Você tem | Ela sugere |
| --- | --- |
| Nenhum TeX | [TinyTeX](https://yihui.org/tinytex) (por usuário, sem precisar de administrador) e depois `tlmgr install` dos pacotes listados |
| TeX Live ou TinyTeX | `tlmgr install <pacotes que faltam>` |
| MiKTeX | `miktex packages install <pacotes que faltam>`, mais o Strawberry Perl para o latexmk |
| TeX Live do apt, dnf, pacman ou zypper | O comando do sistema correspondente (ela nunca roda `sudo` por conta própria) |

Nada é instalado sem a sua confirmação. A lista completa de pacotes está em [`assets/requirements.txt`](../../skills/latex-ops/assets/requirements.txt); o CI instala exatamente essa lista no Linux e no Windows e compila todos os templates e exemplos.

## Avaliação

Quatro pedidos foram executados uma vez por um agente com a skill e uma vez sem ela, e avaliados em 33 critérios verificáveis: consertar um build com `fontspec` quebrado pelo motor errado, um erro de fonte do MiKTeX no Windows, notas de aula com uma prova e a estrutura de um TCC na ABNT.

| | Com latex-ops | Sem |
| --- | --- | --- |
| Critérios atendidos | 33 / 33 | 30 / 33 |
| Tempo médio por tarefa | 77 s | 50 s |
| Tokens médios por tarefa | 64 mil | 49 mil |

O modelo base já é bom em LaTeX: as duas versões compilaram os três documentos produzidos e não inventaram nada. A diferença foi o ciclo de verificação. Sem a skill, o agente não olhou as páginas renderizadas em nenhuma das três tarefas que produziram documento, então problemas de layout chegariam ao usuário sem ninguém ver. A skill custa cerca de meio minuto e 15 mil tokens a mais por tarefa. Foi uma rodada por configuração, então trate como um primeiro sinal, não como benchmark; os pedidos estão em [`evals/evals.json`](../../skills/latex-ops/evals/evals.json).

## Perguntas frequentes

<details>
<summary><strong>Em quais agentes funciona?</strong></summary>

Em qualquer ambiente que carregue Agent Skills (uma pasta com um `SKILL.md`): Claude Code, Codex e os agentes suportados pela CLI `skills`. Os scripts são Python puro e rodam do mesmo jeito em todos.
</details>

<details>
<summary><strong>Ela usa o template da minha revista ou universidade?</strong></summary>

Sim, e esse template prevalece. A skill pede (ou baixa da página oficial) o kit de autor da revista, do ano e da fase, migra o conteúdo para ele e relata cada requisito como atendido, não atendido ou não verificado. Ela nunca reescreve um arquivo de classe de memória e nunca reduz fonte ou margem para caber no limite de páginas.
</details>

<details>
<summary><strong>Ela escreve o trabalho por mim?</strong></summary>

Ela escreve e estrutura o que você fornece e pode redigir o texto que você pedir, mas não inventa resultados, dados, citações nem afirmações. Onde falta algo, deixa um marcador visível `[CONTENT: ...]` para nada fabricado escapar para uma submissão.
</details>

<details>
<summary><strong>Funciona com o Overleaf?</strong></summary>

O agente trabalha com arquivos no seu computador. Ele pode preparar um projeto completo para subir no Overleaf ou trabalhar num projeto que você baixou de lá, respeitando o compilador escolhido no menu do Overleaf.
</details>

<details>
<summary><strong>Funciona em português e outras línguas?</strong></summary>

Sim. Os documentos usam o `babel` para a língua e a hifenização; o template ABNT é em português. O agente responde na sua língua.
</details>

<details>
<summary><strong>Ela executa código dos meus documentos?</strong></summary>

Não por padrão: os builds rodam com shell escape desligado. Recursos que precisam dele (`minted`, PythonTeX, externalização do TikZ) só são ativados quando você pede, e o agente avisa que o documento vai executar programas.
</details>

## Desenvolvimento

```bash
python3 -m unittest discover -s tests       # testes dos scripts
python3 tests/build_templates.py            # compila todos os templates e exemplos
```

Issues e pull requests são bem-vindos. Um template novo precisa compilar só com os pacotes de `requirements.txt` (acrescente os que ele usar) e vir com uma entrada em `references/functional-templates.md`.

## Licença

[MIT](../../LICENSE)
