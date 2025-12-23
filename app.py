from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from combiner import combine_predictions_likert
from quiz_scorer import get_question_order
import json

app = Flask(__name__)
CORS(app)

# Personality type descriptions
TYPE_DESCRIPTIONS = {
    'INTJ': 'The Architect - Strategic, independent, and highly analytical. You see patterns others miss and plan for the future.',
    'INTP': 'The Logician - Innovative, curious, and philosophical. You love exploring abstract theories and solving complex problems.',
    'ENTJ': 'The Commander - Bold, decisive, and natural-born leaders. You excel at organizing people and resources efficiently.',
    'ENTP': 'The Debater - Quick-witted, clever, and innovative. You enjoy intellectual challenges and thinking outside the box.',
    'INFJ': 'The Advocate - Idealistic, organized, and insightful. You understand people deeply and work toward meaningful change.',
    'INFP': 'The Mediator - Empathetic, creative, and idealistic. You follow your values and seek authenticity in all you do.',
    'ENFJ': 'The Protagonist - Charismatic, inspiring, and altruistic. You naturally bring out the best in others.',
    'ENFP': 'The Campaigner - Enthusiastic, creative, and sociable. You see life as full of possibilities and connections.',
    'ISTJ': 'The Logistician - Practical, fact-minded, and reliable. You value tradition, order, and getting things done right.',
    'ISFJ': 'The Defender - Dedicated, warm, and protective. You care deeply about others and maintain harmony.',
    'ESTJ': 'The Executive - Organized, practical, and traditional. You excel at managing tasks and leading with clear standards.',
    'ESFJ': 'The Consul - Caring, social, and popular. You create warm, welcoming environments and help others feel valued.',
    'ISTP': 'The Virtuoso - Bold, practical, and experimental. You master tools and techniques through hands-on experience.',
    'ISFP': 'The Adventurer - Flexible, charming, and artistic. You live in the moment and appreciate beauty in all forms.',
    'ESTP': 'The Entrepreneur - Energetic, perceptive, and direct. You thrive on action and adapt quickly to any situation.',
    'ESFP': 'The Entertainer - Spontaneous, energetic, and enthusiastic. You bring excitement and joy wherever you go.'
}

@app.route('/')
def home():
    """Serve the main web interface"""
    return render_template('index.html')

@app.route('/api/questions/<test_type>', methods=['GET'])
def get_questions(test_type):
    """
    Return questions for the specified test type
    
    Args:
        test_type: 'short' or 'full'
    
    Returns:
        JSON list of questions in order
    """
    try:
        if test_type not in ['short', 'full']:
            return jsonify({'error': 'Invalid test type. Use "short" or "full"'}), 400
        
        questions = get_question_order(test_type)
        
        # Return questions with necessary info
        return jsonify({
            'test_type': test_type,
            'total_questions': len(questions),
            'questions': questions
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Accepts quiz answers (1-5 scale) and optional text
    Returns MBTI prediction with confidence scores
    
    Expected JSON format:
    {
        "answers": [5, 4, 3, 5, 4, ...],  // List of 1-5 responses
        "test_type": "short" or "full",
        "text": "Optional user text..."
    }
    """
    try:
        data = request.json
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        answers = data.get('answers')
        test_type = data.get('test_type', 'short')
        text = data.get('text', '')
        
        if not answers:
            return jsonify({'error': 'Answers required'}), 400
        
        if not isinstance(answers, list):
            return jsonify({'error': 'Answers must be a list'}), 400
        
        # Validate answer values
        if not all(isinstance(a, int) and 1 <= a <= 5 for a in answers):
            return jsonify({'error': 'All answers must be integers between 1 and 5'}), 400
        
        # Get prediction using the updated function
        mbti_type, scores = combine_predictions_likert(
            answers=answers,
            test_type=test_type,
            text=text if text and len(text.strip()) >= 50 else None
        )
        
        # Return results
        return jsonify({
            'success': True,
            'type': mbti_type,
            'description': TYPE_DESCRIPTIONS.get(mbti_type, 'A unique personality type!'),
            'scores': {dim: float(score) for dim, score in scores.items()},
            'dimensions': {
                'I-E': {
                    'name': 'Introversion ↔ Extraversion',
                    'score': float(scores['I-E']),
                    'trait': 'I' if scores['I-E'] > 0.5 else 'E'
                },
                'N-S': {
                    'name': 'Intuition ↔ Sensing',
                    'score': float(scores['N-S']),
                    'trait': 'N' if scores['N-S'] > 0.5 else 'S'
                },
                'T-F': {
                    'name': 'Thinking ↔ Feeling',
                    'score': float(scores['T-F']),
                    'trait': 'T' if scores['T-F'] > 0.5 else 'F'
                },
                'J-P': {
                    'name': 'Judging ↔ Perceiving',
                    'score': float(scores['J-P']),
                    'trait': 'J' if scores['J-P'] > 0.5 else 'P'
                }
            }
        })
    
    except Exception as e:
        print(f"Error in prediction: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Prediction failed: {str(e)}'
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'EchoType API',
        'version': '1.0'
    })

if __name__ == '__main__':
    print("=" * 60)
    print("  ECHOTYPE SERVER STARTING")
    print("=" * 60)
    print("\n🚀 Server running at: http://localhost:5000")
    print("📊 API endpoints available:")
    print("   - GET  /api/questions/<test_type>")
    print("   - POST /api/predict")
    print("   - GET  /api/health")
    print("\n💡 Open http://localhost:5000 in your browser")
    print("=" * 60 + "\n")
    
    app.run(debug=True, port=5000)