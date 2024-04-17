import json
import logging
import re
import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure logging
logging.basicConfig(filename='script.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def initialize_driver(geckodriver_path):
    """Initialize and return a Firefox webdriver."""
    driver = webdriver.Firefox()
    return driver


def main():
    try:
        # Set path to geckodriver
        geckodriver_path = '/usr/local/bin/geckodriver'

        # Initialize Firefox webdriver
        driver = initialize_driver(geckodriver_path)
        logging.info("WebDriver initialized successfully.")

        # Navigate to the login page
        driver.get('https://www.marinetraffic.com/en/users/login')
        logging.info("Navigated to login page.")

        # Wait for the login button to be clickable
        wait = WebDriverWait(driver, 10)
        login_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/button[2]"))
        )
        login_button.click()
        logging.info("Login button clicked successfully.")

        # Enter email address
        email_input = wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "/html/body/div/main/section/div[2]/div/div/div[2]/div/form/div/div/div[1]/div/div/input"))
        )
        email_input.send_keys("---your-email---")  # Your email
        logging.info("Email address entered successfully.")

        # Enter password
        password_input = wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "/html/body/div/main/section/div[2]/div/div/div[2]/div/form/div/div/div[2]/div/div/input"))
        )
        password_input.send_keys("---your-password")  # Your password
        logging.info("Password entered successfully.")

        # Click the login button
        login_submit_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div/main/section/div[2]/div/div/div[2]/div/form/div/div/div[5]/button"))
        )
        login_submit_button.click()
        logging.info("Login button clicked successfully.")

        # Ships to search
        ships = ["9435832", "9352872", "9301653", "7427154"]

        # Common XPaths
        common_xpaths = {
            'Name': "/html/body/div/main/section/div[2]/div/div[2]/div/div[1]/div/section/div[2]/table/tbody/tr[1]/td",
            'Estimated Time Of Arrival': '//*[@id="vesselDetails_aisInfoSection"]/div/table/tbody/tr[12]/td',
            'IMO': "/html/body/div/main/section/div[2]/div/div[2]/div/div[1]/div/section/div[2]/table/tbody/tr[3]/td",
            'MMSI': "/html/body/div/main/section/div[2]/div/div[2]/div/div[1]/div/section/div[2]/table/tbody/tr[4]/td",
            'Speed': "/html/body/div/main/section/div[2]/div/div[2]/div/div[2]/div/section[1]/div/table/tbody/tr[5]/td",
            'Course': "/html/body/div/main/section/div[2]/div/div[2]/div/div[2]/div/section[1]/div/table/tbody/tr[6]/td",
            'Longitude/Latitude': '//*[@id="vesselDetails_aisInfoSection"]/div/table/tbody/tr[4]/td/a',
            'Predicted Time Of Arrival': '//*[@id="vesselDetails_voyageSection"]/div/div[2]/div/div[3]/div/div[2]/div/span[2]',
        }

        ais_data_list = []

        for ship in ships:
            time.sleep(5)
            driver.get(
                'https://www.marinetraffic.com/en/data/?asset_type=vessels&columns=flag%2Cshipname%2Cphoto%2Crecognized_next_port%2Creported_eta%2Creported_destination%2Ccurrent_port%2Cimo%2Cship_type%2Cshow_on_live_map%2Ctime_of_latest_position%2Clat_of_latest_position%2Clon_of_latest_position%2Cnotes')
            logging.info("Navigated to data page.")
            time.sleep(5)

            # Enter IMO to search
            password_input = wait.until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id=":r3:"]'))
            )
            password_input.send_keys(ship)  # Your password
            logging.info("Password entered successfully.")

            time.sleep(2)

            # Press down once
            password_input.send_keys(Keys.DOWN)

            time.sleep(2)
            password_input.send_keys(Keys.ENTER)

            # Click the ship to scrape
            search_bar = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="mainSection"]/div[2]/div/div/div[3]/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div/a'))
            )
            search_bar.click()
            logging.info("Login button clicked successfully.")

            # Extract AIS data
            ais_data = {}
            for key, xpath in common_xpaths.items():
                element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                ais_data[key] = element.text

            # Extract numeric values and units using regex for Speed
            speed_match = re.match(r'(\d+\.*\d*)\s*kn', ais_data['Speed'])
            if speed_match:
                ais_data['Speed_Value'] = float(speed_match.group(1))
            course_match = re.match(r'(\d+)\s*(°)', ais_data['Course'])
            if course_match:
                ais_data['Course_Value'] = int(course_match.group(1))
                ais_data['Course_Unit'] = course_match.group(2)

            # Add AIS data to list
            ais_data_list.append(ais_data)
            logging.info(f"Extracted data from URL: {driver.current_url}")

            # Pause for 5 seconds before the next iteration
            time.sleep(2)

            # Go to live view by pressing the live view button
            live_view_button = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="showOnMapCTA"]'))
            )
            live_view_button.click()
            logging.info('//*[@id="showOnMapCTA"]')


            time.sleep(5)
            xpath = '//*[@id="mainSection"]/div[2]/div/div/div/div[1]/div[4]/div/div/div/div/div/div[3]/div/span'
            element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            key = 'InsertedDT'
            title_attribute = element.get_attribute('title')
            ais_data[key] = title_attribute if title_attribute else element.text
            time.sleep(2)

            # Extract and format latitude and longitude
            lat_lon = ais_data['Longitude/Latitude'].split(' / ')
            ais_data['Latitude'] = float(re.search(r'[-+]?\d*\.\d+|\d+', lat_lon[0]).group())
            ais_data['Longitude'] = float(re.search(r'[-+]?\d*\.\d+|\d+', lat_lon[1]).group())

            # Convert Estimated Time Of Arrival and Predicted Time Of Arrival to UTC datetime
            for key in ['Estimated Time Of Arrival', 'Predicted Time Of Arrival']:
                if ais_data[key]:
                    timestamp_match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}) \(UTC([+-]\d+)\)', ais_data[key])
                    if timestamp_match:
                        dt = datetime.strptime(timestamp_match.group(1), '%Y-%m-%d %H:%M')
                        offset_hours = int(timestamp_match.group(2))
                        dt_utc = dt - timedelta(hours=offset_hours)
                        ais_data[key] = dt_utc.strftime('%Y-%m-%d %H:%M:%S')

            # Format InsertedDT as YYYY-MM-DD HH:MM
            if ais_data['InsertedDT']:
                ais_data['InsertedDT'] = re.sub(r' UTC$', '', ais_data['InsertedDT'])

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
