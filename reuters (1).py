from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import openpyxl

# Initialize the Chrome WebDriver
driver = webdriver.Chrome('chromedriver.exe')

# Define the URL of the Reuters archive page
url = 'https://www.reuters.com/company/google-llc/?view=page&page=5&pageSize=10'
driver.get(url)

# Initialize lists to store headlines and dates
headlines = []
dates = []

# Define the number of times to load more content
load_more_iterations = 500

# Initialize a flag to check if there is more content to load
more_content = True

# Loop to load more content and scrape data
for _ in range(load_more_iterations):
    try:
        # Find all news headlines and dates
        news_headlines = driver.find_elements(By.CLASS_NAME, "text__text__1FZLe.text__dark-grey__3Ml43.text__medium__1kbOh.text__heading_6__1qUJ5.heading__base__2T28j.heading__heading_6__RtD9P")
        news_dates = driver.find_elements(By.CLASS_NAME, "text__regular__2N1Xr")

        # Append the headlines and dates to the respective lists
        for headline, date in zip(news_headlines, news_dates):
            headlines.append(headline.text)
            dates.append(date.text)

        # Find the "Next" button for loading more content using a CSS selector
        load_more_button = driver.find_element(By.CSS_SELECTOR, '#fusion-app > div.search-layout__body__1FDkI > div.search-layout__main__L267c > div > div.search-results__pagination__2h60k > button:nth-child(3)').click()

        # Wait for the page to load
        time.sleep(3)

        # Check if there is a "Next" button on the page
        next_button_exists = driver.find_elements(By.CSS_SELECTOR, '#fusion-app > div.search-layout__body__1FDkI > div.search-layout__main__L267c > div > div.search-results__pagination__2h60k > button:nth-child(3)')

        if not next_button_exists:
            more_content = False

        print("Clicked!!")

    except Exception as e:
        print(e)
        break

    # If there is no more content to load, exit the loop
    if not more_content:
        break

# Close the WebDriver
driver.quit()

# Create an Excel file and write data to it
wb = openpyxl.Workbook()
ws = wb.active

# Write headers to the Excel file
ws.append(['Date', 'Headline'])

# Write data to the Excel file
for date, headline in zip(dates, headlines):
    ws.append([date, headline])

# Save the Excel file
wb.save('reuters_headlines.xlsx')
