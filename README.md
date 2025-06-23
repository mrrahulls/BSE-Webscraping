# 📊 BSE Shareholding Pattern Scraper
This project is a Python automation tool that scrapes the shareholding pattern data of publicly listed companies directly from the Bombay Stock Exchange (BSE). It uses Selenium WebDriver, BeautifulSoup, and Pandas to extract, parse, and export clean tabular data into an Excel file for analysis and research.

# 🚀 Features
✅ Automates browser-based extraction of BSE shareholding pattern

✅ Handles over 100 top-listed companies on BSE

✅ Parses complex nested HTML tables with BeautifulSoup

✅ Outputs data in a structured Excel format

✅ Includes dynamic wait handling for stable scraping

# 🛠️ Technologies Used
Selenium – for browser automation

BeautifulSoup – for HTML parsing

Pandas – for tabular data handling

webdriver-manager – for auto-managing ChromeDriver

# 📁 Output
Generates a single Excel file:

bash
Copy
Edit
All_Companies_Shareholding_Pattern.xlsx
Each row in the file represents a shareholding entry with respective company names as headers.

# 📌 How It Works
Launches a headless Chrome browser.

Searches the company on BSE site.

Navigates to the Shareholding Pattern section.

Extracts and parses the tabular data.

Appends it into a combined pandas DataFrame.

Saves everything into an Excel spreadsheet.

# ⚠️ Disclaimer
This scraper is intended for educational and research purposes only. Frequent or high-volume scraping may violate BSE's Terms of Use. Use responsibly.
