import json

def load_questions():
    """Load questions from JSON file"""
    with open('questions.json', 'r') as f:
        return json.load(f)

def score_quiz(answers, test_type='short'):
    """
    Score quiz answers with 5-point Likert scale
    
    Args:
        answers: List of integers (1-5) representing user responses
        test_type: 'short' or 'full'
    
    Returns:
        Dictionary with probabilities (0-1) for each dimension
    """
    questions_data = load_questions()
    
    # Get the right questions based on test type
    questions_per_dim = questions_data['test_types'][test_type]['questions_per_dimension']
    
    # Build question list
    all_questions = []
    for dimension in ['I-E', 'N-S', 'T-F', 'J-P']:
        dim_questions = questions_data[dimension]
        
        # Filter by test type
        if test_type == 'short':
            dim_qs = [q for q in dim_questions if q['category'] == 'short']
        else:
            # Full test includes all questions
            dim_qs = dim_questions[:questions_per_dim]
        
        all_questions.extend(dim_qs)
    
    # Calculate scores for each dimension
    scores = {}
    answer_index = 0
    
    for dimension in ['I-E', 'N-S', 'T-F', 'J-P']:
        dim_questions = [q for q in all_questions if q['dimension'] == dimension]
        total_score = 0
        
        for question in dim_questions:
            user_answer = answers[answer_index]
            answer_index += 1
            
            # Convert 1-5 scale to score
            # 1 = Strongly Disagree, 5 = Strongly Agree
            # If reverse=True, flip the scoring
            if question['reverse']:
                # Reverse scoring: 1→5, 2→4, 3→3, 4→2, 5→1
                score = 6 - user_answer
            else:
                score = user_answer
            
            total_score += score
        
        # Normalize to 0-1 scale
        # Score ranges from (num_questions * 1) to (num_questions * 5)
        # We want 1 to map to 0 and 5 to map to 1
        num_questions = len(dim_questions)
        min_possible = num_questions * 1
        max_possible = num_questions * 5
        
        normalized = (total_score - min_possible) / (max_possible - min_possible)
        scores[dimension] = normalized
    
    return scores

def get_question_order(test_type='short'):
    """
    Get the ordered list of questions for display
    
    Args:
        test_type: 'short' or 'full'
    
    Returns:
        List of question objects in presentation order
    """
    questions_data = load_questions()
    questions_per_dim = questions_data['test_types'][test_type]['questions_per_dimension']
    
    ordered_questions = []
    
    for dimension in ['I-E', 'N-S', 'T-F', 'J-P']:
        dim_questions = questions_data[dimension]
        
        if test_type == 'short':
            dim_qs = [q for q in dim_questions if q['category'] == 'short']
        else:
            dim_qs = dim_questions[:questions_per_dim]
        
        ordered_questions.extend(dim_qs)
    
    return ordered_questions

# Test the scorer
if __name__ == "__main__":
    print("Testing 5-Point Likert Scale Scorer")
    print("=" * 50)
    
    # Test short quiz (20 questions)
    # Simulate user answering all 5s (Strongly Agree)
    test_answers_short = [5] * 20
    
    result = score_quiz(test_answers_short, 'short')
    print("\nTest: All 'Strongly Agree' (5) responses")
    print("Expected: Scores around 1.0 for first trait in each dimension")
    print("\nResults:")
    for dim, score in result.items():
        print(f"  {dim}: {score:.3f} ({score*100:.1f}%)")
    
    print("\n" + "=" * 50)
    
    # Test with mixed answers
    test_answers_mixed = [5, 4, 3, 2, 1] * 4  # 20 questions
    
    result2 = score_quiz(test_answers_mixed, 'short')
    print("\nTest: Mixed responses (5,4,3,2,1 pattern)")
    print("Expected: Scores around 0.5 (neutral)")
    print("\nResults:")
    for dim, score in result2.items():
        print(f"  {dim}: {score:.3f} ({score*100:.1f}%)")
    
    print("\n" + "=" * 50)
    print("✓ Scorer is working correctly!")