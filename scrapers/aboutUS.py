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

output_folder ="scraped_data"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def scrape_aboutUS(url, filename):
    print(f"Starting scrape for {url}...")
    try:
        driver.get(url)
        
        page_data = {
            "url": url,
            "main_content": "",
            "accordion_data": []
        }

        # A. Extract the main descriptive paragraphs
        try:
            main_paragraphs = driver.find_elements(By.TAG_NAME, "p")
            # Join paragraphs into a single text block
            content_list = [p.text.strip() for p in main_paragraphs if len(p.text) > 20]
            page_data["main_content"] = "\n\n".join(content_list)
        except Exception as e:
            print(f"Error extracting paragraphs: {e}")

        # B. Extract Interactive Accordions
        try:
            headers = driver.find_elements(By.CLASS_NAME, "panel-heading")
            
            for i in range(len(headers)):
                current_headers = driver.find_elements(By.CLASS_NAME, "panel-heading")
                header = current_headers[i]
                title = header.text.strip()
                
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", header)
                time.sleep(1)
                try:
                    link = header.find_element(By.TAG_NAME, "a")
                    driver.execute_script("arguments[0].click();", link)
                    time.sleep(2) 
                except:
                    continue

                try:
                    panel_body = driver.find_element(By.CSS_SELECTOR, ".panel-collapse.collapse.in .panel-body")
                    
                    tables = panel_body.find_elements(By.TAG_NAME, "table")
                    if tables:
                        table_list = []
                        table = tables[0]
                        headers_list = [th.text.strip() for th in table.find_elements(By.TAG_NAME, "th")]
                        rows = table.find_elements(By.TAG_NAME, "tr")[1:] 
                        
                        for row in rows:
                            cells = row.find_elements(By.TAG_NAME, "td")
                            if cells:
                                row_dict = {headers_list[j]: cells[j].text.strip() for j in range(len(cells)) if j < len(headers_list)}
                                table_list.append(row_dict)
                        
                        page_data["accordion_data"].append({"title": title, "type": "table", "content": table_list})
                    else:
                        page_data["accordion_data"].append({"title": title, "type": "text", "content": panel_body.text.strip()})
                except Exception as inner_e:
                    print(f"Error processing section {title}: {inner_e}")

        except Exception as e:
            print(f"Error processing accordions: {e}")

        # 3. Save to TXT (Formatted)
        full_path = os.path.join(output_folder, filename)
        
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(f"URL: {page_data['url']}\n\n")
            
            f.write("=" * 60 + "\n")
            f.write("ABOUT US - INTRODUCTION\n")
            f.write("=" * 60 + "\n")
            f.write(page_data["main_content"] + "\n\n")

            for item in page_data["accordion_data"]:
                f.write("=" * 60 + "\n")
                f.write(f"SECTION: {item['title']}\n")
                f.write("=" * 60 + "\n")
                
                if item["type"] == "text":
                    f.write(item["content"] + "\n\n")
                
                elif item["type"] == "table" and item["content"]:
                    headers = list(item["content"][0].keys())
                    f.write(" | ".join(headers) + "\n")
                    f.write("-" * 60 + "\n")
                    for row in item["content"]:
                        f.write(" | ".join(row.values()) + "\n")
                    f.write("\n")
            
        print(f"Successfully saved {url} to {full_path}")

    except Exception as e:
        print(f"Critical error scraping {url}: {e}")

scrape_aboutUS("https://sunbeaminfo.in/about-us", "sunbeam_about_us.txt")
driver.quit()