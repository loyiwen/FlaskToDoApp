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
