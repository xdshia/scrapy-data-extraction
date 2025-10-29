# scrapy_spider.py
# Optional Scrapy spider for direct API endpoints. Use when you have a known JSON API URL.
import scrapy

class MapApiSpider(scrapy.Spider):
    name = "map_api"

    def __init__(self, api_url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not api_url:
            raise ValueError("Please provide -a api_url=<URL>")
        self.start_urls = [api_url]

    def parse(self, response):
        data = response.json()
        # attempt to find items
        items = None
        for key in ("items", "results", "data", "places"):
            if isinstance(data, dict) and key in data:
                items = data.get(key)
                break
        if not items and isinstance(data, list):
            items = data

        if not items:
            return

        for item in items:
            yield {
                "name": item.get("title") or item.get("name"),
                "address": item.get("address"),
                "lat": item.get("location", {}).get("y") if isinstance(item.get("location"), dict) else None,
                "lon": item.get("location", {}).get("x") if isinstance(item.get("location"), dict) else None,
                "category": item.get("type") or item.get("category"),
            }
