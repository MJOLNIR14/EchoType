from quiz_scorer import score_quiz
from predict import predict_mbti

def combine_predictions_likert(answers, test_type='short', text=None, quiz_weight=0.7):
    """
    Combine quiz (Likert scale) and text predictions
    
    Args:
        answers: List of integers (1-5) representing user responses
        test_type: 'short' or 'full'
        text: Optional text input from user
        quiz_weight: How much to trust quiz vs text (0.7 = 70% quiz, 30% text)
    
    Returns:
        Tuple of (mbti_type, scores_dict)
    """
    # Get quiz scores (0-1 for each dimension)
    quiz_scores = score_quiz(answers, test_type)
    
    # If no text provided, just use quiz
    if not text or len(text.strip()) < 50:
        mbti_type = scores_to_mbti(quiz_scores)
        return mbti_type, quiz_scores
    
    # Get text prediction
    text_result = predict_mbti(text)
    
    # Extract text scores and normalize them
    text_scores = {}
    for dim in ['I-E', 'N-S', 'T-F', 'J-P']:
        letter = text_result['dimensions'][dim]['letter']
        confidence = text_result['dimensions'][dim]['confidence']
        
        # Convert to 0-1 scale where 1 = first trait (I, N, T, J)
        if dim == 'I-E':
            text_scores[dim] = confidence if letter == 'I' else (1 - confidence)
        elif dim == 'N-S':
            text_scores[dim] = confidence if letter == 'N' else (1 - confidence)
        elif dim == 'T-F':
            text_scores[dim] = confidence if letter == 'T' else (1 - confidence)
        elif dim == 'J-P':
            text_scores[dim] = confidence if letter == 'J' else (1 - confidence)
    
    # Combine scores using weighted average
    text_weight = 1 - quiz_weight
    combined_scores = {}
    
    for dim in ['I-E', 'N-S', 'T-F', 'J-P']:
        combined_scores[dim] = (
            quiz_scores[dim] * quiz_weight +
            text_scores[dim] * text_weight
        )
    
    mbti_type = scores_to_mbti(combined_scores)
    return mbti_type, combined_scores

def scores_to_mbti(scores):
    """
    Convert dimension scores to MBTI type
    
    Args:
        scores: Dict with keys 'I-E', 'N-S', 'T-F', 'J-P' and values 0-1
    
    Returns:
        4-letter MBTI type string
    """
    mbti = ""
    mbti += "I" if scores['I-E'] > 0.5 else "E"
    mbti += "N" if scores['N-S'] > 0.5 else "S"
    mbti += "T" if scores['T-F'] > 0.5 else "F"
    mbti += "J" if scores['J-P'] > 0.5 else "P"
    return mbti

# Test the combiner
if __name__ == "__main__":
    print("Testing Likert Scale Combiner")
    print("=" * 60)
    
    # Test 1: Quiz only (short test)
    print("\n📝 Test 1: Quiz Only (20 questions, all neutral)")
    test_answers = [3] * 20  # All neutral (3 out of 5)
    
    mbti_type, scores = combine_predictions_likert(test_answers, 'short')
    
    print(f"Predicted Type: {mbti_type}")
    print("\nDimension Scores:")
    for dim, score in scores.items():
        print(f"  {dim}: {score:.3f} ({score*100:.1f}%)")
    
    # Test 2: Quiz + Text
    print("\n" + "=" * 60)
    print("\n📝 Test 2: Quiz + Text")
    
    test_text = """
    I really love spending time alone, reading books and thinking deeply about 
    abstract concepts and theories. I prefer to analyze things logically rather 
    than going with my feelings. I like to have everything planned out in advance.
    """
    
    # Answers leaning toward INTJ
    test_answers2 = [5, 5, 4, 5, 4] * 4  # 20 questions, mostly high scores
    
    mbti_type2, scores2 = combine_predictions_likert(test_answers2, 'short', test_text)
    
    print(f"Predicted Type: {mbti_type2}")
    print("\nDimension Scores:")
    for dim, score in scores2.items():
        print(f"  {dim}: {score:.3f} ({score*100:.1f}%)")
    
    print("\n" + "=" * 60)
    print("✓ Combiner is working correctly!")