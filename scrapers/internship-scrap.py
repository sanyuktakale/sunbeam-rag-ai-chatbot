import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def scrape_full_internship_data(url, output_filename):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    output_folder = "scraped_data"
    os.makedirs(output_folder, exist_ok=True)

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 20)
        print("Page loaded.")

        full_data = {
            "program_name": "Internship Program",
            "url": url,
            "general_sections": [],
            "technology_matrix": [],
            "batch_schedule": []
        }

        # --- 1. CAPTURE ALL GENERAL ACCORDIONS & TECHNOLOGY MATRIX ---
        try:
            headers = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "panel-heading")))
            
            for i in range(len(headers)):
                current_headers = driver.find_elements(By.CLASS_NAME, "panel-heading")
                header = current_headers[i]
                title_text = header.text.strip()
                
                link = header.find_element(By.TAG_NAME, "a")
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", link)
                time.sleep(1)
                driver.execute_script("arguments[0].click();", link)
                time.sleep(2)

                try:
                    panel_body = driver.find_element(By.CSS_SELECTOR, ".panel-collapse.collapse.in .panel-body")
                    
                    tables = panel_body.find_elements(By.TAG_NAME, "table")
                    # Check if this is the Tech Matrix table
                    if tables and ("Available" in title_text or "Technology" in title_text):
                        table = tables[0]
                        rows = table.find_elements(By.TAG_NAME, "tr")
                        matrix_keys = [td.text.strip() for td in rows[0].find_elements(By.TAG_NAME, "td")]
                        
                        for row in rows[1:]:
                            cells = row.find_elements(By.TAG_NAME, "td")
                            if len(cells) == len(matrix_keys):
                                row_data = {matrix_keys[j]: cells[j].text.strip() for j in range(len(cells))}
                                full_data["technology_matrix"].append(row_data)
                        print(f"Captured Technology Matrix.")
                    else:
                        full_data["general_sections"].append({
                            "title": title_text,
                            "content": panel_body.text.strip()
                        })
                        print(f"Captured section: {title_text}")
                except Exception as inner:
                    print(f"Error inside section {title_text}: {inner}")

        except Exception as e:
            print(f"Error handling accordions: {e}")

        # --- 2. CAPTURE STANDALONE BATCH SCHEDULE (Bottom Table) ---
        try:
            schedule_wrapper = driver.find_element(By.CLASS_NAME, "table-responsive")
            table = schedule_wrapper.find_element(By.TAG_NAME, "table")
            
            headers = [th.text.strip() for th in table.find_elements(By.TAG_NAME, "th")]
            
            rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) >= len(headers):
                    row_data = {headers[j]: cells[j].text.strip() for j in range(len(headers))}
                    full_data["batch_schedule"].append(row_data)
            print("Captured Batch Schedule Table.")
        except Exception as e:
            print(f"Schedule table error: {e}")

        # 3. SAVE TO TXT (Formatted)
        full_path = os.path.join(output_folder, output_filename)
        
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(f"Program: {full_data['program_name']}\n")
            f.write(f"URL: {full_data['url']}\n\n")

            # General Sections
            for section in full_data["general_sections"]:
                f.write("=" * 60 + "\n")
                f.write(f"SECTION: {section['title']}\n")
                f.write("=" * 60 + "\n")
                f.write(section["content"] + "\n\n")

            # Technology Matrix Table
            if full_data["technology_matrix"]:
                f.write("=" * 60 + "\n")
                f.write("AVAILABLE TECHNOLOGY & DOMAINS\n")
                f.write("=" * 60 + "\n")
                
                headers = list(full_data["technology_matrix"][0].keys())
                f.write(" | ".join(headers) + "\n")
                f.write("-" * 60 + "\n")
                
                for row in full_data["technology_matrix"]:
                    f.write(" | ".join(row.values()) + "\n")
                f.write("\n")

            # Batch Schedule Table
            if full_data["batch_schedule"]:
                f.write("=" * 60 + "\n")
                f.write("BATCH SCHEDULE\n")
                f.write("=" * 60 + "\n")

                headers = list(full_data["batch_schedule"][0].keys())
                f.write(" | ".join(headers) + "\n")
                f.write("-" * 60 + "\n")

                for row in full_data["batch_schedule"]:
                    f.write(" | ".join(row.values()) + "\n")
            
        print(f"\nSUCCESS! All data combined into {full_path}")

    except Exception as e:
        print(f"Critical error: {e}")
    finally:
        driver.quit()
        print("Browser closed.")

if __name__ == "__main__":
    scrape_full_internship_data("https://sunbeaminfo.in/internship", "sunbeam_internship_full.txt")