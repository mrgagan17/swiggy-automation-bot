import time
import speech_recognition as sr

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
import undetected_chromedriver as uc
# Monkey-patch undetected_chromedriver destructor to avoid WinError 6 on exit
try:
    original_del = uc.Chrome.__del__
    def safe_del(self):
        try:
            original_del(self)
        except Exception:
            pass
    uc.Chrome.__del__ = safe_del
except Exception:
    pass

# Your dedicated SwiggyBot profile
profile_path = r"YOUR_CHROME_PROFILE_PATH"

# Voice input
def get_food_items():
    r = sr.Recognizer()
    text = ""
    print("\n🎤 Initializing microphone for voice input...")
    try:
        with sr.Microphone() as source:
            print("🎙️ Adjusting for ambient noise, please wait...")
            r.adjust_for_ambient_noise(source, duration=1)
            print("🔊 Listening... Speak your food items now (e.g. 'pizza and burger')")
            audio = r.listen(source, timeout=10, phrase_time_limit=10)
            
        print("Processing voice...")
        text = r.recognize_google(audio)
        print(f"You said: {text}")
    except Exception as e:
        print(f"Voice recognition failed or microphone not accessible: {e}")
        print("Falling back to manual text entry...")
        text = input("Enter food (example: pizza and burger): ")

    items = [x.strip() for x in text.replace(",", " and ").split("and") if x.strip()]
    return items

# Browser setup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import undetected_chromedriver as uc

def launch_browser():
    options = uc.ChromeOptions()

    # use your real Chrome user data folder
    options.add_argument(
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36"
)
    options.add_argument("--profile-directory=AutomationProfile")
    options.add_argument("--start-maximized")

    driver = uc.Chrome(
        options=options,
        version_main=148
    )
    driver.maximize_window()
    driver.get("https://www.swiggy.com/")
    return driver   

# 🍴 Search & Add Item
def search_and_add_item(driver, item):
    wait = WebDriverWait(driver, 20)

    try:
        # open search page directly
        driver.get("https://www.swiggy.com/search")
        time.sleep(3)

        # locate search input
        search_box = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//input[@type="text"]')
            )
        )

        search_box.clear()
        search_box.send_keys(item)
        time.sleep(2)
        search_box.send_keys(Keys.ENTER)

        print(f"Searching for {item}")
        time.sleep(5)

        # click first restaurant/item result
        first_result = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '(//div[contains(@class,"_1HEuF")])[1]')
            )
        )
        first_result.click()

        time.sleep(5)

        # click add button
        add_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[contains(text(),"ADD")]')
            )
        )

        add_btn.click()
        print(f"🛒 Added {item}")

        time.sleep(3)

    except Exception as e:
        print(f"Error with {item}: {e}")
# Main
def main():
    items = get_food_items()
    if not items:
        print("No food items detected. Exiting...")
        return

    driver = launch_browser()
    time.sleep(5)  # allow account page to load

    for item in items:
        search_and_add_item(driver, item)

    print("\nAll items processed. You can now place your order manually.")
    input("Press ENTER to close browser...")
    driver.quit()

if __name__ == "__main__":
    main()
