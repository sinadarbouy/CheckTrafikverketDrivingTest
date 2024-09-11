from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import string
import requests

def generate_random_filename(extension="jpeg", length=10):
    """Generate a random file name for downloaded images."""
    random_name = ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
    return f"{random_name}.{extension}"

def download_image(image_url, save_path):
    """Download the image from the given URL and save it to the specified path."""
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Image saved as {save_path}")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")

def solve_captcha(driver, wait):
    """Attempt to solve the hCaptcha by interacting with the elements."""
    try:
        # Switch to hCaptcha iframe and click the checkbox
        captcha_iframe = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/section[2]/form/div/div[2]/div/div[2]/div/div/div/iframe")))
        driver.switch_to.frame(captcha_iframe)
        checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[1]/div[1]/div/div/div[1]")))
        checkbox.click()
        time.sleep(2)

        # Switch back to default content and handle the challenge
        driver.switch_to.default_content()
        challenge_iframe = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/div[1]/iframe")))
        driver.switch_to.frame(challenge_iframe)
        
        # Find and download images if necessary
        h2_element = driver.find_element(By.CSS_SELECTOR, 'h2.prompt-text')
        if "motor" in h2_element.text:
            elements = driver.find_elements(By.CLASS_NAME, "image")
            for image_div in elements:
                style_attribute = image_div.get_attribute("style")
                start_token = 'background: url("'
                end_token = '") 50% 50%'
                start_index = style_attribute.find(start_token) + len(start_token)
                end_index = style_attribute.find(end_token)
                image_url = style_attribute[start_index:end_index]
                random_filename = generate_random_filename()
                download_image(image_url, random_filename)
                
        # Click challenge to attempt solution
        challenge = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[4]/div[2]/svg:svg')
        for _ in range(10):  # Repeat if needed
            challenge.click()
            time.sleep(2)
        
        driver.switch_to.default_content()  # Switch back to main frame
    except Exception as e:
        print(f"Error while solving captcha: {e}")

def main():
    """Main function to execute the automated browser interactions."""
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("https://fp.trafikverket.se/boka/#/licence")

        # Call the function to solve the captcha
        solve_captcha(driver, wait)

        # After captcha is solved, continue with further steps
        section = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/section[2]")))
        section.click()

        # Additional automation steps as needed...

    finally:
        time.sleep(10)
        driver.quit()

if __name__ == "__main__":
    main()
