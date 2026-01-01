import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def scrape_pre_cat(URL, course_name, output_filename):
    print("Script started")

    # 1. Setup Chrome Browser
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    # 2. Output folder
    output_folder = "scraped_data"
    os.makedirs(output_folder, exist_ok=True)

    try:
        driver.get(URL)
        wait = WebDriverWait(driver, 20)
        print("Page loaded:", driver.title)

        course_data = {
            "course_name": course_name,
            "url": URL,
            "general_info": "",
            "sections": [],
            "batch_schedule_table": []
        }

        # 3. General Info
        try:
            info = driver.find_element(By.CLASS_NAME, "course_info")
            course_data["general_info"] = info.text.strip()
        except:
            course_data["general_info"] = "General information not found."

        # 4. Accordion Sections
        try:
            headers = wait.until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "panel-heading"))
            )

            for i in range(len(headers)):
                headers = driver.find_elements(By.CLASS_NAME, "panel-heading")
                header = headers[i]
                title = header.text.strip()

                link = header.find_element(By.TAG_NAME, "a")
                driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});", link
                )
                time.sleep(1)
                driver.execute_script("arguments[0].click();", link)
                time.sleep(2)

                # Batch Schedule Table
                if "Batch schedule" in title.lower():
                    try:
                        table = driver.find_element(
                            By.CSS_SELECTOR, ".panel-collapse.collapse.in table"
                        )

                        headers_row = [th.text.strip() for th in table.find_elements(By.TAG_NAME, "th")]
                        rows = table.find_elements(By.TAG_NAME, "tr")[1:]

                        for row in rows:
                            cells = row.find_elements(By.TAG_NAME, "td")
                            if cells:
                                row_data = {
                                    headers_row[j]: cells[j].text.strip()
                                    for j in range(len(cells))
                                }
                                course_data["batch_schedule_table"].append(row_data)

                        print("Batch schedule captured")

                    except Exception as e:
                        print("Batch table error:", e)

                else:
                    try:
                        body = driver.find_element(
                            By.CSS_SELECTOR, ".panel-collapse.collapse.in .panel-body"
                        )
                        course_data["sections"].append({
                            "title": title,
                            "content": body.text.strip()
                        })
                        print(f"Section captured: {title}")
                    except:
                        pass

        except Exception as e:
            print("Accordion parsing error:", e)

        # 5. Save as REAL TXT file
        full_path = os.path.join(output_folder, output_filename)

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

                headers = course_data["batch_schedule_table"][0].keys()
                f.write(" | ".join(headers) + "\n")
                f.write("-" * 60 + "\n")

                for row in course_data["batch_schedule_table"]:
                    f.write(" | ".join(row.values()) + "\n")

        print(f"\nTXT file saved successfully at:\n{full_path}")

    except Exception as e:
        print("Critical error:", e)

    finally:
        driver.quit()
        print("🧹 Browser closed")


# 6. Run Script
if __name__ == "__main__":
    scrape_pre_cat(
        URL="https://sunbeaminfo.in/pre-cat",
        course_name="Pre-CAT",
        output_filename="pre_cat.txt"
    )
