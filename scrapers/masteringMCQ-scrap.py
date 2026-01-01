import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# 1. Setup Browser
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Create output folder
output_folder = "scraped_data"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

try:
    url = "https://www.sunbeaminfo.in/modular-courses.php?mdid=57"
    driver.get(url)
    wait = WebDriverWait(driver, 20)
    print("Page loaded.")

    course_data = {
        "course_name": "Mastering MCQs",
        "url": url,
        "general_info": "",
        "sections": [],
        "batch_schedule_table": []
    }

    # 2. Extract General Info
    try:
        info_container = driver.find_element(By.CLASS_NAME, "course_info")
        course_data["general_info"] = info_container.text.strip().replace('\n', ' ')
    except:
        course_data["general_info"] = "Info container not found"

    # 3. Handle Interactive Dropdowns (Accordions)
    try:
        headers = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "panel-heading")))
        
        for i in range(len(headers)):
            current_headers = driver.find_elements(By.CLASS_NAME, "panel-heading")
            header = current_headers[i]
            header_text = header.text.strip()
            
            # Click to expand
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
                    
                    rows = table.find_elements(By.TAG_NAME, "tr")[1:] # Skip header row
                    for row in rows:
                        cells = row.find_elements(By.TAG_NAME, "td")
                        if cells:
                            row_dict = {table_headers[j]: cells[j].text.strip() for j in range(len(cells)) if j < len(table_headers)}
                            course_data["batch_schedule_table"].append(row_dict)
                    print("Captured structured table data.")
                except Exception as e:
                    print(f"Table error: {e}")
            else:
                try:
                    body = driver.find_element(By.CSS_SELECTOR, ".panel-collapse.collapse.in .panel-body")
                    course_data["sections"].append({
                        "title": header_text,
                        "content": body.text.strip()
                    })
                    print(f"Captured text section: {header_text}")
                except:
                    continue
    except Exception as e:
        print(f"Error processing sections: {e}")

    # 4. Save the Final TXT (Formatted)
    full_path = os.path.join(output_folder, "Mastering_MCQ.txt")
    
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(f"Course Name: {course_data['course_name']}\n")
        f.write(f"URL: {course_data['url']}\n\n")

        f.write("=" * 60 + "\n")
        f.write("GENERAL INFORMATION\n")
        f.write("=" * 60 + "\n")
        f.write(course_data["general_info"] + "\n\n")

        for section in course_data["sections"]:
            f.write("=" * 60 + "\n")
            f.write(f"SECTION: {section['title']}\n")
            f.write("=" * 60 + "\n")
            f.write(section["content"] + "\n\n")

        if course_data["batch_schedule_table"]:
            f.write("=" * 60 + "\n")
            f.write("BATCH SCHEDULE\n")
            f.write("=" * 60 + "\n")

            headers = list(course_data["batch_schedule_table"][0].keys())
            f.write(" | ".join(headers) + "\n")
            f.write("-" * 60 + "\n")

            for row in course_data["batch_schedule_table"]:
                f.write(" | ".join(row.values()) + "\n")
        
    print(f"\nSuccess! Complete data saved to {full_path}")

except Exception as e:
    print(f"Critical error: {e}")
finally:
    driver.quit()
    print("Browser closed.")