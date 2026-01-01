import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# 1. Setup Browser
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

output_folder = "scraped_data"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def scrape_contactUS(url, output_filename):
    print(f"Accessing {url}...")
    try:
        driver.get(url)
        
        # Final data object
        page_data = {
            "url": url,
            "content": []
        }

        # Step A: Handle Interactive Accordions
        headers = driver.find_elements(By.CLASS_NAME, "panel-heading")
        
        if headers:
            print(f"Detected Accordion Page: {url}")
            for i in range(len(headers)):
                try:
                    current_headers = driver.find_elements(By.CLASS_NAME, "panel-heading")
                    header = current_headers[i]
                    title = header.text.strip()
                    
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", header)
                    time.sleep(1)
                    try:
                        link = header.find_element(By.TAG_NAME, "a")
                        driver.execute_script("arguments[0].click();", link)
                        time.sleep(2)
                    except: continue

                    panel_body = driver.find_element(By.CSS_SELECTOR, ".panel-collapse.collapse.in .panel-body")
                    
                    tables = panel_body.find_elements(By.TAG_NAME, "table")
                    if tables:
                        table_rows = []
                        table = tables[0]
                        th_cols = [th.text.strip() for th in table.find_elements(By.TAG_NAME, "th")]
                        tr_elements = table.find_elements(By.TAG_NAME, "tr")[1:]
                        for tr in tr_elements:
                            tds = tr.find_elements(By.TAG_NAME, "td")
                            if tds:
                                row_dict = {th_cols[j]: tds[j].text.strip() for j in range(len(tds)) if j < len(th_cols)}
                                table_rows.append(row_dict)
                        page_data["content"].append({"title": title, "type": "table", "data": table_rows})
                    else:
                        page_data["content"].append({"title": title, "type": "text", "data": panel_body.text.strip()})
                except Exception as inner_e:
                    print(f"Error in accordion section {i}: {inner_e}")

        # Step B: Handle Static Content
        else:
            print(f"Detected Static/Contact Page: {url}")
            try:
                containers = driver.find_elements(By.CLASS_NAME, "text_box") or \
                             driver.find_elements(By.CLASS_NAME, "inner_page_wrap")
                for container in containers:
                    text = container.text.strip()
                    if text:
                        page_data["content"].append({"title": "General Info", "type": "text", "data": text})
            except Exception as e:
                print(f"Error extracting static content: {e}")

        # Save to TXT (Formatted)
        full_path = os.path.join(output_folder, output_filename)
        
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(f"Page URL: {page_data['url']}\n\n")

            for item in page_data["content"]:
                f.write("=" * 60 + "\n")
                f.write(f"SECTION: {item.get('title', 'Info')}\n")
                f.write("=" * 60 + "\n")
                
                if item["type"] == "text":
                    f.write(item["data"] + "\n\n")
                
                elif item["type"] == "table" and item["data"]:
                    headers = list(item["data"][0].keys())
                    f.write(" | ".join(headers) + "\n")
                    f.write("-" * 60 + "\n")
                    for row in item["data"]:
                        f.write(" | ".join(row.values()) + "\n")
                    f.write("\n")

        print(f"Success! Saved to {full_path}")

    except Exception as e:
        print(f"Critical Error on {url}: {e}")

scrape_contactUS("https://sunbeaminfo.in/contact-us", "contact_final.txt")
driver.quit()