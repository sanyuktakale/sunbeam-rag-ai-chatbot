import json
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

try:
    url = "https://www.sunbeaminfo.in/modular-courses.php?mdid=57"
    driver.get(url)
    wait = WebDriverWait(driver, 20)

    full_course_data = {
        "course_name": "Mastering MCQs",
        "url": url,
        "general_info": {},
        "sections": [],
        "batch_schedule_table": []
    }

    info_container = driver.find_element(By.CLASS_NAME, "course_info")
    full_course_data["general_info"] = {
        "summary": info_container.text.strip().replace('\n', ' | ')
    }

    headers = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "panel-heading")))
    
    for i in range(len(headers)):
        current_headers = driver.find_elements(By.CLASS_NAME, "panel-heading")
        header = current_headers[i]
        header_text = header.text.strip()
        
        link = header.find_element(By.TAG_NAME, "a")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", link)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", link)
        time.sleep(2)
        
        if "Batch schedule" in header_text:
            try:
                table = driver.find_element(By.CSS_SELECTOR, ".panel-collapse.collapse.in table")
                th_elements = table.find_elements(By.TAG_NAME, "th")
                table_headers = [th.text.strip() for th in th_elements]
                rows = table.find_elements(By.TAG_NAME, "tr")[1:]
                for row in rows:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if cells:
                        row_dict = {table_headers[j]: cells[j].text.strip() for j in range(len(cells))}
                        full_course_data["batch_schedule_table"].append(row_dict)
            except Exception as e:
                print(f"Table error: {e}")
        else:
            try:
                body = driver.find_element(By.CSS_SELECTOR, ".panel-collapse.collapse.in .panel-body")
                full_course_data["sections"].append({
                    "title": header_text,
                    "content": body.get_attribute("textContent").strip()
                })
            except:
                continue

    # SAVE TO PDF
    pdf_saver.save_to_pdf(full_course_data, "Mastering_MCQ.pdf")

finally:
    driver.quit()