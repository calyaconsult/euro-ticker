"""
update_ticker.py
Ergänzt eurchf-history.json mit den neuesten Kursen aus dem EZB-RSS-Feed.

Crontab-Eintrag (Mo-Fr um 16:15 Uhr):
  15 16 * * 1-5 /usr/bin/python3 /path/to/update_ticker.py
"""

import json
import re
import urllib.request

RSS_URL = "https://www.ecb.europa.eu/rss/fxref-chf.html"
JSON_FILE = "eurchf-history.json"


def fetch_rss():
    """RSS-Feed abrufen und Kurse aus den rdf:resource-URLs extrahieren."""
    response = urllib.request.urlopen(RSS_URL)
    content = response.read().decode("utf-8")

    pattern = r"date=([\d-]+)&amp;rate=([\d.]+)"
    matches = re.findall(pattern, content)

    return [{"date": date, "rate": float(rate)} for date, rate in matches]


def update_json(new_entries):
    """Bestehende JSON-Datei laden, neue Einträge ergänzen, speichern."""
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    existing_dates = {entry["date"] for entry in data}
    added = 0

    for entry in new_entries:
        if entry["date"] not in existing_dates:
            data.append(entry)
            added += 1

    data.sort(key=lambda x: x["date"])

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)

    print(f"✅ {added} neue Kurse ergänzt. Total: {len(data)} Datenpunkte.")
    if added > 0:
        latest = data[-1]
        print(f"📈 Aktuell: {latest['date']} → 1 EUR = {latest['rate']} CHF")


if __name__ == "__main__":
    entries = fetch_rss()
    update_json(entries)
