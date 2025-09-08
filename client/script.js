const form = document.getElementById('predictionForm');
const submitBtn = document.getElementById('submitBtn');
const loading = document.getElementById('loading');
const result = document.getElementById('result');

// Validation rules
const validationRules = {
    iq: { min: 70, max: 160 },
    prev_sem_result: { min: 5.0, max: 10.0 },
    cgpa: { min: 5.0, max: 10.0 },
    academic_performance: { min: 1, max: 10 },
    extra_curricular_score: { min: 0, max: 10 },
    communication_skills: { min: 1, max: 10 },
    projects_completed: { min: 0, max: 5 },
};

// Real-time validation
Object.keys(validationRules).forEach((fieldName) => {
    const field = document.getElementById(fieldName);
    const errorDiv = document.getElementById(fieldName + '-error');

    field.addEventListener('input', () => {
        validateField(fieldName, field, errorDiv);
    });

    field.addEventListener('blur', () => {
        validateField(fieldName, field, errorDiv);
    });
});

// Validate internship experience dropdown
const internshipField = document.getElementById('internship_experience_yes');
const internshipError = document.getElementById('internship_experience_yes-error');

internshipField.addEventListener('change', () => {
    if (internshipField.value === '') {
        showError(internshipField, internshipError, 'Please select your internship experience');
    } else {
        showSuccess(internshipField, internshipError);
    }
});

function validateField(fieldName, field, errorDiv) {
    const value = parseFloat(field.value);
    const rules = validationRules[fieldName];

    if (field.value === '') {
        showError(field, errorDiv, 'This field is required');
        return false;
    }

    if (isNaN(value)) {
        showError(field, errorDiv, 'Please enter a valid number');
        return false;
    }

    if (value < rules.min || value > rules.max) {
        showError(field, errorDiv, `Value must be between ${rules.min} and ${rules.max}`);
        return false;
    }

    showSuccess(field, errorDiv);
    return true;
}

function showError(field, errorDiv, message) {
    field.classList.remove('success');
    field.classList.add('error');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
}

function showSuccess(field, errorDiv) {
    field.classList.remove('error');
    field.classList.add('success');
    errorDiv.style.display = 'none';
}

function validateForm() {
    let isValid = true;

    // Validate all numeric fields
    Object.keys(validationRules).forEach((fieldName) => {
        const field = document.getElementById(fieldName);
        const errorDiv = document.getElementById(fieldName + '-error');
        if (!validateField(fieldName, field, errorDiv)) {
            isValid = false;
        }
    });

    // Validate internship experience
    if (internshipField.value === '') {
        showError(internshipField, internshipError, 'Please select your internship experience');
        isValid = false;
    }

    return isValid;
}

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    if (!validateForm()) {
        showResult('Please correct the errors above', 'error');
        return;
    }

    // Show loading state
    submitBtn.disabled = true;
    loading.style.display = 'block';
    result.style.display = 'none';

    const formData = new FormData(form);
    const data = {};

    // Convert form data to numbers
    for (let [key, value] of formData.entries()) {
        data[key] = key === 'internship_experience_yes' ? parseInt(value) : parseFloat(value);
    }

    try {
        const response = await fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const resultData = await response.json();

        if (resultData.error) {
            showResult(`Error: ${resultData.error}`, 'error');
        } else {
            const isSelected = resultData.prediction === 1;
            const message = isSelected
                ? '🎉 Congratulations! You are likely to be selected for the internship!'
                : '😔 Based on the analysis, you might not be selected for the internship. Consider improving your skills!';

            showResult(message, isSelected ? 'success' : 'failure');
        }
    } catch (error) {
        console.error('Error:', error);
        showResult('Network error. Please check if the server is running and try again.', 'error');
    } finally {
        // Hide loading state
        submitBtn.disabled = false;
        loading.style.display = 'none';
    }
});

function showResult(message, type) {
    result.textContent = message;
    result.className = `result ${type}`;
    result.style.display = 'block';
    result.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Form reset functionality
function resetForm() {
    form.reset();
    result.style.display = 'none';

    // Reset all field states
    const fields = form.querySelectorAll('input, select');
    fields.forEach((field) => {
        field.classList.remove('error', 'success');
    });

    const errorMessages = form.querySelectorAll('.error-message');
    errorMessages.forEach((error) => {
        error.style.display = 'none';
    });
}

// Add reset button functionality (optional)
const resetBtn = document.createElement('button');
resetBtn.textContent = 'Reset Form';
resetBtn.type = 'button';
resetBtn.className = 'submit-btn';
resetBtn.style.background = '#6c757d';
resetBtn.style.marginTop = '10px';
resetBtn.addEventListener('click', resetForm);

// Uncomment the line below if you want to add a reset button
// form.appendChild(resetBtn);
