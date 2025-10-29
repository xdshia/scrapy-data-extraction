# main.py
from playwright_scraper import scrape_google_maps_places
from export_utils import save_to_excel, save_to_json
import os
import sys

def main():
    try:
        q = input("Enter Google Maps search query (e.g. رستوران تهران) or leave empty for 'رستوران تهران': ").strip() or "رستوران تهران"
        
        print(f"🔍 Searching for '{q}' on Google Maps...")
        items = scrape_google_maps_places(q)
        
        if not items:
            print("❌ No items found.")
            return
        
        # Create outputs directory
        os.makedirs("outputs", exist_ok=True)
        fname_base = q.replace(" ", "_")
        
        # Clean filename for Windows
        clean_fname_base = "".join(c for c in fname_base if c.isalnum() or c in ('_', '-')).rstrip()
        
        excel_filename = f"outputs/{clean_fname_base}_google_maps.xlsx"
        json_filename = f"outputs/{clean_fname_base}_google_maps.json"
        
        # Save to files
        save_to_excel(items, excel_filename)
        save_to_json(items, json_filename)
        
        print(f"✅ Data saved to:")
        print(f"   📊 Excel: {excel_filename}")
        print(f"   📁 JSON: {json_filename}")
        
        # Show summary
        print(f"\n📈 Summary:")
        print(f"   Total places found: {len(items)}")
        if items:
            print(f"   First 3 places:")
            for i, item in enumerate(items[:3], 1):
                print(f"   {i}. {item['name']}")
                if item.get('rating'):
                    print(f"      Rating: {item['rating']}" + (f" ({item['reviews']} reviews)" if item.get('reviews') else ""))
    
    except KeyboardInterrupt:
        print("\n⏹️ Operation cancelled by user")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        print("💡 Try closing any open Excel files and run again")

if __name__ == "__main__":
    main()