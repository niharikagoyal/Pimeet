// Function to show specific sections
function showSection(section) {
    document.getElementById('meetings').classList.add('hidden');
    document.getElementById('trainers').classList.add('hidden');
    document.getElementById('live-sessions').classList.add('hidden');
    document.getElementById(section).classList.remove('hidden');
    
    // If showing live sessions, show the ongoing tab by default
    if (section === 'live-sessions') {
        showLiveSubsection('ongoing');
    }
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

// Function to show live session subsections
function showLiveSubsection(subsection) {
    // Hide all subsections first
    const subsections = ['upcoming', 'ongoing', 'past'];
    subsections.forEach(section => {
        const element = document.getElementById('live-' + section);
        if (element) {
            element.style.display = 'none';
        }
    });

    // Show the selected subsection
    const selectedSection = document.getElementById('live-' + subsection);
    if (selectedSection) {
        selectedSection.style.display = 'block';
    }

    // Update button states
    const buttons = document.querySelectorAll('.navigation-meetings .btn');
    buttons.forEach(btn => {
        // Reset all buttons to outline style
        btn.classList.remove('btn-primary');
        btn.classList.add('btn-outline-primary');

        // If this is the active button, update its style
        if (btn.getAttribute('data-section') === subsection) {
            btn.classList.remove('btn-outline-primary');
            btn.classList.add('btn-primary');
        }
    });
}

// Function to toggle card expansion
function toggleCardExpand(button) {
    const card = button.closest('.live-card');
    const cardBody = card.querySelector('.card-body');
    
    if (cardBody.style.display === 'none') {
        cardBody.style.display = 'block';
        button.textContent = 'Collapse';
    } else {
        cardBody.style.display = 'none';
        button.textContent = 'Expand';
    }
}
// Open profile modal
document.getElementById("profileToggle").onclick = function () {
    document.getElementById("profileModal").style.display = "block";
};

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
function openEditModal(id, title, date, time, description) {
    document.getElementById('editMeetingId').value = id;
    document.getElementById('editTitle').value = title;
    document.getElementById('editDate').value = date;
    document.getElementById('editTime').value = time;
    document.getElementById('editDescription').value = description;
    var editModal = new bootstrap.Modal(document.getElementById('editMeetingModal'));
    editModal.show();
}
function confirmCancel(meetingId) {
    Swal.fire({
        title: 'Are you sure?',
        text: "You are about to cancel this meeting!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'Yes, cancel it!'
    }).then((result) => {
        if (result.isConfirmed) {
            // Redirect to cancel route
            window.location.href = `/cancel_meeting/${meetingId}`;
        }
    });
}
function toggleTrainerForm() {
    const form = document.getElementById('assignTrainerForm');
    form.style.display = (form.style.display === 'none') ? 'block' : 'none';
}
// Remove the duplicate showSection function at the bottom

// Add event listeners for live session buttons
document.addEventListener('DOMContentLoaded', function() {
    const liveButtons = document.querySelectorAll('.navigation-meetings .btn');
    liveButtons.forEach(button => {
        button.addEventListener('click', function() {
            const section = this.getAttribute('data-section');
            showLiveSubsection(section);
        });
    });
});
function showSection(sectionId) {
    const sections = ['meetings', 'trainers', 'live-sessions']; // <-- Add 'live-sessions' here

    sections.forEach(id => {
        const section = document.getElementById(id);
        if (section) {
            section.classList.add('hidden');
        }
    });
    sidebar.classList.toggle('closed');
    content.classList.toggle('shifted');
    const target = document.getElementById(sectionId);
    if (target) {
        target.classList.remove('hidden');
    }
}
