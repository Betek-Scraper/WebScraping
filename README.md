# How to Download and Use `chromedriver_win32.zip`

This guide explains how to download `chromedriver_win32.zip`, extract it, and configure it for use in your project.

## Prerequisites

Make sure you have:
- **Python** installed (if you're using it for automation or web scraping)
- **Google Chrome** installed on your system

## Step 1: Download `chromedriver_win32.zip`

1. Go to the official ChromeDriver download page: [ChromeDriver - WebDriver for Chrome](https://sites.google.com/chromium.org/driver/).
2. Identify the version of Chrome installed on your computer:
   - Open Chrome, and click on the three dots in the top right corner.
   - Go to **Help** > **About Google Chrome**.
   - Note the version number (e.g., `114.0.5735.90`).
3. Find and download the matching version of ChromeDriver for your Chrome version on the download page.
4. Click on the **chromedriver_win32.zip** link to download the file.

## Step 2: Extract `chromedriver_win32.zip`

1. Once downloaded, locate `chromedriver_win32.zip` in your Downloads folder.
2. Right-click on the file and select **Extract All...**.
3. Extract it to a location that is easy to access, such as `C:\chromedriver` or within your project folder.

## Step 3: Add ChromeDriver to System Path (Optional but Recommended)

To make ChromeDriver accessible from anywhere on your system, add it to the system PATH:

1. Open the **Start Menu** and search for **Environment Variables**.
2. Select **Edit the system environment variables**.
3. In the **System Properties** window, click **Environment Variables**.
4. In the **System Variables** section, find the `Path` variable and select **Edit**.
5. Click **New** and add the path where you extracted `chromedriver.exe` (e.g., `C:\chromedriver`).
6. Click **OK** to save the changes.

## Step 4: Using ChromeDriver in Your Project

You can now use ChromeDriver in your Python project with Selenium. Here’s a simple example:

```python
from selenium import webdriver

# Ensure chromedriver.exe is in your PATH or specify the path directly
driver = webdriver.Chrome(executable_path='path_to_your_chromedriver')  # Update path if needed

# Open a webpage
driver.get("https://www.google.com")

# Close the driver
driver.quit()
