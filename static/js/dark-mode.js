// ============================================
// Dark Mode Toggle
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    const darkModeToggle = document.getElementById('darkModeToggle');
    
    if (!darkModeToggle) return;

    // Load dark mode preference from localStorage
    const isDarkMode = localStorage.getItem('darkMode') === 'true';
    if (isDarkMode) {
        enableDarkMode();
    }

    // Toggle dark mode on button click
    darkModeToggle.addEventListener('click', toggleDarkMode);
});

/**
 * Toggle dark mode
 */
function toggleDarkMode() {
    if (document.body.classList.contains('dark-mode')) {
        disableDarkMode();
    } else {
        enableDarkMode();
    }
}

/**
 * Enable dark mode
 */
function enableDarkMode() {
    document.body.classList.add('dark-mode');
    localStorage.setItem('darkMode', 'true');
    updateDarkModeButton();
}

/**
 * Disable dark mode
 */
function disableDarkMode() {
    document.body.classList.remove('dark-mode');
    localStorage.setItem('darkMode', 'false');
    updateDarkModeButton();
}

/**
 * Update dark mode button icon
 */
function updateDarkModeButton() {
    const button = document.getElementById('darkModeToggle');
    if (!button) return;

    const isDarkMode = document.body.classList.contains('dark-mode');
    button.innerHTML = isDarkMode 
        ? '<i class="fas fa-sun"></i>' 
        : '<i class="fas fa-moon"></i>';
}