# 🧠 EchoType

**Discover your MBTI personality through AI-powered analysis**

EchoType combines traditional questionnaires with natural language processing to provide accurate personality assessments.

---

## ✨ Features

- 🎯 **Dual Assessment**: Choose between Quick (20 questions) or Full (60 questions) test
- 📊 **5-Point Likert Scale**: Nuanced responses for better accuracy
- 🤖 **AI Text Analysis**: Optional text input analyzed by machine learning
- 🎨 **Beautiful UI**: Modern, responsive design with smooth animations
- 📈 **Confidence Scores**: See how confident the system is in each dimension

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/EchoType.git
cd EchoType
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Download NLTK data**
```python
python -c "import nltk; nltk.download('stopwords')"
```

4. **Get the MBTI dataset**
- Download `mbti_1.csv` from [Kaggle MBTI Dataset](https://www.kaggle.com/datasnaek/mbti-type)
- Place it in the project root directory

5. **Train the models**
```bash
python data.py
```
This will create the `.pkl` model files (takes ~2-5 minutes)

6. **Run the application**
```bash
python app.py
```

7. **Open your browser**
Navigate to `http://localhost:5000`

---

## 🧪 Testing

### Test the predictor
```bash
python predict.py
```

### Test the scorer
```bash
python quiz_scorer.py
```

### Test the combiner
```bash
python combiner.py
```

### Terminal interface
```bash
python terminal_test.py
```

---

## 📊 How It Works

### 1. **Questionnaire Analysis**
- Users answer 20 (short) or 60 (full) questions on a 5-point scale
- Questions are scientifically designed to assess the 4 MBTI dimensions:
  - **I-E**: Introversion ↔ Extraversion
  - **N-S**: Intuition ↔ Sensing
  - **T-F**: Thinking ↔ Feeling
  - **J-P**: Judging ↔ Perceiving

### 2. **Text Analysis (Optional)**
- Users can write freely about themselves
- NLP model trained on 8,675+ personality-labeled writing samples
- TF-IDF vectorization + Logistic Regression classifiers
- Average accuracy: **84.3%**

### 3. **Intelligent Combination**
- Quiz responses weighted at 70%
- Text analysis weighted at 30%
- Final prediction combines both for optimal accuracy

---

## 📁 Project Structure
```
EchoType/
├── data.py              # Model training
├── predict.py           # Text-based prediction
├── quiz_scorer.py       # Quiz scoring logic
├── combiner.py          # Combines quiz + text
├── app.py               # Flask web server
├── questions.json       # MBTI questions
├── templates/           # HTML templates
├── static/              # CSS & JavaScript
└── terminal_test.py     # CLI testing
```

---

## 🎨 Technologies

- **Backend**: Python, Flask, scikit-learn, NLTK
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **ML**: TF-IDF, Logistic Regression
- **Design**: Glassmorphism, CSS animations

---

## 📈 Model Performance

| Dimension | Accuracy | Notes |
|-----------|----------|-------|
| I-E | 83.9% | Introversion vs Extraversion |
| N-S | 88.1% | Intuition vs Sensing (best) |
| T-F | 84.3% | Thinking vs Feeling |
| J-P | 80.8% | Judging vs Perceiving |
| **Average** | **84.3%** | |

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👨‍💻 Author

**Leonel Sebastian**

Built with 🧠 and ☕

---

## 🙏 Acknowledgments

- MBTI dataset from Kaggle
- Inspired by Myers-Briggs Type Indicator
- Built as a learning project in personality psychology and machine learning

---

## ⚠️ Disclaimer

This tool is for entertainment and self-discovery purposes only. It should not be used for:
- Clinical diagnosis
- Employment decisions
- Professional psychological assessment

For accurate personality assessment, consult a qualified psychologist.