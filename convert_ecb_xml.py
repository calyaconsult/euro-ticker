"""
convert_ecb_xml.py
Konvertiert die EZB-Datei chf.xml (SDMXML-Format) in eine JSON-Datei.

Verwendung:
  1. XML herunterladen:
     curl -o chf.xml "https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/chf.xml"
  2. Skript ausführen:
     python convert_ecb_xml.py
"""

import xml.etree.ElementTree as ET
import json

INPUT_FILE = "chf.xml"
OUTPUT_FILE = "eurchf-history.json"


def convert():
    tree = ET.parse(INPUT_FILE)
    root = tree.getroot()

    data = []

    for elem in root.iter():
        if elem.tag.endswith("Obs") or elem.tag == "Obs":
            time_period = elem.get("TIME_PERIOD")
            obs_value = elem.get("OBS_VALUE")
            if time_period and obs_value:
                data.append({
                    "date": time_period,
                    "rate": float(obs_value)
                })

    data.sort(key=lambda x: x["date"])

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)

    print(f"✅ {len(data)} Datenpunkte konvertiert: {data[0]['date']} bis {data[-1]['date']}")
    print(f"📁 Gespeichert als: {OUTPUT_FILE}")


if __name__ == "__main__":
    convert()
