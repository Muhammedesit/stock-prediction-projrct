import requests
import openpyxl
from datetime import datetime

# Set up the endpoint and parameters for the API request
url = "https://twitter154.p.rapidapi.com/hashtag/hashtag"
querystring = {"hashtag": "#aapl", "limit": "20", "section": "top"}
headers = {
    "X-RapidAPI-Key": "f79403133emsh23406b278f52a92p17fea2jsn2870f450cafb",
    "X-RapidAPI-Host": "twitter154.p.rapidapi.com"
}

# Make the API request
response = requests.get(url, headers=headers, params=querystring)

# Set the encoding to 'utf-8'
response.encoding = 'utf-8'

# Check if the request was successful
if response.status_code == 200:
    tweets_data = response.json()

    # Check the structure of the response
    print("Response structure:", type(tweets_data))
    if isinstance(tweets_data, dict) and 'results' in tweets_data:
        tweets = tweets_data['results']

        # Create a new Excel workbook
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = 'AAPL Hashtag Tweets'

        # Write the header row
        ws.append(['Tweet ID', 'Date', 'Tweet'])

        # Loop through each tweet in the response
        for tweet in tweets:
            try:
                # Extract data from tweet
                tweet_id = tweet.get('tweet_id', 'N/A')
                tweet_date = tweet.get('creation_date', 'N/A')
                tweet_text = tweet.get('text', '').encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')

                # Write the tweet's ID, date, and text to the Excel file
                ws.append([tweet_id, tweet_date, tweet_text])
            except Exception as e:
                print(f"An error occurred while processing a tweet: {e}")

        # Define the Excel filename with current datetime
        xlsx_filename = f'aapl_hashtag_tweets_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'

        # Save the Excel workbook
        wb.save(xlsx_filename)

        print(f"Tweets have been saved to {xlsx_filename}")
    else:
        print("No tweet data found in response.")
else:
    print("Failed to fetch tweets:", response.status_code)