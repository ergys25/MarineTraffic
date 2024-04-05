# Web Scraping MarineTraffic.com with Selenium

## Project Overview
This project involves scraping data from MarineTraffic.com after logging in. The scraped data includes details of nine vessels, such as Name, IMO, MMSI, Speed, Course, and True Heading. The data will be stored in a JSON array.

## Prerequisites
- Python 3.x
- Selenium
- WebDriver (e.g., geckodriver for Firefox)

## Getting Started

### Step 1: Clone the Repository
\`\`\`bash
git clone <repository_url>
cd <repository_directory>
\`\`\`

### Step 2: Install Required Packages
Install the required Python packages using pip and the provided \`requirements.txt\` file.
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### Step 3: Set Up WebDriver
Download the appropriate WebDriver (e.g., geckodriver for Firefox) and place it in the project directory or update the \`geckodriver_path\` in the code.

### Step 4: Update Credentials
Update the hardcoded email address and password in the code with your own MarineTraffic.com login credentials.

### Step 5: Run the Script
Run the Python script to execute the web scraping.
\`\`\`bash
python scrape_marinetraffic.py
\`\`\`

## Code Structure
- \`scrape_marinetraffic.py\`: Contains the main script for scraping data using Selenium.
- \`requirements.txt\`: Lists the required Python packages.

## How to Overcome reCAPTCHA Limitation
To automate the reCAPTCHA verification in the future, you can use services like 2Captcha or Anti-Captcha, which offer automated solutions for solving reCAPTCHA challenges. Alternatively, you can try implementing machine learning-based solutions to detect and solve reCAPTCHA challenges programmatically.

## Sample JSON Output
The extracted data will be stored in a JSON array in the following format:
\`\`\`json








[
    {"Name": "EFFIE", "IMO": "9591806", "MMSI": "538010145", "Speed": "12.2 kn", "Course": "207 \u00b0"},
    {"Name": "NEW FRIENDSHIP", "IMO": "9249180", "MMSI": "636018294", "Speed": "10.5 kn", "Course": "209 \u00b0"},
    {"Name": "LITTLE M", "IMO": "-", "MMSI": "240126100", "Speed": "0 kn", "Course": "-"},
    {"Name": "CMA CGM CONGO", "IMO": "9679892", "MMSI": "636018564", "Speed": "17.9 kn", "Course": "246 \u00b0"},
    {"Name": "HMM ST PETERSBURG", "IMO": "9868364", "MMSI": "440486000", "Speed": "3.8 kn", "Course": "315 \u00b0"},
    {"Name": "EMDEN", "IMO": "9941788", "MMSI": "636022757", "Speed": "15.3 kn", "Course": "217 \u00b0"},
    {"Name": "ONE ATLAS", "IMO": "9290115", "MMSI": "563191300", "Speed": "1.7 kn", "Course": "313 \u00b0"},
    {"Name": "PREDATOR", "IMO": "1009314", "MMSI": "341548000", "Speed": "0 kn", "Course": "325 \u00b0"},
    {"Name": "MINERVA AMORGOS", "IMO": "9885855", "MMSI": "256047000", "Speed": "13.9 kn", "Course": "207 \u00b0"}
]
\`\`\`
