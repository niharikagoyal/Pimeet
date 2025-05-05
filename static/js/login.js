// Automatically hide flash messages after 5 seconds
document.addEventListener('DOMContentLoaded', () => {
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.display = 'none';
        }, 5000); // 5 seconds
    });

    // Theme Toggle Logic
    const themeToggle = document.getElementById('themeToggle');
    const themeIcon = themeToggle.querySelector('i'); // Select the <i> element inside the button

    // Check for saved theme in localStorage
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'light') {
        document.body.classList.add('light-mode');
        themeIcon.classList.replace('fa-moon', 'fa-sun'); // Change to sun icon for light mode
    }

    // Add click event listener to toggle theme
    themeToggle.addEventListener('click', () => {
        document.body.classList.toggle('light-mode');
        if (document.body.classList.contains('light-mode')) {
            themeIcon.classList.replace('fa-moon', 'fa-sun'); // Change to sun icon for light mode
            localStorage.setItem('theme', 'light'); // Save theme preference
        } else {
            themeIcon.classList.replace('fa-sun', 'fa-moon'); // Change to moon icon for dark mode
            localStorage.setItem('theme', 'dark'); // Save theme preference
        }
    });
});
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".toggle-password").forEach(icon => {
        icon.addEventListener("click", () => {
            const input = document.querySelector(icon.getAttribute("toggle"));
            const type = input.getAttribute("type") === "password" ? "text" : "password";
            input.setAttribute("type", type);
            icon.classList.toggle("fa-eye");
            icon.classList.toggle("fa-eye-slash");
        });
    });
});
