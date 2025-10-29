# 🗺️ Tehran Google Maps Scraper

A powerful Python-based scraper that extracts **location data from Google Maps** specifically for **Tehran, Iran**.  
Perfect for developers, researchers, analysts, and data-driven projects requiring structured geographic information.

---

## 🌟 Features

- 🔍 **Smart Searching** – Automatically searches Google Maps scoped to Tehran
- 📍 **Persian Data** – Extracts Persian names, categories, and ratings
- 🗺️ **Geo Coordinates** – Latitude & longitude for each place
- 🖼️ **Images** – Captures place image URLs directly from Google Maps
- 📊 **Multiple Export Formats** – Save results to **Excel (.xlsx)** and **JSON**
- 🚀 **Simple CLI Interface** – Easy prompts & command-line usage
- 💾 **Error Handling** – Robust exception recovery & file locking

---

## 📋 Supported Place Types

- 🍽️ رستوران (Restaurants)
- 🌳 پارک (Parks)
- 🏨 هتل (Hotels)
- ☕ کافه (Cafes)
- 🛍️ فروشگاه (Stores)
- 🎬 سینما (Cinemas)
- 🏛️ موزه (Museums)
- 🏢 مرکز خرید (Shopping Malls)
- 🏫 دانشگاه (Universities)
- 🏥 بیمارستان (Hospitals)

You can also search custom Persian queries!

---

## 🚀 Quick Start

### ✅ Requirements

- Python **3.7+**
- `pip`

---

### 📦 Installation

Clone or download the project:

```bash
pip install -r requirements.txt

```
Install the Playwright browser engines:


```bash
Copy code
playwright install

```
Project files:


```bash
Copy code
main.py                # Interactive entrypoint
playwright_scraper.py  # Scraping logic
export_utils.py        # Export helpers
requirements.txt       # Dependencies
run.py                 # Quick search (optional)
outputs/               # Generated files

```
▶️ Basic Usage
Run the interactive script:


```bash
Copy code
python main.py
Enter a Persian search term when prompted (examples below).
Generated results will appear inside the outputs/ folder.

```
🔎 Quick Search Examples

```bash
Copy code
# Search for parks
python main.py
# Input: پارک

# Search for restaurants
python main.py
# Input: رستوران

# Search for hotels
python main.py
# Input: هتل
⚙️ Advanced Usage (Optional)
If run.py exists:

```

```bash
Copy code
python run.py "پارک"
python run.py "رستوران"
python run.py "کافه"

```
📊 Output Format
Excel columns include:

Column	Description	Example
name	Persian name of the place	پارک لاله
rating	Google rating (1–5)	4.3
reviews	Number of user reviews	1,234
category	Type of place	رستوران
image_url	URL of the place’s image	https://...
latitude	Latitude	35.6892
longitude	Longitude	51.3890
url	Google Maps link	https://maps.google.com/…


🧩 Project Structure

```bash
arduino
Copy code
tehran-maps-scraper/
│
├── main.py
├── playwright_scraper.py
├── export_utils.py
├── requirements.txt
├── run.py                (optional helper)
└── outputs/              # Excel/JSON results
    ├── پارک_tehran.xlsx
    ├── رستوران_tehran.xlsx
    └── ...

```
🔧 Technical Details
Dependencies
playwright – Browser automation

pandas – Data handling

openpyxl – Excel export

How It Works
Opens Google Maps centered on Tehran

Performs a Persian-language search

Scrolls to load all results

Extracts fields from place cards

Saves formatted outputs to Excel/JSON

🐛 Troubleshooting
“No places found”

Try more general keywords

Check connection

Disable problematic VPNs

“Permission Denied” when saving

Close any open Excel files

Browser won't open

Re-run:

bash
Copy code
playwright install
Persian text issues

Unicode fully supported in Excel & JSON

⚡ Performance Tips
Use specific queries

Results are cached in outputs/

Avoid extremely broad searches when possible

📝 Example Output
Searching for "پارک" generates rows such as:

name	rating	reviews	category	latitude	longitude
پارک لاله	4.5	8,742	پارک	35.7234	51.3880
پارک ملت	4.6	9,123	پارک	35.7654	51.4109
پارک ساعی	4.4	7,891	پارک	35.7345	51.3998

⚠️ Important Notes
For educational & research purposes

Please respect Google Maps’ Terms of Service

Do not overload Google’s servers

Accuracy depends on Google’s dataset

🤝 Contributing
Pull requests welcome!

New features

Bug fixes

Data improvements

Documentation updates

📄 License
This project is for educational purposes. Use responsibly.

🆘 Support
If you encounter problems:

Review troubleshooting above

Verify all dependencies are installed

Try simple searches (e.g., پارک)

Ensure Python is 3.7+

Happy Scraping! 🎉
