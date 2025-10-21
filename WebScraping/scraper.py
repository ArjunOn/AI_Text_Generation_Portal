import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = "https://www.scrapethissite.com/pages/simple/"
OUTPUT_CSV = "country_data.csv"


def fetch_page(url):
    headers = {"User-Agent": "python-requests/1.0"}
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        return resp.text
    except requests.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return None


def parse_countries(html):
    soup = BeautifulSoup(html, "html.parser")
    country_divs = soup.find_all("div", class_="col-md-4 country")
    results = []

    for div in country_divs:
        # Name
        name_tag = div.find("h3", class_="country-name")
        name = name_tag.get_text(strip=True) if name_tag else ""

        # Capital
        cap_tag = div.find("span", class_="country-capital")
        capital = cap_tag.get_text(strip=True) if cap_tag else ""

        # Population
        pop_tag = div.find("span", class_="country-population")
        population = pop_tag.get_text(strip=True) if pop_tag else ""

        # Area
        area_tag = div.find("span", class_="country-area")
        area = area_tag.get_text(strip=True) if area_tag else ""

        results.append({
            "Name": name,
            "Capital": capital,
            "Population": population,
            "Area": area,
        })

    return results


def save_to_csv(data, path):
    if not data:
        print("No data to write.")
        return
    df = pd.DataFrame(data)
    # Ensure columns order and presence
    df = df[["Name", "Capital", "Population", "Area"]]
    df.to_csv(path, index=False)
    print(f"Wrote {len(df)} rows to {path}")


def main():
    html = fetch_page(URL)
    if html is None:
        return

    data = parse_countries(html)
    save_to_csv(data, OUTPUT_CSV)


if __name__ == "__main__":
    main()
