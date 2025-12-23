import pickle
import re
import nltk
from nltk.corpus import stopwords

# Load stopwords
try:
    stop_words = set(stopwords.words('english'))
except:
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))

# Load the vectorizer and models
print("Loading models...")
with open('tfidf_vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

with open('mbti_models.pkl', 'rb') as f:
    models = pickle.load(f)

print("Models loaded!")

# Same cleaning function from data.py
def clean_text(text):
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = text.lower()
    words = [word for word in text.split() if word not in stop_words]
    return " ".join(words)

# The magic prediction function!
def predict_mbti(text):
    """
    Predict MBTI type from text
    
    Args:
        text: String of text to analyze
    
    Returns:
        Dictionary with type and confidence scores
    """
    # Step 1: Clean the text
    cleaned = clean_text(text)
    
    # Step 2: Vectorize (turn into numbers)
    features = vectorizer.transform([cleaned])
    
    # Step 3: Predict each dimension
    results = {}
    mbti_type = ""
    
    # I-E dimension
    pred_ie = models['I-E'].predict(features)[0]
    prob_ie = models['I-E'].predict_proba(features)[0]
    
    if pred_ie == 1:
        letter_ie = 'I'
        confidence_ie = prob_ie[1]
    else:
        letter_ie = 'E'
        confidence_ie = prob_ie[0]
    
    mbti_type += letter_ie
    results['I-E'] = {'letter': letter_ie, 'confidence': confidence_ie}
    
    # N-S dimension
    pred_ns = models['N-S'].predict(features)[0]
    prob_ns = models['N-S'].predict_proba(features)[0]
    
    if pred_ns == 1:
        letter_ns = 'N'
        confidence_ns = prob_ns[1]
    else:
        letter_ns = 'S'
        confidence_ns = prob_ns[0]
    
    mbti_type += letter_ns
    results['N-S'] = {'letter': letter_ns, 'confidence': confidence_ns}
    
    # T-F dimension
    pred_tf = models['T-F'].predict(features)[0]
    prob_tf = models['T-F'].predict_proba(features)[0]
    
    if pred_tf == 1:
        letter_tf = 'T'
        confidence_tf = prob_tf[1]
    else:
        letter_tf = 'F'
        confidence_tf = prob_tf[0]
    
    mbti_type += letter_tf
    results['T-F'] = {'letter': letter_tf, 'confidence': confidence_tf}
    
    # J-P dimension
    pred_jp = models['J-P'].predict(features)[0]
    prob_jp = models['J-P'].predict_proba(features)[0]
    
    if pred_jp == 1:
        letter_jp = 'J'
        confidence_jp = prob_jp[1]
    else:
        letter_jp = 'P'
        confidence_jp = prob_jp[0]
    
    mbti_type += letter_jp
    results['J-P'] = {'letter': letter_jp, 'confidence': confidence_jp}
    
    return {
        'type': mbti_type,
        'dimensions': results
    }

# Test it!
if __name__ == "__main__":
    print("\n--- Testing the Predictor ---")
    
    test_text = """
    I really enjoy spending time alone reading books and thinking about abstract concepts.
    I prefer to analyze things logically rather than going with my feelings.
    I like to plan things in advance and stick to a schedule.
    """
    
    result = predict_mbti(test_text)
    
    print(f"\nPredicted Type: {result['type']}")
    print("\nDimension Breakdown:")
    for dim, info in result['dimensions'].items():
        print(f"  {dim}: {info['letter']} (confidence: {info['confidence']*100:.1f}%)")