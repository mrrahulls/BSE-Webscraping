from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

# Setup Selenium Chrome driver
options = Options()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 20)

# Company list
companies = [

    "Reliance Industries Ltd",
    "HDFC Bank Ltd",
    "Tata Consultancy Services Ltd",
    "Bharti Airtel Ltd",
    "ICICI Bank Ltd",
    "State Bank of India",
    "Infosys Ltd",
    "Life Insurance Corporation of India",
    "Bajaj Finance Ltd",
    "Hindustan Unilever Ltd",
    "ITC Ltd",
    "Larsen & Toubro Ltd",
    "HCL Technologies Ltd",
    "Kotak Mahindra Bank Ltd",
    "Maruti Suzuki India Ltd",
    "Sun Pharmaceutical Industries Ltd",
    "Mahindra & Mahindra Ltd",
    "AXIS Bank Ltd",
    "UltraTech Cement Ltd",
    "Hindustan Aeronautics Ltd",
    "NTPC Ltd",
    "Bajaj Finserv Ltd",
    "Oil and Natural Gas Corporation Ltd",
    "Titan Company Ltd",
    "Bharat Electronics Ltd",
    "Adani Ports and Special Economic Zone Ltd",
    "Adani Enterprises Ltd",
    "Avenue Supermarts Ltd",
    "Wipro Ltd",
    "Power Grid Corporation of India Ltd",
    "Tata Motors Ltd",
    "JSW Steel Ltd",
    "Eternal Ltd",
    "Coal India Ltd",
    "Bajaj Auto Ltd",
    "Nestle India Ltd",
    "Asian Paints Ltd",
    "DLF Ltd",
    "Trent Ltd",
    "InterGlobe Aviation Ltd",
    "Adani Power Ltd",
    "Indian Oil Corporation Ltd",
    "Tata Steel Ltd",
    "Jio Financial Services Ltd",
    "Hindustan Zinc Ltd",
    "Grasim Industries Ltd",
    "SBI Life Insurance Company Ltd",
    "Indian Railway Finance Corporation Ltd",
    "Divis Laboratories Ltd",
    "Vedanta Ltd",
    "HDFC Life Insurance Company Ltd",
    "Tech Mahindra Ltd",
    "Hyundai Motor India Ltd",
    "LTIMindtree Ltd",
    "Varun Beverages Ltd",
    "Solar Industries India Ltd",
    "Eicher Motors Ltd",
    "Bajaj Holdings & Investment Ltd",
    "Pidilite Industries Ltd",
    "Adani Green Energy Ltd",
    "Macrotech Developers Ltd",
    "Hindalco Industries Ltd",
    "Bharat Petroleum Corporation Ltd",
    "Power Finance Corporation Ltd",
    "Britannia Industries Ltd",
    "TVS Motor Company Ltd",
    "Mazagon Dock Shipbuilders Ltd",
    "Ambuja Cements Ltd",
    "Cholamandalam Investment and Finance Company Ltd",
    "ABB India Ltd",
    "Shriram Finance Ltd",
    "Tata Power Company Ltd",
    "Godrej Consumer Products Ltd",
    "Cipla Ltd",
    "Bank of Baroda",
    "Gail (India) Ltd",
    "Punjab National Bank",
    "Max Healthcare Institute Ltd",
    "Siemens Ltd",
    "Dr Reddys Laboratories Ltd",
    "Union Bank of India",
    "Tata Consumer Products Ltd",
    "Indian Hotels Company Ltd",
    "Torrent Pharmaceuticals Ltd",
    "Indus Towers Ltd",
    "United Spirits Ltd",
    "HDFC Asset Management Company Ltd",
    "Samvardhana Motherson International Ltd",
    "CG Power and Industrial Solutions Ltd",
    "Muthoot Finance Ltd",
    "Shree Cement Ltd",
    "REC Ltd",
    "Apollo Hospitals Enterprise Ltd",
    "Bajaj Housing Finance Ltd",
    "Adani Energy Solutions Ltd",
    "ICICI Lombard General Insurance Company Ltd",
    "IDBI Bank Ltd",
    "Info Edge (India) Ltd",
    "Swiggy Ltd",
    "Canara Bank"

]

combined_df = pd.DataFrame()

def extract_shareholding(company_name):
    driver.get("https://www.bseindia.com/")
    time.sleep(3)

    try:
        # Step 1: Search the company
        search_box = wait.until(EC.presence_of_element_located((By.ID, "getquotesearch")))
        driver.execute_script("arguments[0].scrollIntoView(true);", search_box)
        search_box.clear()
        search_box.send_keys(company_name)
        time.sleep(2)

        # Step 2: Click the first search suggestion
        suggestion = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ulSearchQuote"]/li[1]/a')))
        suggestion.click()

        # Step 3: Click on Shareholding Pattern section
        shareholding_div = wait.until(EC.element_to_be_clickable((By.ID, 'l9')))
        driver.execute_script("arguments[0].scrollIntoView(true);", shareholding_div)
        time.sleep(1)
        shareholding_div.click()

        # Step 4: Wait for the shareholding table to appear
        table = wait.until(EC.presence_of_element_located((
            By.XPATH, '//*[@id="deribody"]/div[2]/div[1]/div[1]/div/table/tbody/tr/td/table/tbody/tr[4]/td/table'
        )))
        table_html = table.get_attribute("outerHTML")

        # Step 5: Extract actual company name using your provided XPath
        actual_name_element = wait.until(EC.presence_of_element_located((
            By.XPATH, '//*[@id="getquoteheader"]/div[4]/div[5]/div[3]/div/div[1]/div[1]/div[1]/div[2]/div/h1'
        )))
        actual_company_name = actual_name_element.text.strip()

        # Step 6: Parse the table with BeautifulSoup
        soup = BeautifulSoup(table_html, 'html.parser')
        rows = soup.find_all('tr')

        # Separate header rows
        header_rows = [row for row in rows if row.find('td', class_='innertable_header1')]
        headers = []
        for row in header_rows:
            for cell in row.find_all(['td', 'th']):
                colspan = int(cell.get('colspan', 1))
                headers.extend([cell.get_text(strip=True)] * colspan)

        # Make headers unique
        unique_headers = []
        seen = {}
        for h in headers:
            if h not in seen:
                seen[h] = 1
                unique_headers.append(h)
            else:
                seen[h] += 1
                unique_headers.append(f"{h}_{seen[h]}")

        # Data rows
        data_rows = rows[len(header_rows):]
        data = []
        for row in data_rows:
            values = [cell.get_text(strip=True) for cell in row.find_all('td')]
            if values and values[0] != "Notes":
                while len(values) < len(unique_headers):
                    values.append('')
                data.append(values)

        df = pd.DataFrame(data, columns=unique_headers[:len(data[0])])
        df.insert(0, "Company", actual_company_name)
        return df

    except Exception as e:
        print(f"❌ Error extracting for {company_name}: {e}")
        return None

# Run for each company
for name in companies:
    print(f"🔍 Extracting: {name}")
    df = extract_shareholding(name)
    if df is not None:
        combined_df = pd.concat([combined_df, df], ignore_index=True)
    time.sleep(2)

# Save all data to Excel
combined_df.to_excel("All_Companies_Shareholding_Pattern.xlsx", index=False)
print("✅ Saved to All_Companies_Shareholding_Pattern.xlsx")

# Cleanup
driver.quit()
