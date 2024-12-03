# Microsoft Stream Video Downloader

## Overview
A Python script to download videos from Microsoft Stream using Selenium for authentication.

## Prerequisites
- Python 3.7+
- Chrome Browser

## Installation
1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
```python
from ms_stream_downloader import MSStreamDownloader

# Initialize downloader with your credentials
downloader = MSStreamDownloader('your_email@example.com', 'your_password')

# Download a video
downloaded_path = downloader.download_video('https://web.microsoftstream.com/video/your-video-id')
print(f'Video downloaded to: {downloaded_path}')

# Close the session
downloader.close()
```

## Notes
- Requires Microsoft Stream login credentials
- Uses Selenium for authentication
- Supports downloading videos to a specified path

## Disclaimer
Ensure you have the right to download and use the videos.
