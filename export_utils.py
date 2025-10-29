# export_utils.py
import json
import pandas as pd
from datetime import datetime
import os
import time

def save_to_excel(data, filename):
    if not data:
        print("❌ No data to save")
        return
    
    try:
        # Create DataFrame with all possible columns
        df = pd.DataFrame(data)
        
        # Reorder columns for better readability
        preferred_order = ['name', 'english_name', 'address', 'rating', 'reviews', 'category', 'latitude', 'longitude', 'image_url', 'url']
        
        # Get existing columns in preferred order, then remaining columns
        existing_columns = [col for col in preferred_order if col in df.columns]
        remaining_columns = [col for col in df.columns if col not in preferred_order]
        final_columns = existing_columns + remaining_columns
        
        df = df[final_columns]
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Try to save with retry logic in case of file locks
        max_retries = 3
        for attempt in range(max_retries):
            try:
                df.to_excel(filename, index=False, engine='openpyxl')
                print(f"✅ Saved {len(data)} items to {filename}")
                return
            except PermissionError:
                if attempt < max_retries - 1:
                    print(f"⚠️ File {filename} is busy, retrying in 2 seconds... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(2)
                else:
                    # Try with a different filename
                    base, ext = os.path.splitext(filename)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    new_filename = f"{base}_{timestamp}{ext}"
                    df.to_excel(new_filename, index=False, engine='openpyxl')
                    print(f"✅ Saved {len(data)} items to {new_filename} (original file was busy)")
                    return
            except Exception as e:
                print(f"❌ Error saving to Excel: {str(e)}")
                # Try to save as CSV as fallback
                try:
                    csv_filename = filename.replace('.xlsx', '.csv')
                    df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
                    print(f"✅ Saved {len(data)} items to CSV fallback: {csv_filename}")
                    return
                except Exception as csv_error:
                    print(f"❌ Could not save as CSV either: {str(csv_error)}")
                    raise
    
    except Exception as e:
        print(f"❌ Failed to save Excel file: {str(e)}")

def save_to_json(data, filename):
    if not data:
        print("❌ No data to save")
        return
        
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ Saved {len(data)} items to {filename}")
    except Exception as e:
        print(f"❌ Error saving to JSON: {str(e)}")
        # Try with a different filename
        try:
            base, ext = os.path.splitext(filename)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_filename = f"{base}_{timestamp}{ext}"
            with open(new_filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"✅ Saved {len(data)} items to JSON fallback: {new_filename}")
        except Exception as fallback_error:
            print(f"❌ Could not save JSON file at all: {str(fallback_error)}")