const form = document.getElementById('predictionForm');
const resultCard = document.getElementById('resultCard');
const predictedCategory = document.getElementById('predictedCategory');
const estimatedStress = document.getElementById('estimatedStress');
const confidenceScore = document.getElementById('confidenceScore');
const stressToggle = document.getElementById('stressToggle');
const stressInputContainer = document.getElementById('stressInputContainer');
const stressValueDisplay = document.getElementById('stressValue');
const stressSlider = document.querySelector('.stress-slider');

// Update stress input visibility based on toggle
function updateStressField() {
  if (stressToggle.checked) {
    stressInputContainer.style.display = 'block';
    stressSlider.required = true;
  } else {
    stressInputContainer.style.display = 'none';
    stressSlider.required = false;
  }
}

// Update stress value display as slider moves
function updateStressValue() {
  stressValueDisplay.textContent = stressSlider.value;
}

stressToggle.addEventListener('change', updateStressField);
stressSlider.addEventListener('input', updateStressValue);
updateStressField();

function formatConfidence(score) {
  if (score >= 0.80) return 'High';
  if (score >= 0.65) return 'Medium';
  return 'Low';
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  resultCard.querySelector('.result-status').textContent = 'Predicting…';

  const data = new FormData(form);
  const payload = {
    heart_rate_BPM: Number(data.get('heart_rate_BPM')),
    blood_oxygen_level: Number(data.get('blood_oxygen_level')),
    step_count: Number(data.get('step_count')),
    sleep_duration_hr: Number(data.get('sleep_duration_hr')),
    activity_level: data.get('activity_level'),
    health_score: Number(data.get('health_score')),
    model: stressToggle.checked ? 'health' : 'stress',
  };

  // Include stress level if toggle is checked
  if (stressToggle.checked && stressSlider.value) {
    payload.stress_level = Number(stressSlider.value);
  }

  const endpoint = window.location.protocol === 'file:'
    ? 'http://127.0.0.1:5000/predict'
    : `${window.location.origin}/predict`;

  if (window.location.protocol === 'file:') {
    resultCard.querySelector('.result-status').textContent = 'Error: Open the app through the Flask server at http://127.0.0.1:5000, not as a local file.';
    return;
  }

  try {
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Prediction failed');
    }

    const result = await response.json();
    
    resultCard.innerHTML = `
      <div class="result-details">
        <p><strong>Category:</strong> <span>${result.health_category}</span></p>
        <p><strong>Stress Level:</strong> <span>${result.stress_level}</span> (${result.stress_source})</p>
        <p><strong>Confidence:</strong> <span>${formatConfidence(result.health_confidence)}</span></p>
      </div>
    `;
  } catch (error) {
    resultCard.querySelector('.result-status').textContent = `Error: ${error.message}`;
  }
});
