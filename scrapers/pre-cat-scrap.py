import time
import pdf_saver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def scrape_sunbeam_page(url):
    driver.get(url)
    wait = WebDriverWait(driver, 15)
    
    full_data = {
        "page_url": url,
        "general_info": {},
        "accordion_sections": []
    }

    try:
        full_data["general_info"]["course_title"] = driver.find_element(By.TAG_NAME, "h3").text
        
        headers = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "panel-heading")))
        for i in range(len(headers)):
            current_headers = driver.find_elements(By.CLASS_NAME, "panel-heading")
            header = current_headers[i]
            section_title = header.text.strip()
            
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", header)
            time.sleep(0.5)
            link = header.find_element(By.TAG_NAME, "a")
            driver.execute_script("arguments[0].click();", link)
            time.sleep(1.5)
            
            section_data = {"title": section_title}
            panel_body = driver.find_element(By.CSS_SELECTOR, ".panel-collapse.collapse.in .panel-body")
            
            tables = panel_body.find_elements(By.TAG_NAME, "table")
            if tables:
                table_data = []
                table = tables[0]
                th_elements = table.find_elements(By.TAG_NAME, "th")
                table_headers = [th.text.strip() for th in th_elements]
                rows = table.find_elements(By.TAG_NAME, "tr")[1:]
                for row in rows:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if cells:
                        row_dict = {table_headers[j]: cells[j].text.strip() for j in range(len(cells))}
                        table_data.append(row_dict)
                section_data["type"] = "table"
                section_data["content"] = table_data
            else:
                section_data["type"] = "text"
                section_data["content"] = panel_body.text.strip()
            
            full_data["accordion_sections"].append(section_data)

        # SAVE TO PDF
        pdf_saver.save_to_pdf(full_data, "Pre-CAT.pdf")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

scrape_sunbeam_page("https://sunbeaminfo.in/pre-cat")