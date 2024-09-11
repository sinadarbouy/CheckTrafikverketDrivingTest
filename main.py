import requests
import time
from datetime import datetime
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize the Chrome WebDriver
driver = webdriver.Chrome()

def beep():
    """Play a beep sound to indicate a found session."""
    os.system('say "found session"')

def prompt_user_input():
    """Prompt the user for required inputs and validate them."""
    social_security_number = input("Enter your social security number (e.g., 19970504XXXX): ")
    
    while True:
        try:
            date_input = input("Enter the date threshold in YYYY-MM-DD format (e.g., 2024-08-21): ")
            date_threshold = datetime.strptime(date_input, "%Y-%m-%d").date()
            break
        except ValueError:
            print("Invalid date format. Please try again.")
    
    while True:
        try:
            licence_id_input = input("Enter the licence ID (default is 5): ")
            licence_id = int(licence_id_input) if licence_id_input else 5
            break
        except ValueError:
            print("Invalid licence ID. Please enter a valid number.")

    return social_security_number, date_threshold, licence_id

def login(social_security_number):
    """Perform login using Selenium and return the cookies for use in requests."""
    driver.get("https://fp.trafikverket.se/boka/#/licence")
    print("Navigating to login page...")

    try:
        # Wait until the social security number input field is available, then enter the number
        try:
            personal_number_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'social-security-number-input'))
            )
            personal_number_field.send_keys(social_security_number)
            print("Social security number entered.")
        except Exception as e:
            print("Social security number input field not found or error occurred")

        # Wait until redirected to the correct URL (after login)
        while True:
            if driver.current_url.startswith("https://fp.trafikverket.se/boka/#/search/"):
                cookies = {cookie['name']: cookie['value'] for cookie in driver.get_cookies()}
                print("Login successful, cookies retrieved.")
                return cookies
            time.sleep(1)  # Wait a bit before re-checking the URL

    except Exception as e:
        print(f"Error during login: {e}")
        driver.quit()
        return None

def is_session_valid():
    """Check if the session is still valid by verifying the presence of specific text on the page."""
    try:
        driver.get("https://fp.trafikverket.se/boka/#/licence")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Välj behörighet')]"))
        )
        print("Session is valid.")
        return True
    except Exception as e:
        print(f"Session validation failed or text not found: {e}")
        return False

def check_date(cookies, social_security_number, date_threshold, licence_id):
    """Check the available exam dates against the user-defined threshold."""
    url = "https://fp.trafikverket.se/boka/occasion-bundles"
    headers = {
        "Host": "fp.trafikverket.se",
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Referer": "https://fp.trafikverket.se/boka/",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Connection": "close"
    }
    data = {
        "bookingSession": {
            "socialSecurityNumber": social_security_number,
            "licenceId": licence_id,
            "bookingModeId": 0,
            "ignoreDebt": False,
            "ignoreBookingHindrance": False,
            "examinationTypeId": 0,
            "excludeExaminationCategories": [],
            "rescheduleTypeId": 0,
            "paymentIsActive": False,
            "searchedMonths": 0
        },
        "occasionBundleQuery": {
            "startDate": "1970-01-01T00:00:00.000Z",
            "searchedMonths": 0,
            "locationId": 1000337,
            "nearbyLocationIds": [1000326, 1000134, 1000132],
            "languageId": 0,
            "vehicleTypeId": 2,
            "tachographTypeId": 1,
            "occasionChoiceId": 1,
            "examinationTypeId": 12
        }
    }

    response = requests.post(url, headers=headers, cookies=cookies, json=data)

    if response.status_code != 200:
        print(f"Error: {response.status_code}. Failed to fetch exam dates.")
        return False

    try:
        response_data = response.json()
        for bundle in response_data.get('data', {}).get('bundles', []):
            for occasion in bundle.get('occasions', []):
                exam_date = occasion['date']
                location_name = occasion['locationName']
                if datetime.strptime(exam_date, "%Y-%m-%d").date() < date_threshold:
                    print(f"Exam date: {exam_date}, Location Name: {location_name}")
                    beep()
                    return True  # Stop checking once a valid session is found
    except (KeyError, ValueError) as e:
        print(f"Failed to process response: {e}")
    
    return False

def main():
    social_security_number, date_threshold, licence_id = prompt_user_input()
    cookies = None

    while True:
        if not cookies or not is_session_valid():
            cookies = login(social_security_number)

        if cookies and not check_date(cookies, social_security_number, date_threshold, licence_id):
            print("Session expired or authentication failed. Retrying login...")
            cookies = None  # Trigger re-login

        time.sleep(120)  # Wait for 2 minutes before the next check

if __name__ == "__main__":
    main()
