import requests
import json

slack_webhook_url = "your_webhook_url"  # Use the Webhook URL you copied from Slack


review_output = """
    I had a very disappointing experience at this hotel. While the room was decent, the service was abysmally slow. 
    The staff at the reception were completely unhelpful, and it took forever for them to check me in. 
    I had to wait more than 30 minutes, and they seemed disinterested in assisting me. 
    Furthermore, the food at the restaurant was cold, tasteless, and overpriced. I expect much better quality for the price I paid. 
    To make matters worse, the air conditioning in my room wasn't working properly, and when I called reception for help, no one answered the phone. 
    I won't be coming back anytime soon, and I will certainly not recommend this place to anyone.
"""

sentiment = "Negative"
area_responsible = "Reception"
recommendations = "Gym, Swimming Pool, Restaurant"

message = {
    "text": f"Review Alert:\n\nReview: {review_output}\n\nSentiment: {sentiment}\nArea Responsible For: {area_responsible}\nRecommendations: {recommendations}"
}

response = requests.post(slack_webhook_url, data=json.dumps(message), headers={'Content-Type': 'application/json'})

if response.status_code == 200:
    print("Message successfully sent to Slack!")
else:
    print(f"Failed to send message to Slack. Status code: {response.status_code}")
