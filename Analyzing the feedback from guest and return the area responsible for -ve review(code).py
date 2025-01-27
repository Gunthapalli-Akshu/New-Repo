import requests
import time

#Define your Hugging Face API key
api_key = "your_hugging_face_api_key" 

#Define the API endpoint and headers (for BLOOM model)
api_url = "https://api-inference.huggingface.co/models/bigscience/bloom"  # BLOOM model endpoint
headers = {
    "Authorization": f"Bearer {api_key}",
}

def classify_sentiment(feedback_text):
    # Create a prompt for BLOOM to classify the sentiment and responsible area
    prompt = f"Classify the sentiment and responsible area for the following feedback: \n\n{feedback_text}\n\nResponse:"

    payload = {
        "inputs": prompt
    }

    retries = 5
    for attempt in range(retries):
        response = requests.post(api_url, headers=headers, json=payload)

        if response.status_code == 200:
            result = response.json()
            return result  # Return the response directly for debugging
            
        elif response.status_code == 503:
            wait_time = 2 ** attempt  # Exponential backoff
            print(f"Model is loading. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
        else:
            return f"Error: {response.status_code}, {response.text}"
    
    return "Error: Model could not be loaded after multiple attempts."

#Example guest feedbacks (short negative feedbacks)
guest_feedbacks = [
    "The room was fine, but the service at the reception was terrible. The staff was unhelpful, and it took forever to check in.",
    "The breakfast was awful. The food was cold and tasteless. I would never come back for a meal here.",
    "The air conditioning in my room was broken, and when I called reception, no one answered. Very frustrating experience."
]

#Analyze each feedback
for guest_feedback in guest_feedbacks:
    print(f"\nAnalyzing Feedback: {guest_feedback}")
    
    #Classify sentiment and responsible area using Hugging Face API (BLOOM model)
    response = classify_sentiment(guest_feedback)

    #Check if the response is structured as expected
    if isinstance(response, list) and len(response) > 0:
        generated_text = response[0].get('generated_text', '').strip()
        print("Generated Text by BLOOM:", generated_text)

        #negative keywords
        negative_keywords = ["terrible", "worst", "disappointing", "slow","broken", "unbearably hot", "cold", "tasteless", "bad", "uninterested"]
        
        feedback_lower = guest_feedback.lower()
        
        # Check if any negative sentiment keywords are found
        if any(keyword in feedback_lower for keyword in negative_keywords):
            sentiment = "NEGATIVE"
        else:
            sentiment = "POSITIVE"

        # Check for responsible area based on keywords
        dining_keywords = ["dining", "breakfast", "food", "meal", "restaurant", "cafe", "dinner"]
        reception_keywords = ["reception", "check-in", "front desk", "staff", "service", "air conditioning"]

        # Check for dining-related issues
        if any(keyword in feedback_lower for keyword in dining_keywords):
            area = "Dining"
        # Check for reception-related issues
        elif any(keyword in feedback_lower for keyword in reception_keywords):
            area = "Reception"
        else:
            area = "General"  

        print(f"Sentiment: {sentiment}")
        print(f"Responsible Area: {area}")
    else:
        # If the response format is not as expected, print the raw response
        print("Unexpected response format:")
        print(response)
