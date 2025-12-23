from combiner import combine_predictions_likert

def run_terminal_test():
    print("=" * 50)
    print("  ECHOTYPE - MBTI Personality Test")
    print("=" * 50)
    print("\nAnswer each question on a scale of 1-5")
    print("1 = Strongly Disagree")
    print("2 = Disagree")
    print("3 = Neutral")
    print("4 = Agree")
    print("5 = Strongly Agree\n")
    
    # Simple questions for terminal (20 total)
    questions = [
        # I-E Questions (5)
        "I feel energized after spending time with large groups of people",
        "I prefer deep one-on-one conversations over group discussions",
        "I often need time alone to recharge after social events",
        "I enjoy being the center of attention at parties",
        "I think out loud and process ideas by talking to others",
        
        # N-S Questions (5)
        "I focus more on possibilities and future potential than present reality",
        "I prefer concrete facts and data over abstract theories",
        "I often get lost in imaginative thoughts and daydreams",
        "I trust my intuition and gut feelings when making decisions",
        "I prefer practical, hands-on learning over theoretical concepts",
        
        # T-F Questions (5)
        "I make decisions based primarily on logic and objective analysis",
        "I consider how decisions will affect people's feelings",
        "I value truth and accuracy over maintaining harmony",
        "I'm naturally empathetic and attuned to others' emotions",
        "I prefer to remain emotionally detached when solving problems",
        
        # J-P Questions (5)
        "I prefer to have a structured plan before starting any project",
        "I enjoy keeping my options open and adapting as I go",
        "I feel stressed when things are unorganized or unplanned",
        "I thrive in spontaneous, unpredictable situations",
        "I prefer to complete tasks well before deadlines"
    ]
    
    answers = []
    
    for i, question in enumerate(questions, 1):
        print(f"\n{i}. {question}")
        while True:
            try:
                answer = input("Your answer (1-5): ").strip()
                answer_int = int(answer)
                if 1 <= answer_int <= 5:
                    answers.append(answer_int)
                    break
                else:
                    print("Please enter a number between 1 and 5")
            except ValueError:
                print("Please enter a valid number (1-5)")
    
    # Optional text
    print("\n" + "=" * 50)
    print("OPTIONAL: Tell us more about yourself")
    print("(Press Enter to skip, or write at least 50 characters)")
    print("=" * 50)
    text = input("\nYour thoughts: ").strip()
    
    # Get prediction
    print("\n🔮 Analyzing your personality...")
    mbti_type, scores = combine_predictions_likert(
        answers=answers,
        test_type='short',
        text=text if len(text) >= 50 else None
    )
    
    # Display results
    print("\n" + "=" * 50)
    print("  YOUR PERSONALITY TYPE")
    print("=" * 50)
    print(f"\n🎯 {mbti_type}\n")
    
    print("Confidence Breakdown:")
    for dim, score in scores.items():
        bar_length = int(score * 30)
        bar = "█" * bar_length + "░" * (30 - bar_length)
        
        # Show which trait is dominant
        if dim == 'I-E':
            trait = "I (Introvert)" if score > 0.5 else "E (Extravert)"
        elif dim == 'N-S':
            trait = "N (Intuitive)" if score > 0.5 else "S (Sensing)"
        elif dim == 'T-F':
            trait = "T (Thinking)" if score > 0.5 else "F (Feeling)"
        elif dim == 'J-P':
            trait = "J (Judging)" if score > 0.5 else "P (Perceiving)"
        
        print(f"  {dim} ({trait}): {bar} {score*100:.1f}%")
    
    # Type descriptions
    descriptions = {
        'INTJ': 'The Architect - Strategic, independent, analytical',
        'INTP': 'The Logician - Innovative, curious, philosophical',
        'ENTJ': 'The Commander - Bold, decisive, natural leader',
        'ENTP': 'The Debater - Quick-witted, clever, innovative',
        'INFJ': 'The Advocate - Idealistic, organized, insightful',
        'INFP': 'The Mediator - Empathetic, creative, idealistic',
        'ENFJ': 'The Protagonist - Charismatic, inspiring, altruistic',
        'ENFP': 'The Campaigner - Enthusiastic, creative, sociable',
        'ISTJ': 'The Logistician - Practical, fact-minded, reliable',
        'ISFJ': 'The Defender - Dedicated, warm, protective',
        'ESTJ': 'The Executive - Organized, practical, traditional',
        'ESFJ': 'The Consul - Caring, social, popular',
        'ISTP': 'The Virtuoso - Bold, practical, experimental',
        'ISFP': 'The Adventurer - Flexible, charming, artistic',
        'ESTP': 'The Entrepreneur - Energetic, perceptive, direct',
        'ESFP': 'The Entertainer - Spontaneous, energetic, enthusiastic'
    }
    
    print(f"\n{descriptions.get(mbti_type, 'Unique personality!')}")
    print("\n" + "=" * 50)

if __name__ == "__main__":
    run_terminal_test()