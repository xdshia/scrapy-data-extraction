# playwright_scraper.py
from playwright.sync_api import sync_playwright
import time
import re
import pandas as pd

def scrape_google_maps_places(query="رستوران تهران", timeout=30):
    data = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context(
            viewport={"width": 1200, "height": 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        page = context.new_page()
        
        print("🌍 Opening https://www.google.com/maps ...")
        page.goto("https://www.google.com/maps", timeout=60000)
        time.sleep(5)

        # Handle cookie consent popup
        print("🍪 Handling cookie consent...")
        consent_handled = False
        
        consent_selectors = [
            'button:has-text("Accept all")',
            'button:has-text("Alle akzeptieren")',
            'button:has-text("Alles akzeptieren")',
            'button:has-text("Ich stimme zu")',
            'button:has-text("I agree")',
            'button:has-text("Agree")',
            '[aria-label*="Accept"]',
            '[aria-label*="Akzeptieren"]',
            'button.jsb',
            'form:has(button) button',
            'div[class*="consent"] button',
            'button:has-text("Reject all")',
            'button:has-text("Alle ablehnen")',
        ]
        
        for selector in consent_selectors:
            try:
                consent_button = page.query_selector(selector)
                if consent_button and consent_button.is_visible():
                    consent_button.click()
                    print(f"✅ Clicked consent button: {selector}")
                    consent_handled = True
                    time.sleep(3)
                    break
            except Exception as e:
                continue

        if not consent_handled:
            print("⚠️ No consent button found or clickable, continuing anyway...")
        
        try:
            page.mouse.click(100, 100)
            time.sleep(2)
            
            for selector in consent_selectors:
                try:
                    consent_button = page.query_selector(selector)
                    if consent_button and consent_button.is_visible():
                        consent_button.click()
                        print(f"✅ Clicked consent button after interaction: {selector}")
                        time.sleep(2)
                        break
                except:
                    continue
        except:
            pass

        print(f"🔍 Searching for '{query}' ...")
        
        # Find and use the Google Maps search box
        search_input = None
        search_selectors = [
            'input[placeholder*="Search Google Maps"]',
            'input[placeholder*="جستجو"]',
            'input[id="searchboxinput"]',
            'input[class*="searchbox"]',
            'input[type="text"]',
            '#searchboxinput',
        ]
        
        for selector in search_selectors:
            try:
                search_input = page.wait_for_selector(selector, timeout=10000)
                if search_input:
                    print(f"✅ Found search input with: {selector}")
                    break
            except:
                continue

        if not search_input:
            print("❌ Could not find Google Maps search box")
            page.reload()
            time.sleep(5)
            for selector in consent_selectors[:3]:
                try:
                    consent_button = page.query_selector(selector)
                    if consent_button:
                        consent_button.click()
                        time.sleep(2)
                        break
                except:
                    continue
            for selector in search_selectors:
                try:
                    search_input = page.query_selector(selector)
                    if search_input:
                        break
                except:
                    continue

        if not search_input:
            print("❌ Still could not find search box after retry")
            browser.close()
            return []

        # Perform search
        search_input.click()
        search_input.fill("")
        time.sleep(1)
        search_input.fill(query)
        time.sleep(2)
        
        # Press Enter or click search button
        search_button_selectors = [
            'button[id="searchbox-searchbutton"]',
            'button[class*="searchbox-searchbutton"]',
            'button:has-text("Search")',
            'button:has-text("جستجو")',
            '#searchbox-searchbutton',
        ]
        
        search_button = None
        for selector in search_button_selectors:
            try:
                search_button = page.query_selector(selector)
                if search_button and search_button.is_visible():
                    search_button.click()
                    print(f"✅ Clicked search button: {selector}")
                    break
            except:
                continue
        
        if not search_button:
            print("⚠️ No search button found, pressing Enter...")
            page.keyboard.press("Enter")

        print("⏳ Waiting for search results to load...")
        time.sleep(8)

        # Wait for results panel
        try:
            page.wait_for_selector('[role="feed"], [aria-label*="Results for"], [class*="section-result"]', timeout=15000)
            print("✅ Results panel loaded")
        except:
            print("⚠️ Results panel loading slowly, continuing anyway...")

        # Scroll to load more results
        print("🔄 Scrolling to load more results...")
        results_container = page.query_selector('[role="feed"]')
        
        for i in range(15):
            if results_container:
                results_container.evaluate("element => element.scrollTop = element.scrollHeight")
            else:
                page.mouse.wheel(0, 800)
            time.sleep(1.5)
            
            end_indicator = page.query_selector('div:has-text("You\'ve reached the end of the list"), div:has-text("Ende der Liste")')
            if end_indicator:
                print("📄 Reached end of results")
                break

            if i % 5 == 0:
                print(f"   ... Scrolled {i+1} times")

        time.sleep(3)

        # Find all place cards
        print("🔍 Looking for place cards...")
        
        card_selectors = [
            '[role="feed"] > div > div',
            '[class*="section-result"]',
            '[class*="place-result"]',
            '[class*="search-result"]',
            'a[href*="/place/"]',
            'a[href*="/maps/place/"]',
            'div[class*="result-container"]'
        ]
        
        all_cards = []
        for selector in card_selectors:
            cards = page.query_selector_all(selector)
            if cards:
                print(f"🔍 Found {len(cards)} elements with selector: {selector}")
                all_cards.extend(cards)
        
        # Remove duplicates
        unique_cards = []
        seen_handles = set()
        for card in all_cards:
            handle = str(card)
            if handle not in seen_handles:
                seen_handles.add(handle)
                unique_cards.append(card)

        print(f"📦 Processing {len(unique_cards)} unique cards...")

        for i, card in enumerate(unique_cards):
            try:
                # Get card text content
                text = card.inner_text().strip()
                
                if not text or len(text) < 10:
                    continue
                
                # Skip promotional or irrelevant content
                skip_patterns = [
                    "Sponsored", "Promoted", "Ads", "Advertisement",
                    "You've reached", "end of list", "©", "Feedback",
                    "Werbung", "Anzeige"
                ]
                
                if any(pattern.lower() in text.lower() for pattern in skip_patterns):
                    continue
                
                lines = [line.strip() for line in text.split('\n') if line.strip()]
                
                if len(lines) < 2:
                    continue
                
                # Extract data from Google Maps structure
                # Look for Persian name first - improved logic
                persian_name = None
                english_name = None
                
                # Common patterns that indicate this is NOT a name
                not_name_patterns = [
                    '·', 'Restaurant ·', 'Cafe ·', 'Hotel ·', 'Store ·',
                    'خیابان', 'کوچه', 'بلوار', 'میدان', 'جنوبی', 'شمالی', 'شرقی', 'غربی',
                    'Street', 'Avenue', 'St', 'Ave', 'Rd', 'Road', 'Lane',
                    'Ally', 'Alley', 'Boulevard', 'Square'
                ]
                
                # Address-like patterns (usually contain specific formats)
                address_patterns = [
                    r'[A-Z]{2,3}\d+\+[A-Z]{2,3}',  # Like QC5J+HPX
                    r'\d+\.\d+',  # Coordinates
                    r'[NSEW]\d+',  # Direction indicators
                ]
                
                # First, try to find the actual name by excluding address-like lines
                candidate_names = []
                for line in lines:
                    # Skip lines that are clearly not names
                    is_address_like = (
                        any(pattern in line for pattern in not_name_patterns) or
                        any(re.search(pattern, line) for pattern in address_patterns) or
                        '·' in line or  # Often used as separator in addresses
                        len(line) > 50 or  # Too long to be a name
                        (re.search(r'\d{3,}', line) and len(line) < 30)  # Contains multiple digits but short
                    )
                    
                    if not is_address_like:
                        candidate_names.append(line)
                
                # Prioritize Persian names from candidates
                for name_candidate in candidate_names:
                    if re.search(r'[\u0600-\u06FF]', name_candidate):  # Persian script
                        # Additional check to ensure it's not an address
                        if not any(indicator in name_candidate for indicator in ['خیابان', 'کوچه', 'بلوار', 'میدان']):
                            persian_name = name_candidate
                            break
                
                # If no Persian name found in candidates, try the first line that's not obviously an address
                if not persian_name:
                    for line in lines:
                        if (re.search(r'[\u0600-\u06FF]', line) and  # Has Persian
                            not any(pattern in line for pattern in not_name_patterns) and  # Not address-like
                            len(line) < 40):  # Reasonable length for a name
                            persian_name = line
                            break
                
                # Last resort: use first line if it's not obviously an address
                if not persian_name and lines:
                    first_line = lines[0]
                    if not any(pattern in first_line for pattern in not_name_patterns):
                        persian_name = first_line
                
                # Look for English name
                for line in lines:
                    if (re.search(r'[a-zA-Z]', line) and 
                        not re.search(r'[\u0600-\u06FF]', line) and
                        len(line) > 2 and
                        len(line) < 40 and
                        not any(word in line.lower() for word in ['street', 'avenue', 'st', 'ave', 'road', 'rd', 'ally', 'alley']) and
                        not any(pattern in line for pattern in not_name_patterns)):
                        english_name = line
                        break
                
                # If we still don't have a name, skip this card
                if not persian_name:
                    continue
                
                name = persian_name
                
                # Skip if name is obviously not a place
                if len(name) < 2 or name.isdigit():
                    continue
                
                address = None
                rating = None
                reviews = None
                category = None
                
                # Look for rating
                for line in lines:
                    rating_match = re.search(r'(\d+\.?\d*)\s*(?:\(|⭐|★|stars?)', line)
                    if rating_match:
                        rating = rating_match.group(1)
                        reviews_match = re.search(r'\(([\d,]+)\s*(?:review|نظر|Bewertungen?)', line)
                        if reviews_match:
                            reviews = reviews_match.group(1)
                        break
                    elif '⭐' in line or '★' in line:
                        num_match = re.search(r'(\d+\.?\d*)', line)
                        if num_match:
                            rating = num_match.group(1)
                        else:
                            rating = line
                        break
                
                # Look for address - specifically look for address patterns
                address_indicators = [
                    'خیابان', 'کوچه', 'بلوار', 'میدان', 'تهران', 'ایران',
                    'Street', 'Avenue', 'St', 'Ave', 'Rd', 'Road', 'Lane', 'Ally', 'Alley',
                    'Straße', 'Allee', 'Platz'
                ]
                
                # Look for lines that contain address indicators
                for line in lines:
                    if any(indicator in line for indicator in address_indicators):
                        address = line
                        break
                
                # Also look for coordinate patterns or long descriptive lines
                if not address:
                    for line in lines:
                        if (len(line) > 30 or 
                            any(re.search(pattern, line) for pattern in address_patterns) or
                            '·' in line):
                            address = line
                            break
                
                # Look for category
                for line in lines:
                    if line and line not in [name, english_name, rating, address, reviews] and len(line) < 30:
                        persian_categories = ['رستوران', 'کافه', 'فست فود', 'سوپرمارکت', 'هتل', 'مغازه']
                        english_categories = ['Restaurant', 'Cafe', 'Fast food', 'Supermarket', 'Hotel', 'Store']
                        if any(cat in line for cat in persian_categories + english_categories):
                            category = line
                            break
                
                # Extract image
                image_url = None
                try:
                    img = card.query_selector('img')
                    if img:
                        image_url = img.get_attribute('src')
                        if image_url and (image_url.startswith('//') or image_url.startswith('/')):
                            if image_url.startswith('//'):
                                image_url = 'https:' + image_url
                            else:
                                image_url = 'https://www.google.com' + image_url
                except:
                    pass
                
                # Get place URL for coordinates
                place_url = None
                try:
                    link = card.query_selector('a')
                    if link:
                        href = link.get_attribute('href')
                        if href and '/place/' in href:
                            place_url = 'https://www.google.com' + href if href.startswith('/') else href
                except:
                    pass
                
                # Extract coordinates from URL if available
                lat = None
                lng = None
                if place_url:
                    try:
                        # Extract coordinates from Google Maps URL pattern
                        coord_match = re.search(r'!3d([-\d.]+)!4d([-\d.]+)', place_url)
                        if coord_match:
                            lat = coord_match.group(1)
                            lng = coord_match.group(2)
                        else:
                            # Alternative pattern
                            coord_match = re.search(r'@([-\d.]+),([-\d.]+)', place_url)
                            if coord_match:
                                lat = coord_match.group(1)
                                lng = coord_match.group(2)
                    except:
                        pass
                
                # Filter for Tehran locations
                is_tehran = False
                if address:
                    tehran_indicators = ['تهران', 'Tehran', 'طهران']
                    is_tehran = any(indicator in address for indicator in tehran_indicators)
                
                # If no address but we have coordinates, check if coordinates are in Tehran area
                if not is_tehran and lat and lng:
                    try:
                        lat_num = float(lat)
                        lng_num = float(lng)
                        # Tehran is roughly between 35.5-35.8°N and 51.2-51.6°E
                        if 35.5 <= lat_num <= 35.8 and 51.2 <= lng_num <= 51.6:
                            is_tehran = True
                    except:
                        pass
                
                # If we still can't determine, assume it's in Tehran if the query contains Tehran
                if not is_tehran and 'تهران' in query:
                    is_tehran = True
                
                # Only add if it's in Tehran
                if is_tehran:
                    item = {
                        "name": name,
                        "english_name": english_name,
                        "address": address,
                        "rating": rating,
                        "reviews": reviews,
                        "category": category,
                        "image_url": image_url,
                        "latitude": lat,
                        "longitude": lng,
                        "url": place_url
                    }
                    
                    # Avoid duplicates
                    if not any(d['name'] == name for d in data):
                        data.append(item)
                        print(f"✅ {len(data)}. {name}")
                        if english_name:
                            print(f"   🇬🇧 English: {english_name}")
                        if rating:
                            print(f"   ⭐ Rating: {rating}" + (f" ({reviews} reviews)" if reviews else ""))
                        if address:
                            print(f"   📍 {address}")
                        if lat and lng:
                            print(f"   🗺️  Coordinates: {lat}, {lng}")
                    
            except Exception as e:
                print(f"❌ Error processing card {i}: {str(e)}")
                continue

        browser.close()
    
    print(f"✅ Successfully extracted {len(data)} places in Tehran for '{query}'")
    return data

if __name__ == "__main__":
    q = input("Enter search query for Google Maps (e.g. رستوران تهران): ").strip() or "رستوران تهران"
    results = scrape_google_maps_places(q)
    
    # Save to Excel automatically
    if results:
        import os
        from export_utils import save_to_excel, save_to_json
        
        os.makedirs("outputs", exist_ok=True)
        fname_base = q.replace(" ", "_")
        save_to_excel(results, f"outputs/{fname_base}_google_maps.xlsx")
        save_to_json(results, f"outputs/{fname_base}_google_maps.json")
        
        print(f"\n📊 Excel file saved: outputs/{fname_base}_google_maps.xlsx")
        print(f"📊 JSON file saved: outputs/{fname_base}_google_maps.json")