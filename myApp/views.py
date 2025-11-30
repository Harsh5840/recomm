from sklearn.metrics.pairwise import cosine_similarity
from django.shortcuts import render
import pandas as pd
import joblib

# Lazy loading to reduce memory usage and startup time
_data = None
_preprocessor = None
_feature_matrix = None
_cosine_sim = None
_kmeans = None

def get_data():
    global _data
    if _data is None:
        _data = pd.read_pickle('myApp/dataset/data.pkl')
    return _data

def get_preprocessor():
    global _preprocessor
    if _preprocessor is None:
        _preprocessor = joblib.load('myApp/models/preprocessor.joblib')
    return _preprocessor

def get_feature_matrix():
    global _feature_matrix
    if _feature_matrix is None:
        data = get_data()
        preprocessor = get_preprocessor()
        _feature_matrix = preprocessor.transform(data)  # Use transform, not fit_transform
    return _feature_matrix

def get_cosine_sim():
    global _cosine_sim
    if _cosine_sim is None:
        feature_matrix = get_feature_matrix()
        _cosine_sim = cosine_similarity(feature_matrix, feature_matrix)
    return _cosine_sim

def get_kmeans():
    global _kmeans
    if _kmeans is None:
        _kmeans = joblib.load('myApp/models/kmeans_model.joblib')
    return _kmeans

# feature_matrix = joblib.load(open("myApp/models/feature_matrix.joblib", "rb"))
# feature_matrix = feature_matrix.reshape(-1, 1)

# Assuming feature_matrix is a 1D array, reshape it to a 2D array
# cosine_sim = cosine_similarity(feature_matrix, feature_matrix)

def home(request):
    return render(request, 'index.html')

def get_recommendations(search_param, n_recommendations=6):
    # Lazy load data and models
    data = get_data()
    kmeans = get_kmeans()
    cosine_sim = get_cosine_sim()
    
    # Filter data based on search parameter
    search_results = data[data['Title'].str.contains(search_param, case=False) |
                          (data['Category'] == search_param) |
                          (data['Sub-Category'] == search_param)]

    # If no results found, return an empty DataFrame
    if search_results.empty:
        return pd.DataFrame()

    cluster_label = kmeans.labels_[search_results.index[0]]

    # Get the indices of products in the same cluster
    cluster_indices = [i for i, label in enumerate(kmeans.labels_) if label == cluster_label]

    # Get the pairwise similarity scores within the cluster
    sim_scores = [(i, cosine_sim[search_results.index[0]][i]) for i in cluster_indices]

    # Sort the products based on similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the top N most similar products
    sim_scores = sim_scores[:n_recommendations]
    product_indices = [i[0] for i in sim_scores]
    
    # Use data from lazy loader
    data = get_data()
    recommendations_kmeans = []

    # Append the recommendations to the list
    for idx in product_indices:
        recommendations_kmeans.append({
            'Title': data.iloc[idx]['Title'],
            'Category': data.iloc[idx]['Category'],
            'Sub_Category': data.iloc[idx]['Sub-Category'],
            'Price': data.iloc[idx]['Price'],
            'Ratings': data.iloc[idx]['Ratings'],
            'Total_Ratings': round(data.iloc[idx]['Total Ratings'], 2)
        })

    return recommendations_kmeans

def recommend_products(request):
    if request.method == 'POST':
        title = request.POST.get('product')
        print(title)

        # Get recommendations for the input product title
        recommendations_kmeans = get_recommendations(title)

        return render(request, 'index.html', {'recommendations': recommendations_kmeans})

    return render(request, 'index.html')
