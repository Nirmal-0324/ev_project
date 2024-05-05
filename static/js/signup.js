document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const passwordInput = document.querySelector('input[name="psw"]');
    const confirmPasswordInput = document.querySelector('input[name="psw-confirm"]');
    const errorMessage = document.querySelector('.error-message');

    form.addEventListener('submit', function(event) {
        if (passwordInput.value !== confirmPasswordInput.value) {
            errorMessage.innerHTML = "Passwords do not match";
            errorMessage.style.display = 'block';
            event.preventDefault(); // Prevent form submission
        } else {
            errorMessage.style.display = 'none';
        }
    });
});

function validateForm() {
    const username = document.querySelector('input[type="text"]').value;
    const password = document.querySelector('input[type="password"]').value;
    const errorMessages = document.querySelectorAll('.error-message');

    if (username === '' || password === '') {
        errorMessages[0].innerHTML = "Please enter both username and password";
        return false;
    }

    return true;
}
