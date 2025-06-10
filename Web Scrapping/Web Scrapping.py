# Required Libraries
from bs4 import BeautifulSoup        # HTML parsing
import lxml                          # Optional parser
import html5lib                      # Another parser
import pandas as pd                  # Data manipulation
import requests                      # For HTTP requests (if using URLs)
from selenium import webdriver       # Headless browser automation
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from parsel import Selector          # Another parsing alternative
import os                            # For file path handling

# Load HTML from local file
html_filename = "Premier_League.html"
with open(html_filename, "r", encoding="utf-8") as file:
    html_content = file.read()

# ===== BeautifulSoup Parsing =====
# Use different parsers
soup_bs4 = BeautifulSoup(html_content, "html.parser")   # Built-in parser
soup_lxml = BeautifulSoup(html_content, "lxml")         # Faster, needs lxml installed
soup_html5lib = BeautifulSoup(html_content, "html5lib") # More lenient, supports malformed HTML

# Select the table from any parser
table = soup_bs4.find("table")

# Extract headers
headers = [th.text.strip() for th in table.find("thead").find_all("th")]

# Extract rows
data_rows = []
for row in table.find("tbody").find_all("tr"):
    columns = row.find_all("td")
    row_data = [col.text.strip() for col in columns]
    data_rows.append(row_data)

# Convert to DataFrame
df = pd.DataFrame(data_rows, columns=headers)

# Save as CSV
df.to_csv("Premier_League.csv", index=False)
print("===== BeautifulSoup Data =====")
print(df)

# ===== Parsel Alternative =====
selector = Selector(text=html_content)
rows = selector.css("table tbody tr")
parsel_data = []

for row in rows:
    cols = [c.strip() for c in row.css("td::text").getall()]
    parsel_data.append(cols)

print("\n===== Parsel Extracted Data (Sample) =====")
print(parsel_data[:2])

# ===== Selenium Headless Parsing =====
chrome_options = Options()
chrome_options.add_argument("--headless")  # Headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=chrome_options)

# ✅ FIXED: Use absolute file path for local HTML
html_path = os.path.abspath(html_filename)
driver.get("file://" + html_path)

# Wait for JavaScript rendering if needed
time.sleep(2)

# Extract table rows using Selenium
table_rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
selenium_data = []

for row in table_rows:
    cells = row.find_elements(By.TAG_NAME, "td")
    row_data = [cell.text.strip() for cell in cells]
    selenium_data.append(row_data)

driver.quit()
print("\n===== Selenium Extracted Data (Sample) =====")
print(selenium_data[:2])
