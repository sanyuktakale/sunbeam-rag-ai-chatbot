import time
import pdf_saver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def scrape_contactUS(url, output_file):
    driver.get(url)
    wait = WebDriverWait(driver, 20)
    
    page_data = {
        "url": url,
        "scrape_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "content": []
    }

    try:
        headers = driver.find_elements(By.CLASS_NAME, "panel-heading")
        if headers:
            print(f"Detected Accordion Page: {url}")
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
                            row_dict = {th_cols[j]: tds[j].text.strip() for j in range(min(len(tds), len(th_cols)))}
                            table_rows.append(row_dict)
                    page_data["content"].append({"title": title, "type": "table", "data": table_rows})
                else:
                    page_data["content"].append({"title": title, "type": "text", "data": panel_body.text.strip()})
        else:
            print(f"Detected Static/Contact Page: {url}")
            containers = driver.find_elements(By.CLASS_NAME, "text_box") or \
                         driver.find_elements(By.CLASS_NAME, "inner_page_wrap")
            for container in containers:
                text = container.text.strip()
                if text:
                    page_data["content"].append({"type": "info_block", "data": text.split('\n')})

        # SAVE TO PDF
        pdf_saver.save_to_pdf(page_data, output_file)

    except Exception as e:
        print(f"Error on {url}: {e}")

scrape_contactUS("https://sunbeaminfo.in/contact-us", "contact_final.pdf")
driver.quit()