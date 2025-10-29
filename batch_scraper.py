# batch_scraper.py
# Runs multiple queries and outputs combined Excel/JSON.
from playwright_scraper import scrape_neshan_places
from export_utils import save_to_excel, save_to_json
import os

QUERIES = [
    "رستوران تهران",
    "کافی شاپ تهران",
    "داروخانه تهران",
    "مدرسه تهران"
]

ALL = []
for q in QUERIES:
    print("\n======================")
    print(f"Scraping: {q}")
    items = scrape_neshan_places(q, timeout=12)
    ALL.extend(items)

os.makedirs("outputs", exist_ok=True)
save_to_excel(ALL, "outputs/batch_places.xlsx")
save_to_json(ALL, "outputs/batch_places.json")
print("Batch finished.")
