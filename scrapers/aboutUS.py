import time
import pdf_saver  # Import the helper
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def scrape_aboutUS(url, filename):
    driver.get(url)
    wait = WebDriverWait(driver, 20)
    
    page_data = {
        "url": url,
        "main_content": [],
        "accordion_data": []
    }

    try:
        main_paragraphs = driver.find_elements(By.TAG_NAME, "p")
        page_data["main_content"] = [p.text.strip() for p in main_paragraphs if len(p.text) > 20]

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
                        # Handle case where headers count doesn't match cells
                        row_dict = {}
                        for j in range(len(cells)):
                            key = headers_list[j] if j < len(headers_list) else f"Column_{j}"
                            row_dict[key] = cells[j].text.strip()
                        table_list.append(row_dict)
                page_data["accordion_data"].append({"title": title, "type": "table", "content": table_list})
            else:
                page_data["accordion_data"].append({"title": title, "type": "text", "content": panel_body.text.strip()})

        # SAVE TO PDF INSTEAD OF JSON
        pdf_saver.save_to_pdf(page_data, filename)

    except Exception as e:
        print(f"Error scraping {url}: {e}")

scrape_aboutUS("https://sunbeaminfo.in/about-us", "sunbeam_about_us.pdf")
driver.quit()