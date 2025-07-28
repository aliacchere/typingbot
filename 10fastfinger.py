import time
import pyautogui
import threading
import customtkinter as ctk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

# SETTINGS
WPM = 2050
CHARS_PER_WORD = 5
TYPING_DELAY = 60 / (WPM * CHARS_PER_WORD)  # ~0.048 seconds per character

running = False
driver = None

def init_browser():
    global driver
    options = Options()
    options.add_argument("--start-maximized")
    service = Service("chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://10fastfingers.com/login")
    print("🌐 Chrome opened. Please click 'Start Typing Test'.")

def wait_for_typing_box():
    for _ in range(30):
        try:
            word_element = driver.find_element(By.CSS_SELECTOR, "#row1 span.highlight")
            if word_element.is_displayed():
                return True
        except:
            pass
        time.sleep(1)
    return False

def type_fast_and_accurate(word):
    pyautogui.typewrite(word, interval=TYPING_DELAY)

def start_typing():
    global running
    running = True

    pyautogui.click()  # Focus input box

    if not wait_for_typing_box():
        print("❌ Typing box not found.")
        return

    while running:
        try:
            word_element = driver.find_element(By.CSS_SELECTOR, "#row1 span.highlight")
            word = word_element.text.strip()
            if word:
                type_fast_and_accurate(word)
                pyautogui.press("space")
        except NoSuchElementException:
            print("✅ Test complete.")
            break
        except Exception as e:
            print("❌ Error:", e)
            break

def stop_typing():
    global running, driver
    running = False
    try:
        driver.quit()
    except:
        pass

# GUI SETUP
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

def run_gui():
    app = ctk.CTk()
    app.title("Typing Bot 250+ WPM")
    app.geometry("450x220")

    label = ctk.CTkLabel(app, text="Click 'Start Bot' after starting test manually", font=("Arial", 15))
    label.pack(pady=20)

    start_btn = ctk.CTkButton(app, text="▶️ Start Bot", font=("Arial", 16), command=lambda: threading.Thread(target=start_typing).start())
    start_btn.pack(pady=10)

    stop_btn = ctk.CTkButton(app, text="⛔ Stop Bot", font=("Arial", 16), command=stop_typing)
    stop_btn.pack(pady=10)

    app.mainloop()

# Run everything
init_browser()
run_gui()
