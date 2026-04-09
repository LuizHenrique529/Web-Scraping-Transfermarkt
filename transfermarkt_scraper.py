import subprocess
import sys
import os

try:
    import requests
    import bs4
except ImportError:
    print("instalando dependencias...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "beautifulsoup4"])
    os.execv(sys.executable, [sys.executable] + sys.argv)

import csv

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (Chrome/124.0 Safari/537.36)"
}

TIMES = [
    {
        "nome": "Flamengo",
        "url": "https://www.transfermarkt.com.br/clube-de-regatas-do-flamengo/kader/verein/614"
    },
    {
        "nome": "Palmeiras",
        "url": "https://www.transfermarkt.com.br/sociedade-esportiva-palmeiras/kader/verein/1023"
    },
    {
        "nome": "Corinthians",
        "url": "https://www.transfermarkt.com.br/sport-club-corinthians-paulista/kader/verein/199"
    }
]

PASTA = "dados_esportivos"

if not os.path.exists(PASTA):
    os.makedirs(PASTA)


def scrape_elenco(time):
    print(f"\n--- buscando elenco: {time['nome']} ---")

    res = requests.get(time["url"], headers=HEADERS)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, "html.parser")

    jogadores = []

    linhas = soup.select("table.items tbody tr")

    for linha in linhas:

        if "spacer" in linha.get("class", []) or "bg_Extrazeile" in linha.get("class", []):
            continue

        colunas = linha.select("td")
        if len(colunas) < 5:
            continue

        nome_tag = linha.select_one("td.hauptlink a")
        nome = nome_tag.text.strip() if nome_tag else "N/A"

        posicao_tag = linha.select_one("td.posrela table tr:nth-child(2) td")
        posicao = posicao_tag.text.strip() if posicao_tag else "N/A"

        idade = "N/A"
        for td in colunas:
            texto = td.text.strip()
            if texto.isdigit() and 15 <= int(texto) <= 45:
                idade = texto
                break

        nac_tag = linha.select_one("td.zentriert img.flaggenrahmen")
        nacionalidade = nac_tag.get("title", "N/A") if nac_tag else "N/A"

        valor_tag = linha.select_one("td.rechts.hauptlink a")
        valor = valor_tag.text.strip() if valor_tag else "N/A"

        jogadores.append({
            "nome": nome,
            "posicao": posicao,
            "idade": idade,
            "nacionalidade": nacionalidade,
            "valor_mercado": valor
        })

        print(f"  {nome} | {posicao} | {idade} anos | {nacionalidade} | {valor}")

    return jogadores


def salvar_csv(time_nome, jogadores):
    nome_arquivo = os.path.join(PASTA, f"{time_nome.lower()}_elenco.csv")

    with open(nome_arquivo, "w", newline="", encoding="utf-8") as f:
        campos = ["nome", "posicao", "idade", "nacionalidade", "valor_mercado"]
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(jogadores)

    print(f"  salvo em: {nome_arquivo}")


total_jogadores = 0

for time in TIMES:
    jogadores = scrape_elenco(time)
    if jogadores:
        salvar_csv(time["nome"], jogadores)
        total_jogadores += len(jogadores)

print(f"\nfim! {total_jogadores} jogadores coletados no total.")
print(f"arquivos salvos na pasta '{PASTA}/'")
