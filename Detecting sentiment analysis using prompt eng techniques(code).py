import requests
import time

#Define your Hugging Face API key
api_key = "your_hugging_face_api_key"  # Replace with your actual Hugging Face API key

#Define the API endpoint and headers for BLOOM model
api_url = "https://api-inference.huggingface.co/models/bigscience/bloom"  # BLOOM model URL
headers = {
    "Authorization": f"Bearer {api_key}",
}

#Define a function to make the request to Hugging Face's API 
def classify_sentiment(feedback_text):
    payload = {
        "inputs": f"Classify the sentiment of the following review as Positive, Negative, or Neutral: {feedback_text}",
        "parameters": {
            "max_length": 50,  
            "temperature": 0.7,  
            "top_p": 0.9,  
            "top_k": 50  
        }
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

#Define one short hotel feedback
guest_feedback = "The hotel was great, the staff was friendly, and the room was clean, but the breakfast could have been better."

#Create prompts for different techniques

prompts = []

# Zero-shot: No prior examples, just classify based on the text
prompts.append(("Zero-shot", f"Classify the sentiment of the following review as Positive, Negative, or Neutral: {guest_feedback}"))

# Few-shot: Provide a few examples to guide the model
few_shot_prompt = """
Classify the sentiment of the following reviews as Positive, Negative, or Neutral:
Review: 'The room was clean, and the staff were very polite.'
Sentiment: Positive

Review: 'The room was dirty and uncomfortable. The bed was hard, and the sheets were not clean.'
Sentiment: Negative
"""

prompts.append(("Few-shot", f"{few_shot_prompt} Review: '{guest_feedback}'"))

# Direct: Directly asking the model for sentiment
prompts.append(("Direct", f"Classify the sentiment of the following review as Positive, Negative, or Neutral: {guest_feedback}"))

# Contextual: Making it more conversational
prompts.append(("Contextual", f"Based on the review: '{guest_feedback}', how would you rate the sentiment as positive, negative, or neutral?"))

# Structured: Requesting a structured response
prompts.append(("Structured", f"""
Please classify the sentiment of the following review:
Review: '{guest_feedback}'
Output format: Sentiment = [Positive, Negative, Neutral]
"""))

#Generate output using BLOOM for each technique
for prompt_name, prompt in prompts:
    print(f"Using {prompt_name} Prompt: \n{prompt}\n")
    response = classify_sentiment(prompt)
    
    #Process the response and extract the sentiment
    if isinstance(response, list) and len(response) > 0:
        # Check the content of the response for sentiment classification
        generated_text = response[0].get('generated_text', '').strip() if isinstance(response[0], dict) else None
        
        if generated_text:
            # Simple logic to determine sentiment from the output
            if "positive" in generated_text.lower():
                sentiment = "POSITIVE"
            elif "negative" in generated_text.lower():
                sentiment = "NEGATIVE"
            elif "neutral" in generated_text.lower():
                sentiment = "NEUTRAL"
            else:
                sentiment = "NEUTRAL"
            
            print(f"Sentiment from {prompt_name} Feedback: {sentiment}")
        else:
            print(f"Error: No generated text found for {prompt_name} feedback")
    else:
        print(f"Unexpected response format for {prompt_name} feedback:")
        print(response)
    
    print("\n" + "-" * 50 + "\n")
