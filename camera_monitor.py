import os
import django
import requests
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "camera_log_project.settings")
django.setup()
# Import the CameraLog model from Django
from camera_log.models import CameraLog
# Configure Chrome WebDriver
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
# Update with your correct ChromeDriver path
service = Service("chromedriver-win64/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)
# Slack configuration
slack_webhook_url = "https://hooks.slack.com/services/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"
# Track start time of status changes
status_start_times = {}
# Function to send Slack notifications
def send_slack_notification(camera_id, status):
    message = f"Camera {camera_id} status changed: {status}"
    payload = {"text": message}
    try:
        response = requests.post(slack_webhook_url, json=payload)
        if response.status_code != 200:
            print(f"Slack notification failed: {response.text}")
        else:
            print(f"Notification sent to Slack for {camera_id}: {status}")
    except Exception as e:
        print(f"Error sending Slack notification: {e}")
# Function to check the camera status and log data in the Django database
def check_camera_status():
    driver.get("https://support-team-bpf.landmark.oly.live/dashboard")
    # Wait for the table to load
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table tbody tr')))
    except Exception as e:
        print(f"Error loading page: {e}")
        return
    # Find the table rows
    rows = driver.find_elements(By.CSS_SELECTOR, 'table tbody tr')
    for row in rows:
        camera_id = row.find_element(By.CSS_SELECTOR, 'td:nth-child(2)').text
        status_color = row.get_attribute("class")
        status = ""
        if 'highlight-critical' in status_color:
            status = 'AI not working (Red)'
        elif 'highlight-inactive' in status_color:
            status = 'Camera inactive (Yellow)'
        if status:
            timestamp = datetime.now()
            start_time = status_start_times.get(camera_id, timestamp)  # Use previous start time if available
            duration = (timestamp - start_time).total_seconds() / 60  # Duration in minutes
            # Save log entry to Django database
            log_entry = CameraLog(
                timestamp=timestamp,
                camera_id=camera_id,
                status=status,
                start_time=start_time,
                end_time=timestamp,
                duration=duration
            )
            log_entry.save()  # Save the log to the database
            # Update the start time for the next check
            status_start_times[camera_id] = timestamp
            # Send Slack notification
            send_slack_notification(camera_id, status)
    print(f"Status checked and logged at {datetime.now()}")
# Main loop to run every 10 minutes
try:
    while True:
        check_camera_status()
        time.sleep(600)  # Wait 10 minutes
finally:
    driver.quit()