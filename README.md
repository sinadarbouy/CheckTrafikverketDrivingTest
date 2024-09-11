### Driving Test Session Checker

This Python script allows users to check for available driving test sessions from the Swedish Transport Administration’s booking website using their social security number, a specified date, and license ID. The script requires manual login due to CAPTCHA or BankID verification.

### Captcha Handling (Experimental)

The script includes an experimental and just-for-fun feature for handling CAPTCHA, located in the images and captcha.py files. This part is not guaranteed to work and may require manual intervention. It is intended for educational purposes only and should not be relied upon for automated CAPTCHA solving.

### Features

- Automatic login: Automates the login process to the booking site, handling cookies and session management.
- Session availability checking: Continuously checks for available driving test sessions and compares them against a user-defined date.
- Alert system: Plays a beep sound when a session that meets the criteria is found.
- Automatic retry: Reattempts login if the session expires.

### Prerequisites

To run this script, you need:

- Python 3.x installed.
- Selenium WebDriver for Python.
- A WebDriver for your preferred browser (e.g., ChromeDriver for Google Chrome).
- Requests library for handling HTTP requests.
- A system capable of playing sound for the alert feature (os.system call to say on macOS, may require adjustment for other OS).

1.	Input Required Details:
- Social Security Number: Enter your social security number in the format YYYYMMDDXXXX.
- Date Threshold: Enter the date in YYYY-MM-DD format. The script will only consider exam dates earlier than this date.
- License ID: Enter the license ID (default is 5 if no input is provided).
2.	Login:
- The script will open a browser window and navigate to the login page of the Swedish Transport Administration’s booking site. You need to manually log in using your social security number, CAPTCHA, or BankID.
3.	Checking Sessions:
- The script will start checking for available sessions that match your criteria. If a session is found, it will play a beep sound to alert you.

### Script Details

The script consists of several functions:

- beep(): Plays a beep sound to alert the user of a found session.
- prompt_user_input(): Prompts the user for their social security number, date threshold, and license ID.
- login(social_security_number): Handles the login process using Selenium.
- is_session_valid(): Verifies if the current session is still valid.
- check_date(cookies, social_security_number, date_threshold, licence_id): Checks available exam dates against the user’s criteria.
- main(): Main function that orchestrates the checking process, managing login, and re-login as needed.


### Notes

- Manual login required: Due to the use of CAPTCHA or BankID, manual intervention is required for the login process.
- Session expiration handling: The script will reattempt login if the session expires.
