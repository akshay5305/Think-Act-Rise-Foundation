
# selenium_helpers.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import time


def create_driver(download_path=None, headless=False, window_size=(1200, 900)):
    """
    Create and return a Chrome webdriver with sensible defaults.
    If download_path is provided, PDFs will be downloaded to that dir.
    """
    options = Options()
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
    # Useful flags for linux/container environments
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"--window-size={window_size[0]},{window_size[1]}")
    
    # Additional options to prevent click interception
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")

    if download_path:
        prefs = {
            "download.default_directory": download_path,
            "download.prompt_for_download": False,
            # ensure PDFs are downloaded instead of opened in viewer
            "plugins.always_open_pdf_externally": True
        }
        options.add_experimental_option("prefs", prefs)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def open_case_status(driver, url="https://www.delhihighcourt.nic.in/web/", timeout=15):
    """
    Open the given url and click the 'Case Status' link in the banner.
    Waits for the case_type select to appear before returning.
    Raises RuntimeError on failure.
    """
    driver.get(url)
    wait = WebDriverWait(driver, timeout)

    # wait for the banner links to be present
    time.sleep(7)
    links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.banner-important-link-sec a")))

    clicked = False
    for link in links:
        text = (link.text or "").strip()
        if "Case Status" in text:
            # Try multiple click methods to avoid interception
            try:
                # Method 1: Regular click
                link.click()
            except:
                try:
                    # Method 2: JavaScript click
                    driver.execute_script("arguments[0].click();", link)
                except:
                    # Method 3: Action chains
                    ActionChains(driver).move_to_element(link).click().perform()
            clicked = True
            break

    if not clicked:
        raise RuntimeError("Could not find 'Case Status' link on the page.")

    # After clicking, wait for the form/select to load (case_type select)
    wait.until(EC.presence_of_element_located((By.ID, "case_type")))
    # small pause to let any JS settle (optional)
    time.sleep(0.5)
    return True


def fill_case_details(driver, case_type, case_number, year, timeout=15):
    """
    Fill in case details: case_type, case_number, year, captcha.
    Returns True if submitted successfully, False if captcha or form fails.
    """
    wait = WebDriverWait(driver, timeout)

    # --- CASE TYPE ---
    case_type_dropdown = wait.until(EC.presence_of_element_located((By.ID, "case_type")))
    select_case_type = Select(case_type_dropdown)
    try:
        select_case_type.select_by_visible_text(case_type)
    except Exception:
        raise ValueError(f"Case type '{case_type}' not found in dropdown.")

    # --- CASE NUMBER ---
    case_number_input = wait.until(EC.presence_of_element_located((By.ID, "case_number")))
    case_number_input.clear()
    case_number_input.send_keys(str(case_number))

    # --- YEAR ---
    year_dropdown = wait.until(EC.presence_of_element_located((By.ID, "case_year")))
    select_year = Select(year_dropdown)
    try:
        select_year.select_by_visible_text(str(year))
    except Exception:
        raise ValueError(f"Year '{year}' not found in dropdown.")

    # --- CAPTCHA ---
    captcha_text = wait.until(EC.presence_of_element_located((By.ID, "captcha-code"))).text.strip()
    captcha_input = wait.until(EC.presence_of_element_located((By.ID, "captchaInput")))
    captcha_input.clear()
    captcha_input.send_keys(captcha_text)

    # --- SUBMIT ---
    search_button = wait.until(EC.element_to_be_clickable((By.ID, "search")))
    
    # Try multiple click methods for submit button too
    try:
        search_button.click()
    except:
        try:
            driver.execute_script("arguments[0].click();", search_button)
        except:
            ActionChains(driver).move_to_element(search_button).click().perform()

    time.sleep(3)  # Wait for results
    return True


def check_data_and_click_orders(driver, wait_time=10):
    """
    Checks if search results have data. 
    If no data, returns {'status': 'no_data'}.
    If data exists, clicks 'Orders' and returns {'status': 'orders_page'}.
    """
    wait = WebDriverWait(driver, wait_time)

    try:
        # Wait for either "No data" row or the "Orders" link
        wait.until(lambda driver: 
                   driver.find_elements(By.CSS_SELECTOR, "td.dt-empty") or 
                   driver.find_elements(By.LINK_TEXT, "Orders"))

        if driver.find_elements(By.CSS_SELECTOR, "td.dt-empty"):
            print("❌ No data available for given details.")
            return {"status": "no_data"}

        else:
            orders_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Orders")))
            
            # Try multiple click methods for Orders link
            try:
                orders_link.click()
            except:
                try:
                    driver.execute_script("arguments[0].click();", orders_link)
                except:
                    ActionChains(driver).move_to_element(orders_link).click().perform()
                    
            print("✅ Clicked on Orders link.")
            time.sleep(3)
            return {"status": "orders_page"}

    except Exception as e:
        print("⚠️ Error while checking data:", e)
        return {"status": "error", "error": str(e)}


def get_orders_list(driver, wait_time=8):
    wait = WebDriverWait(driver, wait_time)
    orders_data = []

    try:
        wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "table tbody tr")
        ))

        rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
        if not rows:
            print("❌ No orders found.")
            return []

        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 3:  # At least 3 cells to get date
                order_date = cells[2].text.strip()  # Date is in the 3rd column

                link_element = cells[1].find_element(By.TAG_NAME, "a")
                order_name = link_element.text.strip()
                order_link = link_element.get_attribute("href")

                orders_data.append({
                    "date": order_date,
                    "name": order_name,
                    "link": order_link
                })

        print(f"✅ Found {len(orders_data)} orders with links.")
        return orders_data

    except Exception as e:
        print("⚠️ Error while scraping orders:", e)
        return []
