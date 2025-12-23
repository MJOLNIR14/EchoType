// Global variables
let questions = {};
let currentDimension = '';
let currentQuestionIndex = 0;
let answers = {
    'I-E': [],
    'N-S': [],
    'T-F': [],
    'J-P': []
};
const dimensionOrder = ['I-E', 'N-S', 'T-F', 'J-P'];
let totalQuestions = 0;

// Load questions from backend
async function loadQuestions() {
    try {
        const response = await fetch('/api/questions');
        questions = await response.json();
        
        // Calculate total questions
        totalQuestions = Object.values(questions).reduce((sum, qs) => sum + qs.length, 0);
        document.getElementById('total-q').textContent = totalQuestions;
    } catch (error) {
        console.error('Error loading questions:', error);
        alert('Failed to load questions. Please refresh the page.');
    }
}

// Start the quiz
function startQuiz() {
    document.getElementById('welcome-screen').classList.remove('active');
    document.getElementById('quiz-screen').classList.add('active');
    
    currentDimension = dimensionOrder[0];
    currentQuestionIndex = 0;
    
    displayQuestion();
}

// Display current question
function displayQuestion() {
    const container = document.getElementById('question-container');
    const dimQuestions = questions[currentDimension];
    const question = dimQuestions[currentQuestionIndex];
    
    // Update progress
    const totalAnswered = answers['I-E'].length + answers['N-S'].length + 
                         answers['T-F'].length + answers['J-P'].length;
    const progress = (totalAnswered / totalQuestions) * 100;
    document.getElementById('progress').style.width = progress + '%';
    document.getElementById('current-q').textContent = totalAnswered + 1;
    
    // Display question
    container.innerHTML = `
        <div class="question">
            <h3>${question.question}</h3>
            <div class="options">
                <div class="option" onclick="selectOption('A')">
                    A) ${question.options.A}
                </div>
                <div class="option" onclick="selectOption('B')">
                    B) ${question.options.B}
                </div>
            </div>
        </div>
    `;
    
    // Show/hide buttons
    document.getElementById('prev-btn').style.display = totalAnswered > 0 ? 'block' : 'none';
}

// Select an option
function selectOption(choice) {
    // Save answer
    answers[currentDimension][currentQuestionIndex] = choice;
    
    // Highlight selected
    document.querySelectorAll('.option').forEach(opt => opt.classList.remove('selected'));
    event.target.classList.add('selected');
    
    // Auto advance after short delay
    setTimeout(() => {
        nextQuestion();
    }, 300);
}

// Next question
function nextQuestion() {
    const dimQuestions = questions[currentDimension];
    
    // Check if current dimension is complete
    if (currentQuestionIndex < dimQuestions.length - 1) {
        currentQuestionIndex++;
        displayQuestion();
    } else {
        // Move to next dimension
        const currentDimIndex = dimensionOrder.indexOf(currentDimension);
        
        if (currentDimIndex < dimensionOrder.length - 1) {
            currentDimension = dimensionOrder[currentDimIndex + 1];
            currentQuestionIndex = 0;
            displayQuestion();
        } else {
            // All questions done, show text section
            showTextSection();
        }
    }
}

// Previous question
function previousQuestion() {
    if (currentQuestionIndex > 0) {
        currentQuestionIndex--;
        displayQuestion();
    } else {
        // Go to previous dimension
        const currentDimIndex = dimensionOrder.indexOf(currentDimension);
        if (currentDimIndex > 0) {
            currentDimension = dimensionOrder[currentDimIndex - 1];
            const dimQuestions = questions[currentDimension];
            currentQuestionIndex = dimQuestions.length - 1;
            displayQuestion();
        }
    }
}

// Show text input section
function showTextSection() {
    document.getElementById('question-container').style.display = 'none';
    document.getElementById('text-section').style.display = 'block';
    document.getElementById('next-btn').textContent = 'Get My Results';
    document.getElementById('next-btn').onclick = submitQuiz;
    document.getElementById('prev-btn').style.display = 'block';
    
    // Update progress to 100%
    document.getElementById('progress').style.width = '100%';
}

// Submit quiz
async function submitQuiz() {
    const userText = document.getElementById('user-text').value;
    
    // Show loading
    document.getElementById('next-btn').textContent = 'Analyzing...';
    document.getElementById('next-btn').disabled = true;
    
    try {
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                quiz_answers: answers,
                text: userText
            })
        });
        
        const result = await response.json();
        showResults(result);
    } catch (error) {
        console.error('Error:', error);
        alert('Something went wrong. Please try again.');
        document.getElementById('next-btn').textContent = 'Get My Results';
        document.getElementById('next-btn').disabled = false;
    }
}

// Show results
function showResults(result) {
    document.getElementById('quiz-screen').classList.remove('active');
    document.getElementById('results-screen').classList.add('active');
    
    // Display type
    document.getElementById('mbti-type').textContent = result.type;
    document.getElementById('type-description').textContent = result.description;
    
    // Display dimension scores
    const dimensionNames = {
        'I-E': 'Introversion vs Extraversion',
        'N-S': 'Intuition vs Sensing',
        'T-F': 'Thinking vs Feeling',
        'J-P': 'Judging vs Perceiving'
    };
    
    const scoresContainer = document.getElementById('dimension-scores');
    scoresContainer.innerHTML = '';
    
    for (const [dim, score] of Object.entries(result.scores)) {
        const percentage = (score * 100).toFixed(1);
        
        scoresContainer.innerHTML += `
            <div class="dimension">
                <div class="dimension-label">
                    <span>${dimensionNames[dim]}</span>
                    <span>${percentage}%</span>
                </div>
                <div class="dimension-bar">
                    <div class="dimension-fill" style="width: ${percentage}%"></div>
                </div>
            </div>
        `;
    }
}

// Reset quiz
function resetQuiz() {
    answers = {
        'I-E': [],
        'N-S': [],
        'T-F': [],
        'J-P': []
    };
    
    document.getElementById('results-screen').classList.remove('active');
    document.getElementById('welcome-screen').classList.add('active');
    
    // Reset button
    document.getElementById('next-btn').textContent = 'Next';
    document.getElementById('next-btn').onclick = nextQuestion;
    document.getElementById('next-btn').disabled = false;
}

// Load questions when page loads
loadQuestions();