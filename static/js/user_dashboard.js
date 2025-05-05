// Function to show specific sections
function showSection(section) {
    document.getElementById('meetings').classList.add('hidden');
    document.getElementById('trainers').classList.add('hidden');
    document.getElementById(section).classList.remove('hidden');
}
setTimeout(() => {
    document.querySelectorAll('.toast-message').forEach(msg => {
      msg.remove();
    });
  }, 4000);

// Theme toggle functionality
const themeToggle = document.getElementById('themeToggle');
themeToggle.addEventListener('click', function () {
    document.body.classList.toggle('light-mode');
    const icon = themeToggle.querySelector('i');
    if (document.body.classList.contains('light-mode')) {
        icon.classList.remove('fa-moon');
        icon.classList.add('fa-sun');
    } else {
        icon.classList.remove('fa-sun');
        icon.classList.add('fa-moon');
    }
});

// Sidebar toggle functionality
const sidebarToggle = document.getElementById('sidebarToggle');
const sidebar = document.getElementById('sidebar');
const content = document.getElementById('content');

sidebarToggle.addEventListener('click', () => {
    sidebar.classList.toggle('closed');
    content.classList.toggle('shifted');
});

// Function to toggle sub-menu visibility
function toggleSubMenu(subMenuId) {
    const subMenu = document.getElementById(subMenuId);
    subMenu.classList.toggle('hidden');
}

// Function to show specific sections
function showSection(sectionId) {
    const sections = document.querySelectorAll('.content > div');
    sections.forEach(section => section.classList.add('hidden'));
    document.getElementById(sectionId).classList.remove('hidden');
}

document.getElementById("profileToggle").onclick = function () {
    document.getElementById("profileModal").style.display = "block";
};

// Handle logout
function handleLogout() {
    Swal.fire({
        title: 'Are you sure?',
        text: "You will be logged out of your account!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'Yes, logout!'
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = '/logout';
        }
    });
}

// Close profile modal
document.getElementById("closeModal").onclick = function () {
    document.getElementById("profileModal").style.display = "none";
};

// Close modal if click outside content
window.onclick = function (event) {
    const modal = document.getElementById("profileModal");
    if (event.target === modal) {
        modal.style.display = "none";
    }
};

