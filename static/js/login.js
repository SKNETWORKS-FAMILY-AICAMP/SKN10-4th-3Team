// Password toggle functionality
function setupPasswordToggle(toggleId, inputId) {
    const toggle = document.getElementById(toggleId);
    const input = document.getElementById(inputId);
    
    if (toggle && input) {
        toggle.addEventListener('click', () => {
            const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
            input.setAttribute('type', type);
            toggle.querySelector('i').classList.toggle('fa-eye');
            toggle.querySelector('i').classList.toggle('fa-eye-slash');
        });
    }
}

// Form validation
function validateForm(formId, validationRules) {
    const form = document.getElementById(formId);
    if (!form) return false;

    let isValid = true;
    const errors = {};

    // Clear previous errors
    document.querySelectorAll('.error-message').forEach(el => {
        el.classList.add('hidden');
        el.textContent = '';
    });
    document.querySelectorAll('.border-red-500').forEach(el => {
        el.classList.remove('border-red-500');
    });

    // Validate each field
    for (const [fieldId, rules] of Object.entries(validationRules)) {
        const field = document.getElementById(fieldId);
        if (!field) continue;

        const value = field.value.trim();
        const errorElement = document.getElementById(`${fieldId}Error`);

        // Required check
        if (rules.required && !value) {
            errors[fieldId] = 'This field is required';
            field.classList.add('border-red-500');
            if (errorElement) {
                errorElement.textContent = errors[fieldId];
                errorElement.classList.remove('hidden');
            }
            isValid = false;
            continue;
        }

        // Pattern check
        if (rules.pattern && value && !rules.pattern.test(value)) {
            errors[fieldId] = rules.message || 'Invalid format';
            field.classList.add('border-red-500');
            if (errorElement) {
                errorElement.textContent = errors[fieldId];
                errorElement.classList.remove('hidden');
            }
            isValid = false;
        }
    }

    return isValid;
}

// Initialize form validation
document.addEventListener('DOMContentLoaded', () => {
    // Setup password toggle
    setupPasswordToggle('loginPasswordToggle', 'loginPassword');

    // Setup form validation
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const isValid = validateForm('loginForm', {
                loginCredential: {
                    required: true,
                    pattern: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$|^[a-zA-Z0-9_]{3,20}$/,
                    message: 'Please enter a valid email or username'
                },
                loginPassword: {
                    required: true,
                    pattern: /^.{8,}$/,
                    message: 'Password must be at least 8 characters long'
                }
            });

            if (isValid) {
                // Submit form
                loginForm.submit();
            }
        });
    }
}); 