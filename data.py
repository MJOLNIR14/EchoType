import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

df = pd.read_csv('mbti_1.csv')

print(df.head())

print(df['type'].value_counts())

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def clean_text(text):
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = text.lower()
    words = [word for word in text.split() if word not in stop_words]
    return " ".join(words)

df['cleaned_posts'] = df['posts'].apply(clean_text)

print(df[['type', 'cleaned_posts']].head())

# Extract individual MBTI dimensions from the type

# If first letter is 'I', mark as 1, otherwise 0
df['I-E'] = df['type'].apply(lambda x: 1 if x[0] == 'I' else 0)

# If second letter is 'N', mark as 1, otherwise 0
df['N-S'] = df['type'].apply(lambda x: 1 if x[1] == 'N' else 0)

# If third letter is 'T', mark as 1, otherwise 0
df['T-F'] = df['type'].apply(lambda x: 1 if x[2] == 'T' else 0)

# If fourth letter is 'J', mark as 1, otherwise 0
df['J-P'] = df['type'].apply(lambda x: 1 if x[3] == 'J' else 0)

# Distribution of each dimension
print("\n--- Dimension Distributions ---")
print(f"Introversion (I=1): {df['I-E'].sum()} | Extraversion (E=0): {len(df) - df['I-E'].sum()}")
print(f"Intuition (N=1): {df['N-S'].sum()} | Sensing (S=0): {len(df) - df['N-S'].sum()}")
print(f"Thinking (T=1): {df['T-F'].sum()} | Feeling (F=0): {len(df) - df['T-F'].sum()}")
print(f"Judging (J=1): {df['J-P'].sum()} | Perceiving (P=0): {len(df) - df['J-P'].sum()}")

# Verify it works
print("\n--- Sample Types with Dimensions ---")
print(df[['type', 'I-E', 'N-S', 'T-F', 'J-P']].head(10))

print("\n--- Vectorizing Text ---")

# Vectorizer
vectorizer = TfidfVectorizer(
    max_features=3000,
    min_df=5,
    max_df=0.7
)

# Transform the text into numbers
X = vectorizer.fit_transform(df['cleaned_posts'])

print(f"Text vectorized! Shape: {X.shape}")
print(f"This means: {X.shape[0]} posts, {X.shape[1]} features (words)")


from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

print("\n--- Training Model for I-E Dimension ---")
y_ie = df['I-E']
print(f"We're trying to predict: {y_ie.value_counts().to_dict()}")

X_train, X_test, y_train, y_test = train_test_split(
    X, y_ie, test_size=0.2, random_state=42, stratify=y_ie
)

print(f"\nTraining set: {X_train.shape[0]} people")
print(f"Test set: {X_test.shape[0]} people")

model_ie = LogisticRegression(max_iter=1000) 
print("\nTeaching the computer... (this might take a minute)")
model_ie.fit(X_train, y_train) 
print("Done learning!")

y_pred = model_ie.predict(X_test)  
accuracy = accuracy_score(y_test, y_pred)
print(f"\n✨ Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
print("\n--- Detailed Results ---")
print(classification_report(y_test, y_pred, target_names=['Extravert (E)', 'Introvert (I)']))

print("\n--- Training Model for N-S Dimension ---")
y_ns = df['N-S']
print(f"We're trying to predict: {y_ns.value_counts().to_dict()}")

X_train, X_test, y_train, y_test = train_test_split(
    X, y_ns, test_size=0.2, random_state=42, stratify=y_ns
)

print(f"\nTraining set: {X_train.shape[0]} people")
print(f"Test set: {X_test.shape[0]} people")

model_ns = LogisticRegression(max_iter=1000) 
print("\nTeaching the computer... (this might take a minute)")
model_ns.fit(X_train, y_train)  
print("Done learning!")

y_pred = model_ns.predict(X_test)  
accuracy = accuracy_score(y_test, y_pred)
print(f"\n✨ Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
print("\n--- Detailed Results ---")
print(classification_report(y_test, y_pred, target_names=['Intuitive (N)', 'Sensing (S)']))

print("\n--- Training Model for T-F Dimension ---")
y_tf = df['T-F']
print(f"We're trying to predict: {y_tf.value_counts().to_dict()}")

X_train, X_test, y_train, y_test = train_test_split(
    X, y_tf, test_size=0.2, random_state=42, stratify=y_tf
)

print(f"\nTraining set: {X_train.shape[0]} people")
print(f"Test set: {X_test.shape[0]} people")

model_tf = LogisticRegression(max_iter=1000) 
print("\nTeaching the computer... (this might take a minute)")
model_tf.fit(X_train, y_train)  
print("Done learning!")

y_pred = model_tf.predict(X_test)  
accuracy = accuracy_score(y_test, y_pred)
print(f"\n✨ Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
print("\n--- Detailed Results ---")
print(classification_report(y_test, y_pred, target_names=['Thinking (T)', 'Feeling (F)']))

print("\n--- Training Model for J-P Dimension ---")
y_jp = df['J-P']
print(f"We're trying to predict: {y_jp.value_counts().to_dict()}")

X_train, X_test, y_train, y_test = train_test_split(
    X, y_jp, test_size=0.2, random_state=42, stratify=y_jp
)

print(f"\nTraining set: {X_train.shape[0]} people")
print(f"Test set: {X_test.shape[0]} people")

model_jp = LogisticRegression(max_iter=1000) 
print("\nTeaching the computer... (this might take a minute)")
model_jp.fit(X_train, y_train)  
print("Done learning!")

y_pred = model_jp.predict(X_test)  
accuracy = accuracy_score(y_test, y_pred)
print(f"\n✨ Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
print("\n--- Detailed Results ---")
print(classification_report(y_test, y_pred, target_names=['Judging (J)', 'Perceiving (P)']))

import pickle
print("\n--- Saving All Models ---")

# Save the vectorizer
with open('tfidf_vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)
print("✓ Saved: tfidf_vectorizer.pkl")

# Save all 4 MODELS 
models_dict = {
    'I-E': model_ie,  
    'N-S': model_ns,  
    'T-F': model_tf,  
    'J-P': model_jp   
}

with open('mbti_models.pkl', 'wb') as f:
    pickle.dump(models_dict, f)
print("✓ Saved: mbti_models.pkl")

print("\n🎉 All done! You can now use these models for predictions!")