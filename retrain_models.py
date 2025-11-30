"""
Retrain ML models with scikit-learn 1.6.1 for Python 3.13 compatibility
"""
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import DBSCAN, KMeans
import joblib
import warnings
warnings.filterwarnings('ignore')

print("Loading dataset...")
data = pd.read_csv('dataset_and_machine_learning_files/amazon_data.csv', on_bad_lines='skip')

print(f"Dataset shape: {data.shape}")

# Convert columns to numeric type
data['Price'] = pd.to_numeric(data['Price'], errors='coerce')
data['Ratings'] = pd.to_numeric(data['Ratings'], errors='coerce')
data['Total Ratings'] = pd.to_numeric(data['Total Ratings'], errors='coerce')

# Calculate the mean of each column
price_mean = data['Price'].mean()
ratings_mean = data['Ratings'].mean()
total_ratings_mean = data['Total Ratings'].mean()

# Fill NaN values with the mean of each column
data['Price'].fillna(price_mean, inplace=True)
data['Ratings'].fillna(ratings_mean, inplace=True)
data['Total Ratings'].fillna(total_ratings_mean, inplace=True)

print("Preprocessing features...")
# Combine relevant columns into a single feature
data['Features'] = data['Title'] + ' ' + data['Category'] + ' ' + data['Sub-Category']

# Define the feature transformation steps
preprocessor = ColumnTransformer(
    transformers=[
        ('text', TfidfVectorizer(stop_words='english'), 'Features'),
        ('numeric', StandardScaler(), ['Price', 'Ratings', 'Total Ratings']),
        ('categorical', OneHotEncoder(), ['Category', 'Sub-Category'])
    ]
)

# Transform the features
print("Transforming features...")
feature_matrix = preprocessor.fit_transform(data)

print("Training DBSCAN model...")
# Clustering using DBSCAN
dbscan = DBSCAN(eps=0.5, min_samples=5)
dbscan.fit(feature_matrix)

print("Training K-Means model...")
# Clustering using K-means
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(feature_matrix)

print("Saving models...")
# Save the models
joblib.dump(preprocessor, 'myApp/models/preprocessor.joblib')
joblib.dump(dbscan, 'myApp/models/dbscan_model.joblib')
joblib.dump(kmeans, 'myApp/models/kmeans_model.joblib')

print("Saving dataset...")
# Save the processed data
data.to_pickle('myApp/dataset/data.pkl')

print("\n✅ All models retrained and saved successfully!")
print(f"   - preprocessor.joblib (scikit-learn {__import__('sklearn').__version__})")
print(f"   - dbscan_model.joblib")
print(f"   - kmeans_model.joblib")
print(f"   - data.pkl ({len(data)} products)")
