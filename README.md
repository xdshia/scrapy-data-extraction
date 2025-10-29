Tehran Google Maps Scraper
A powerful Python scraper that extracts place data from Google Maps specifically for Tehran, Iran. Perfect for researchers, data analysts, and developers who need location data from Tehran.

🌟 Features
🔍 Smart Searching: Automatically searches in Tehran for any type of place

📍 Persian Data: Extracts Persian names, ratings, and categories

🗺️ Coordinates: Gets latitude and longitude for each place

🖼️ Images: Extracts place images from Google Maps

📊 Multiple Formats: Exports to Excel (.xlsx) and JSON formats

🚀 Easy to Use: Simple command-line interface

💾 Error Handling: Robust error recovery and file locking handling

📋 Supported Place Types
🍽️ رستوران - Restaurants

🌳 پارک - Parks

🏨 هتل - Hotels

☕ کافه - Cafes

🛍️ فروشگاه - Stores

🎬 سینما - Cinemas

🏛️ موزه - Museums

🏢 مرکز خرید - Shopping malls

🏫 دانشگاه - Universities

🏥 بیمارستان - Hospitals

🚀 Quick Start
Prerequisites
Python 3.7 or higher

pip (Python package manager)

Installation
Clone or download the project files:

main.py - Main interactive script

playwright_scraper.py - Scraping logic

export_utils.py - Export utilities

requirements.txt - Dependencies

Install dependencies:

bash
pip install -r requirements.txt
Install Playwright browser:

bash
playwright install
Basic Usage
Run the interactive scraper:

bash
python main.py
Enter your search query when prompted (examples below)

Wait for results - the script will open a browser and extract data

Check the outputs/ folder for your Excel and JSON files

Quick Search Examples
bash
# Search for parks
python main.py
# Then enter: پارک

# Search for restaurants  
python main.py
# Then enter: رستوران

# Search for hotels
python main.py
# Then enter: هتل
Advanced Usage
Using the quick search script (if you have run.py):

bash
python run.py "پارک"
python run.py "رستوران"
python run.py "کافه"
📊 Output Data
The scraper generates Excel files with the following columns:

Column	Description	Example
name	Persian name of the place	پارک لاله
rating	Google rating (1-5)	4.3
reviews	Number of reviews	1,234
category	Type of place	رستوران
image_url	URL of place image	https://...
latitude	Latitude coordinates	35.6892
longitude	Longitude coordinates	51.3890
url	Google Maps URL	https://maps.google.com/...
🛠️ Project Structure
text
tehran-maps-scraper/
│
├── main.py                 # Interactive main script
├── playwright_scraper.py   # Core scraping logic
├── export_utils.py         # Excel/JSON export functions
├── requirements.txt        # Python dependencies
├── run.py                 # Quick search script (optional)
└── outputs/               # Generated Excel/JSON files
    ├── پارک_tehran.xlsx
    ├── رستوران_tehran.xlsx
    └── ...
🔧 Technical Details
Dependencies
playwright: Browser automation

pandas: Data manipulation and Excel export

openpyxl: Excel file handling

How It Works
Opens Google Maps with Tehran coordinates

Performs search with Persian queries

Scrolls through results to load all places

Extracts data from each place card

Exports to organized Excel/JSON files

🐛 Troubleshooting
Common Issues
"No places found"

Try different search terms

Check your internet connection

Ensure you're not using a VPN that blocks Google

"Permission denied" error

Close any open Excel files

The script will automatically create a backup file

Browser doesn't open

Run playwright install again

Ensure you have Chrome/Firefox installed

Persian text issues

The script handles Persian encoding automatically

Excel files support Persian text correctly

Performance Tips
Use specific queries for faster results

The script automatically scrolls to load all results

Results are cached in the outputs/ folder

📝 Example Output
After searching for "پارک", you'll get an Excel file like:

name	rating	reviews	category	latitude	longitude
پارک لاله	4.5	8,742	پارک	35.7234	51.3880
پارک ملت	4.6	9,123	پارک	35.7654	51.4109
پارک ساعی	4.4	7,891	پارک	35.7345	51.3998
⚠️ Important Notes
Educational Use: This tool is for educational and research purposes

Rate Limiting: Please use responsibly to avoid overwhelming Google's servers

Terms of Service: Respect Google Maps' Terms of Service

Data Accuracy: Data comes from Google Maps and may have limitations

🤝 Contributing
Feel free to fork this project and submit pull requests for:

Additional features

Bug fixes

Performance improvements

Documentation updates

📄 License
This project is for educational purposes. Please use responsibly and respect website terms of service.

🆘 Support
If you encounter issues:

Check the troubleshooting section above

Ensure all dependencies are installed

Try running with a simple query like "پارک"

Check that your Python version is 3.7+

Happy Scraping! 🎉
