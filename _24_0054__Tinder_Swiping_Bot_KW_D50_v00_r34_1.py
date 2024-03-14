from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException  # Updated to include TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import time

# Constants
EMAIL = "YOUR_EMAIL"

# Function to log messages
def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n{timestamp} - {message}")


def click_big_main_login_button(driver):
    try:
        # this css selector might be specific and may need adjustment based on the actual page structure
        big_main_login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#s1524772468 > div > div.App__body.H\\(100\\%\\).Pos\\(r\\).Z\\(0\\) > div > div > main > div > div.Expand > div > div.Expand.Pos\\(r\\) > div > div > button.c1p6lbu0.W\\(80\\%\\).My\\(20px\\).Mx\\(a\\) > div.w1u9t036 > div.l17p5q9z"))
        )
        big_main_login_button.click()
        log_message("big main login button clicked successfully.")
    except TimeoutException as e:
        log_message("big main login button not found or not clickable.")


# Function to click on the English option
def click_english_option(driver):
    try:
        english_option = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'English')]"))
        )
        english_option.click()
        log_message("Selected English from the selection.")
    except TimeoutException as e:
        log_message(f"Error selecting English option: {e}")

# Function to find and click the decline button
def find_decline_button(driver):
    try:
        decline_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'l17p5q9z') and contains(text(), 'I decline')]"))
        )
        decline_button.click()
        log_message("Decline button clicked.")

        click_big_main_login_button(driver)

        return True
    except TimeoutException as e:
        log_message("Decline button not found within 3 seconds.")
        return False

# Function to click the login button
def click_login_button(driver):
    try:
        login_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Log in')]"))
        )
        login_button.click()
        log_message("Login button clicked.")
    except TimeoutException as e:
        log_message(f"Error clicking login button: {e}")

# Function to click the login button as a backup
def click_login_button_2(driver):
    try:
        login_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Log in')]/ancestor::a"))
        )
        login_button.click()
        log_message("Backup login button clicked.")
    except TimeoutException as e:
        log_message(f"Error clicking backup login button: {e}")



# Attempt to find and click the Google login button using WebDriverWait for consistency
def continue_with_google_login_spanish_then_english(attempts=2):
    while attempts > 0:
        try:
            continue_with_google_spanish = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'nsm7Bb-HzV7m-LgbsSe-BPrWId') and contains(text(), 'Continuar con Google')]"))
            )
            continue_with_google_spanish.click()
            log_message("Clicked on 'Continuar con Google' button successfully.")
            break  # Exit loop on success
        except TimeoutException:
            log_message("'Continuar con Google' button not found, attempting in English.")
            try:
                continue_with_google = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "span.nsm7Bb-HzV7m-LgbsSe-BPrWId"))
                )
                continue_with_google.click()
                log_message("Clicked on 'Continue with Google' button successfully.")
                break  # Exit loop on success
            except TimeoutException as e:
                log_message(f"Error clicking 'Continue with Google' button: {e}")
                attempts -= 1
                if attempts <= 0:
                    log_message("Failed to click on Google login button after multiple attempts, trying Login button.")
                    # If both Spanish and English attempts fail, click on the Login button and retry
                    click_login_button(driver)
                    # Here you should also consider what to do if click_login_button fails, e.g., try click_login_button_2
                    # Since the primary login button click is already in the main script, you may want to ensure it doesn't repeat unnecessarily
                else:
                    log_message("Retrying Google login after clicking on Login button.")
                    # Optionally wait a bit before retrying
                    time.sleep(2)  # Adjust sleep time as needed



# Initialize Chrome WebDriver options
chrome_options = Options()

# Initialize the Chrome WebDriver service
service = Service(ChromeDriverManager().install())

# Initialize the Chrome WebDriver with the service and options
driver = webdriver.Chrome(service=service, options=chrome_options)
log_message("WebDriver initialized.")

# Navigate to Tinder's login page
driver.get("https://tinder.com/")
log_message("Navigated to Tinder's login page.")

# Attempt to click on the decline button and then the continue_with_google_login
if find_decline_button(driver):
    continue_with_google_login_spanish_then_english()

# typing your email into the email field box:
# more enhancements:
try:
    WebDriverWait(driver, 10).until(lambda d: d.execute_script('return document.readyState') == 'complete')
    log_message("Confirmed page is fully loaded.")
except TimeoutException:
    log_message("Page did not load within expected time.")


# update the webdriver wait to ensure the page is fully loaded and ready for interaction
WebDriverWait(driver, 20).until(lambda d: d.execute_script('return document.readyState') == 'complete')
log_message("Confirmed page is fully loaded and ready for email interaction.")

# insert direct email input interaction here
# this assumes the google login field is immediately accessible; if it's within an iframe or a new window, additional context switching is needed
try:
    # adjust the selector as needed to accurately target the google email input field
    email_input_field = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='email']")))
    email_input_field.clear()  # clear any pre-filled text
    email_input_field.send_keys(EMAIL + Keys.ENTER)
    log_message("Directly typed in the email and sent the Enter key.")
except TimeoutException:
    log_message("Failed to directly type in the email within the timeout period.")




# Check if the element is inside an iframe and switch to it

try:
    body_element = driver.find_element(By.TAG_NAME, 'body')
    body_element.send_keys(Keys.TAB + EMAIL + Keys.ENTER)  # Move focus to the next focusable element
    log_message("Tab key sent and email typed in.")
    # If you know the exact number of tabs to reach the email input, repeat as needed
    # for _ in range(number_of_tabs - 1):
    #     body_element.send_keys(Keys.TAB)
except Exception as e:
    log_message(f"Error sending Tab key: {e}")

# After focusing the correct field, send the email
# Assuming the email field is now focused after tabbing
# try:
#     focused_element = driver.switch_to.active_element
#     focused_element.send_keys(EMAIL + Keys.ENTER)
#     log_message("Email entered and Enter key sent.")
# except Exception as e:
#     log_message(f"Error entering email: {e}")



# Try the primary login method:
# click_login_button(driver)

# Try the backup login method if the primary fails or as an additional step:
# click_login_button_2(driver)

# Click on the English option:
# click_english_option(driver)




# Wait for user input to exit
input("Press Enter to exit...\n")

# Close the browser
# driver.quit()
