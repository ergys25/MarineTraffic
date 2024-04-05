import json
import logging
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure logging
logging.basicConfig(filename='script.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def initialize_driver(geckodriver_path):
    """Initialize and return a Firefox webdriver."""
    service = Service(geckodriver_path)
    driver = webdriver.Firefox(service=service)
    return driver


def main():
    try:
        # Set path to geckodriver
        geckodriver_path = 'geckodriver'

        # Initialize Firefox webdriver
        driver = initialize_driver(geckodriver_path)
        logging.info("WebDriver initialized successfully.")

        # Navigate to the login page
        driver.get('https://www.marinetraffic.com/en/users/login')
        logging.info("Navigated to login page.")

        # Wait for the login button to be clickable
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/button[2]"))
        )
        login_button.click()
        logging.info("Login button clicked successfully.")

        # Enter email address
        email_input = WebDriverWait(driver, 1).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "/html/body/div[2]/main/section/div[2]/div/div/div[2]/div/form/div/div/div[1]/div/div/input"))
        )
        email_input.send_keys("<--YOUR_EMAIL_ADDRESS-->")  # Your email
        logging.info("Email address entered successfully.")

        # Enter password
        password_input = WebDriverWait(driver, 1).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "/html/body/div[2]/main/section/div[2]/div/div/div[2]/div/form/div/div/div[2]/div/div/input"))
        )
        password_input.send_keys("<--YOUR_PASSWORD-->")  # Your password
        logging.info("Password entered successfully.")

        # Click the login button
        login_submit_button = WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[2]/main/section/div[2]/div/div/div[2]/div/form/div/div/div[5]/button"))
        )
        login_submit_button.click()
        logging.info("Login button clicked successfully.")

        # Wait for the main page to load completely
        main_page_title = "MarineTraffic"
        WebDriverWait(driver, 10).until(EC.title_contains(main_page_title))
        logging.info("Main page loaded successfully.")

        # List of URLs
        urls = [
            'https://www.marinetraffic.com/en/ais/details/ships/shipid:688894/mmsi:538010145/imo:9591806/vessel:EFFIE',
            'https://www.marinetraffic.com/en/ais/details/ships/shipid:374953/mmsi:636018294/imo:9249180/vessel:NEW_FRIENDSHIP',
            'https://www.marinetraffic.com/en/ais/details/ships/shipid:5961417/mmsi:240126100/imo:0/vessel:LITTLE_M',
            'https://www.marinetraffic.com/en/ais/details/ships/shipid:3549980/mmsi:636018564/imo:9679892/vessel:CMA_CGM_CONGO',
            'https://www.marinetraffic.com/en/ais/details/ships/shipid:6334768/mmsi:440486000/imo:9868364/vessel:HMM_ST_PETERSBURG',
            'https://www.marinetraffic.com/en/ais/details/ships/shipid:7848861/mmsi:636022757/imo:9941788/vessel:EMDEN',
            'https://www.marinetraffic.com/en/ais/details/ships/shipid:685004/mmsi:563191300/imo:9290115/vessel:ONE_ATLAS',
            'https://www.marinetraffic.com/en/ais/details/ships/shipid:385499/mmsi:341548000/imo:1009314/vessel:PREDATOR',
            'https://www.marinetraffic.com/en/ais/details/ships/shipid:7236561/mmsi:256047000/imo:9885855/vessel:MINERVA_AMORGOS'
        ]

        # Common XPaths
        common_xpaths = {
            'Name': "/html/body/div[2]/main/section/div[2]/div[2]/div[2]/div/div[1]/div/section/div[2]/table/tbody/tr[1]/td",
            'IMO': "/html/body/div[2]/main/section/div[2]/div[2]/div[2]/div/div[1]/div/section/div[2]/table/tbody/tr[3]/td",
            'MMSI': "/html/body/div[2]/main/section/div[2]/div[2]/div[2]/div/div[1]/div/section/div[2]/table/tbody/tr[4]/td",
            'Speed': "/html/body/div[2]/main/section/div[2]/div[2]/div[2]/div/div[2]/div/section[1]/div/table/tbody/tr[5]/td",
            'Course': "/html/body/div[2]/main/section/div[2]/div[2]/div[2]/div/div[2]/div/section[1]/div/table/tbody/tr[6]/td"
        }

        ais_data_list = []

        for url in urls:
            # Navigate to the current URL
            driver.get(url)
            logging.info(f"Navigated to URL: {url}")

            # Wait for the page to load completely
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, common_xpaths['Name']))
            )

            # Extract data based on common XPaths
            ais_data = {}
            for key, xpath in common_xpaths.items():
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
                ais_data[key] = element.text

            # Add AIS data to list
            ais_data_list.append(ais_data)
            logging.info(f"Extracted data from URL: {url}")

        # Save AIS data list to JSON file
        with open('ais_data.json', 'w') as json_file:
            json.dump(ais_data_list, json_file, indent=4)
        logging.info("AIS data saved to JSON file.")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise

    finally:
        # Close webdriver
        driver.quit()
        logging.info("WebDriver closed.")


if __name__ == "__main__":
    main()
