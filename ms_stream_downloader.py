import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class MSStreamDownloader:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.driver = None
        self.session = requests.Session()

    def login(self):
        # Setup Chrome WebDriver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        
        # Navigate to Microsoft Stream login
        self.driver.get('https://web.microsoftstream.com/browse')
        
        # Wait for and fill in email
        email_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'loginfmt'))
        )
        email_input.send_keys(self.email)
        self.driver.find_element(By.ID, 'idSIButton9').click()
        
        # Wait for and fill in password
        password_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'passwd'))
        )
        password_input.send_keys(self.password)
        self.driver.find_element(By.ID, 'idSIButton9').click()
        
        # Handle stay signed in prompt
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'idSIButton9'))
        ).click()

    def download_video(self, video_url, output_path=None):
        # Ensure login
        if not self.driver:
            self.login()
        
        # Navigate to video
        self.driver.get(video_url)
        
        # Wait for video to load and get download link
        video_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'video'))
        )
        video_src = video_element.get_attribute('src')
        
        # Determine output path
        if not output_path:
            output_path = os.path.join(os.getcwd(), 'downloaded_video.mp4')
        
        # Download video
        response = self.session.get(video_src, stream=True)
        with open(output_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        return output_path

    def close(self):
        if self.driver:
            self.driver.quit()

# Example usage
if __name__ == '__main__':
    downloader = MSStreamDownloader('your_email@example.com', 'your_password')
    try:
        video_url = 'https://web.microsoftstream.com/video/your-video-id'
        downloaded_path = downloader.download_video(video_url)
        print(f'Video downloaded to: {downloaded_path}')
    finally:
        downloader.close()
