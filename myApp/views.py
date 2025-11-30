from sklearn.metrics.pairwise import cosine_similarity
from django.shortcuts import render
import pandas as pd
import joblib
import numpy as np

# Lazy loading to reduce memory usage and startup time
_data = None
_kmeans = None

def get_data():
    global _data
    if _data is None:
        _data = pd.read_pickle('myApp/dataset/data.pkl')
    return _data

def get_kmeans():
    global _kmeans
    if _kmeans is None:
        _kmeans = joblib.load('myApp/models/kmeans_model.joblib')
    return _kmeans

def home(request):
    return render(request, 'index.html')

def get_recommendations(search_param, n_recommendations=6):
    try:
        # Load data and kmeans model
        data = get_data()
        kmeans = get_kmeans()
        
        # Filter data based on search parameter (case insensitive)
        search_results = data[
            data['Title'].str.contains(search_param, case=False, na=False) |
            data['Category'].str.contains(search_param, case=False, na=False) |
            data['Sub-Category'].str.contains(search_param, case=False, na=False)
        ]

        # If no results found, return empty list
        if search_results.empty:
            return []

        # Get the cluster label of the first matching product
        first_match_idx = search_results.index[0]
        cluster_label = kmeans.labels_[first_match_idx]

        # Get all products in the same cluster
        same_cluster_mask = kmeans.labels_ == cluster_label
        same_cluster_data = data[same_cluster_mask]
        
        # Get top N products from the same cluster (sorted by ratings)
        recommended_products = same_cluster_data.nlargest(n_recommendations, 'Ratings')
        
        # Format recommendations
        recommendations = []
        for idx, row in recommended_products.iterrows():
            recommendations.append({
                'Title': row['Title'],
                'Category': row['Category'],
                'Sub_Category': row['Sub-Category'],
                'Price': row['Price'],
                'Ratings': row['Ratings'],
                'Total_Ratings': round(row['Total Ratings'], 2)
            })
        
        return recommendations
    
    except Exception as e:
        print(f"Error in recommendations: {e}")
        # Return some random popular products as fallback
        data = get_data()
        fallback = data.nlargest(n_recommendations, 'Ratings')
        recommendations = []
        for idx, row in fallback.iterrows():
            recommendations.append({
                'Title': row['Title'],
                'Category': row['Category'],
                'Sub_Category': row['Sub-Category'],
                'Price': row['Price'],
                'Ratings': row['Ratings'],
                'Total_Ratings': round(row['Total Ratings'], 2)
            })
        return recommendations

def recommend_products(request):
    if request.method == 'POST':
        title = request.POST.get('product')
        print(title)

        # Get recommendations for the input product title
        recommendations_kmeans = get_recommendations(title)

        return render(request, 'index.html', {'recommendations': recommendations_kmeans})

    return render(request, 'index.html')
