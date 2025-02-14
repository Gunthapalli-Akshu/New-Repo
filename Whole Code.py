import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


user_item_data = {
    'user_id': [1, 1, 2, 2, 3, 3, 4, 4],
    'item_id': [1, 2, 1, 3, 2, 3, 1, 4],
    'interaction_score': [5, 3, 4, 2, 5, 4, 3, 5]  
}


item_features_data = {
    'item_id': [1, 2, 3, 4],
    'feature1': [1, 0, 1, 1],  # E.g., Indoor vs Outdoor
    'feature2': [0, 1, 0, 1],  # E.g., Fitness vs Relaxation
    'feature3': [1, 0, 1, 0]   # E.g., Adventure vs Leisure
}


user_item_df = pd.DataFrame(user_item_data)
item_features_df = pd.DataFrame(item_features_data)


user_item_matrix = user_item_df.pivot(index='user_id', columns='item_id', values='interaction_score').fillna(0)


user_similarity = cosine_similarity(user_item_matrix)
user_similarity_df = pd.DataFrame(user_similarity, index=user_item_matrix.index, columns=user_item_matrix.index)


item_features = item_features_df.drop(columns=['item_id'])
item_similarity = cosine_similarity(item_features)
item_similarity_df = pd.DataFrame(item_similarity, index=item_features_df['item_id'], columns=item_features_df['item_id'])


def collaborative_filtering(user_id, user_similarity_df, user_item_matrix, top_n=3):
    similar_users = user_similarity_df[user_id].sort_values(ascending=False).drop(user_id)
    item_scores = {}

    for similar_user, similarity in similar_users.items():
        similar_user_ratings = user_item_matrix.loc[similar_user]
        for item_id, rating in similar_user_ratings.items():
            if rating > 0:
                if item_id not in item_scores:
                    item_scores[item_id] = 0
                item_scores[item_id] += similarity * rating

    recommended_items = sorted(item_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
    return [item[0] for item in recommended_items]


def content_based_filtering(user_id, user_item_matrix, item_similarity_df, top_n=3):
    user_ratings = user_item_matrix.loc[user_id]
    item_scores = {}

    for item_id, rating in user_ratings.items():
        if rating > 0:
            similar_items = item_similarity_df[item_id]
            for similar_item, similarity in similar_items.items():
                if similar_item not in item_scores:
                    item_scores[similar_item] = 0
                item_scores[similar_item] += similarity * rating

    recommended_items = sorted(item_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
    return [item[0] for item in recommended_items]


def hybrid_recommendation(user_id, user_similarity_df, user_item_matrix, item_similarity_df, top_n=3, alpha=0.5):
    collaborative_recs = collaborative_filtering(user_id, user_similarity_df, user_item_matrix, top_n)
    content_based_recs = content_based_filtering(user_id, user_item_matrix, item_similarity_df, top_n)
    
    hybrid_scores = {}
    
    for item in set(collaborative_recs + content_based_recs):
        collaborative_score = collaborative_recs.count(item)
        content_based_score = content_based_recs.count(item)
        
        hybrid_scores[item] = alpha * collaborative_score + (1 - alpha) * content_based_score
    
    hybrid_recs = sorted(hybrid_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
    return [item[0] for item in hybrid_recs]


guest_feedback = """
    I had a very disappointing experience at this hotel. While the room was decent, the service was abysmally slow. 
    The staff at the reception were completely unhelpful, and it took forever for them to check me in. 
    I had to wait more than 30 minutes, and they seemed disinterested in assisting me. 
    Furthermore, the food at the restaurant was cold, tasteless, and overpriced. I expect much better quality for the price I paid. 
    To make matters worse, the air conditioning in my room wasn't working properly, and when I called reception for help, no one answered the phone. 
    I won't be coming back anytime soon, and I will certainly not recommend this place to anyone.
"""


def determine_sentiment(feedback):
    negative_keywords = ["disappointing", "terrible", "worst", "slow", "unhelpful", "cold", "tasteless", "overpriced", "frustrating"]
    positive_keywords = ["decent", "good", "helpful", "comfortable", "great"]
    
    sentiment = "Neutral"
    
    feedback_lower = feedback.lower()
    
    if any(keyword in feedback_lower for keyword in negative_keywords):
        sentiment = "Negative"
    elif any(keyword in feedback_lower for keyword in positive_keywords):
        sentiment = "Positive"
    
    return sentiment


area_keywords = {
    "Dining": ["dining", "breakfast", "food", "meal", "restaurant", "cafe"],
    "Reception": ["reception", "check-in", "staff", "service", "air conditioning"]
}


def determine_area(feedback):
    for area, keywords in area_keywords.items():
        if any(keyword in feedback.lower() for keyword in keywords):
            return area
    return "General"


def get_recommendations(user_id):
    hybrid_recommendations = hybrid_recommendation(user_id, user_similarity_df, user_item_matrix, item_similarity_df)
    item_names = {1: "Gym", 2: "Spa", 3: "Swimming Pool", 4: "Restaurant"}
    recommended_items = [item_names[item] for item in hybrid_recommendations]
    return recommended_items


sentiment = determine_sentiment(guest_feedback)
area_responsible = determine_area(guest_feedback)
recommended_items = get_recommendations(user_id=1)

print(f"Review: {guest_feedback}")
print(f"Sentiment: {sentiment}")
print(f"Area Responsible For: {area_responsible}")
print(f"Recommendations: {', '.join(recommended_items)}")
