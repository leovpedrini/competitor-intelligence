# Competitor Intelligence

Este projeto foi desenvolvido para realizar análise e engenharia reversa de conteúdo no YouTube.

A ideia central é coletar dados públicos de canais e vídeos, estruturar essas informações em planilhas e identificar padrões de desempenho, formatos, temas e estratégias de conteúdo que estão gerando mais alcance, engajamento e retenção.

## Objetivo

O projeto ajuda a responder perguntas como:

- Quais vídeos de um canal têm melhor performance?
- Qual tipo de conteúdo gera mais visualizações por dia?
- Como o canal publica e quando os vídeos são mais bem recebidos?
- Quais títulos, formatos, durações e temas parecem funcionar melhor?
- Como estudar a estratégia de concorrentes e aplicar aprendizados em conteúdo próprio?

Em outras palavras, este projeto funciona como uma ferramenta de inteligência competitiva para análise de conteúdo no YouTube, permitindo fazer engenharia reversa de estratégias de canais e criadores.

## Funcionalidades

- Busca de canal por handle do YouTube
- Coleta dos vídeos do canal
- Extração de metadados como:
  - título
  - descrição
  - data de publicação
  - tags
  - duração
  - thumbnail
  - visualizações
  - likes
  - comentários
- Cálculo de métricas como:
  - views per day
  - engagement rate
  - like rate
  - comment rate
  - dias online
- Exportação dos dados para CSV
- Organização em pasta de saída para análise posterior

## Estrutura do projeto

```text
competitor-intelligence/
├── collector.py
├── requirements.txt
├── .env
├── README.md
├── output/
└── ...
```

## Requisitos

- Python 3.10+
- Chave de API do YouTube Data API v3
- Arquivo `.env` com as variáveis necessárias

## Configuração

1. Crie um ambiente virtual (opcional, mas recomendado):

```bash
python -m venv .venv
```

2. Ative o ambiente virtual:

Windows (PowerShell):

```powershell
.\.venv\Scripts\Activate.pshell
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Crie um arquivo `.env` com a seguinte estrutura:

```env
YOUTUBE_API_KEY=sua_chave_aqui
YOUTUBE_HANDLE=@dr.biogas
```

- `YOUTUBE_API_KEY`: sua chave da API do YouTube
- `YOUTUBE_HANDLE`: handle do canal que será analisado

## Como executar

```bash
py collector.py
```

O script busca os vídeos do canal informado, coleta os dados e salva a saída em `output/` em formato CSV.

## Saída

Os arquivos gerados ficam na pasta `output/` com nome no formato:

```text
output/youtube_dr.biogas_2026-09-26_21-42.csv
```

Esses dados podem ser abertos em Excel, Google Sheets ou importados em ferramentas de análise para identificar padrões de conteúdo.

## Casos de uso

Este projeto é útil para:

- análise de concorrência
- benchmarking de canais
- estudos de conteúdo e storytelling
- identificação de formatos de vídeo que geram maior engajamento
- pesquisa de tendências e comportamento de audiência
- engenharia reversa de estratégias de criadores de conteúdo

## Observação

Este projeto coleta dados públicos disponíveis via API do YouTube e é destinado apenas para fins de análise e pesquisa de conteúdo. Sempre respeite os termos de uso da plataforma e os limites de acesso da API.

## Licença

Este projeto está sendo usado para fins de pesquisa, análise e aprendizagem prática em engenharia reversa de conteúdo digital.
