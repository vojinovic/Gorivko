import requests
from bs4 import BeautifulSoup

def get_fuel_prices():
    url = 'https://goriva.info/srbija'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table')
    rows = table.find_all('tr')

    prices = {}
    for row in rows:
        cells = row.find_all('td')
        if len(cells) >= 2:
            fuel_type = cells[0].get_text(strip=True)
            price_rsd = cells[1].get_text(strip=True).replace(' RSD', '').replace(',', '.')
            try:
                price_rsd = float(price_rsd)
                price_eur = round(price_rsd / 117.0, 2)
                prices[fuel_type] = price_eur
            except ValueError:
                continue

    return prices

def update_html(prices):
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    html = html.replace('1.60', f"{prices.get('BMB 95', 1.60):.2f}")
    html = html.replace('1.68', f"{prices.get('Dizel', 1.68):.2f}")
    html = html.replace('0.85', f"{prices.get('TNG / Auto Gas', 0.85):.2f}")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == "__main__":
    prices = get_fuel_prices()
    print(\"Aktuelne cene (EUR):\", prices)
    update_html(prices)
