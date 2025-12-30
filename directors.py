import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from pathlib import Path

EXPORT_DIR = Path("/Users/samiaibrahim/Downloads/letterboxd-notsadanymore-2025-11-11-21-50-utc")  # <-- set this

WATCHED_CSV = EXPORT_DIR / "watched.csv"
OUT_CSV = EXPORT_DIR / "watched_with_directors.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def extract_directors_from_letterboxd(url: str) -> str:
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    # Letterboxd film pages typically have director links in the "directed by" section
    # This selector is fairly robust:
    director_links = soup.select('a[href^="/director/"]')
    directors = []
    for a in director_links:
        name = a.get_text(strip=True)
        if name and name not in directors:
            directors.append(name)

    return ", ".join(directors)

def main():
    df = pd.read_csv(WATCHED_CSV)

    # Adjust this column name if yours differs:
    # common names: "Letterboxd URI", "URL", "Link"
    url_col = None
    for c in df.columns:
        if c.lower() in ["letterboxd uri", "url", "link"]:
            url_col = c
            break
    if url_col is None:
        raise ValueError(f"Could not find a URL column in watched.csv. Columns: {list(df.columns)}")

    directors = []
    for i, url in enumerate(df[url_col].astype(str).tolist(), start=1):
        try:
            d = extract_directors_from_letterboxd(url)
        except Exception as e:
            d = ""
            print(f"[{i}/{len(df)}] Failed for {url}: {e}")
        directors.append(d)

        # be polite to the site
        time.sleep(0.5)

        if i % 25 == 0:
            print(f"[{i}/{len(df)}] done")

    df["Directors"] = directors
    df.to_csv(OUT_CSV, index=False)
    print(f"Saved: {OUT_CSV}")

if __name__ == "__main__":
    main()
