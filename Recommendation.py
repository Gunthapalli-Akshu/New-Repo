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


user_id = 1
hybrid_recommendations = hybrid_recommendation(user_id, user_similarity_df, user_item_matrix, item_similarity_df)


item_names = {1: "Gym", 2: "Spa", 3: "Swimming Pool", 4: "Restaurant"}


recommended_items = [item_names[item] for item in hybrid_recommendations]
print(f"Hybrid Recommendations for User {user_id}: {recommended_items}")


#SUBMIT THE REVIEW
import requests
import json
url = 'http://127.0.0.1:5000/review'
headers = {'Content-Type': 'application/json'}
data = {
    "hotel_name": "Hotel Sunshine",  # Hotel name
    "rating": 4,                     # Rating (1-5)
    "amenities": ["pool", "gym"],    # Amenities at the hotel
    "room_preference": "sea view",   # Room preference
    "comments": "Great stay, but could improve breakfast options."  # Additional comments
}
response = requests.post(url, headers=headers, data=json.dumps(data))

# Print the response
print(response.json())
