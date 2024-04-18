import requests
import csv
from datetime import datetime

# API endpoint and parameters
url = "https://x-com2.p.rapidapi.com/v1.1/SearchTweets/"
querystring = {"q":"$aapl","count":"50","until":"2024-03-01","lang":"english"}
headers = {
    "X-RapidAPI-Key": "f79403133emsh23406b278f52a92p17fea2jsn2870f450cafb",
    "X-RapidAPI-Host": "x-com2.p.rapidapi.com"
}

# Make the API request
response = requests.get(url, headers=headers, params=querystring)

# Check if the request was successful
if response.status_code == 200:
    tweets_data = response.json()

    # Define the CSV filename with current datetime
    csv_filename = f'aapl_tweets_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    
    # Open the CSV file for writing
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write the header row
        writer.writerow(['Date', 'Tweet'])
        
        # Write tweet data
        for tweet in tweets_data['statuses']:
            tweet_date = tweet['created_at']  # The date when the tweet was created
            tweet_text = tweet['text']        # The text content of the tweet
            
            # Write the tweet's date and text to the CSV file
            writer.writerow([tweet_date, tweet_text])
            
    print(f"Tweets have been saved to {csv_filename}")
else:
    print("Failed to fetch tweets:", response.status_code)