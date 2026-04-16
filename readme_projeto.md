# Web Scraping Esportivo - Transfermarkt

Projeto desenvolvido para a disciplina de **Linguagem de Programação II** da **Fatec Rio Claro**.

O script acessa o site Transfermarkt e extrai automaticamente dados dos elencos de times de futebol, salvando as informações em arquivos `.csv` para análise.

---

## O que o script coleta

Para cada jogador de cada time configurado, o script extrai:

- Nome completo  
- Posição  
- Idade  
- Nacionalidade  
- Valor de mercado  

---

## Times configurados (padrão)

- Flamengo  
- Palmeiras  
- Corinthians  

Você pode adicionar ou trocar times editando a lista `TIMES` no início do script.

---

## Tecnologias utilizadas

- requests → Download das páginas web  
- beautifulsoup4 → Análise e extração do HTML  
- csv → Gravação dos dados coletados  
- os / sys → Gerenciamento do ambiente  

---

## Estrutura do projeto

projeto/
│
├── transfermarkt_scraper.py
├── requirements.txt
└── dados_esportivos/
    ├── flamengo_elenco.csv
    ├── palmeiras_elenco.csv
    └── corinthians_elenco.csv

---

## Como executar

1. Clone ou baixe os arquivos do projeto

2. Execute o script:

python transfermarkt_scraper.py

Ou instale manualmente:

pip install -r requirements.txt
python transfermarkt_scraper.py

---

## Observações

- O site Transfermarkt exige um User-Agent na requisição  
- O método raise_for_status() trata erros HTTP  
- Os dados variam conforme a temporada  

---

## Autor

Projeto acadêmico - Fatec Rio Claro
