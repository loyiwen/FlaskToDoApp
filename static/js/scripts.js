// scripts.js
function toggleCheckbox(iconElement, assessmentId) {
    // Toggle the icon between checked and unchecked
    if (iconElement.textContent === 'check_box') {
        iconElement.textContent = 'check_box_outline_blank'; // Unchecked state
    } else {
        iconElement.textContent = 'check_box'; // Checked state
    }

    // Submit the form to toggle the completion state in the backend
    document.getElementById(`completion-form-${assessmentId}`).submit();
}

setTimeout(function() {
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(message => {
        message.style.transition = 'opacity 1s';
        message.style.opacity = '0';
        
        // Remove the message from the DOM after fading out
        setTimeout(() => message.remove(), 1000);
    });
}, 3000);
