## 🌐 Pimeet — Smart Meeting Management Made Simple
Pimeet is a user-friendly, web-based meeting management system built with Flask. It empowers users, trainers, and administrators to easily schedule, manage, and oversee meetings — all from a single platform. With features like trainer assignment, profile image uploads, and role-based dashboards, Pimeet simplifies coordination and boosts productivity.

## 🚀 Key Features
🔐 User Authentication
Secure login/logout for users, trainers, and admins.

🛠️ Admin Dashboard
View all trainers and meetings

Assign trainers to specific meetings

Edit or cancel meetings as needed

👨‍🏫 Trainer Dashboard
View all assigned meetings

Update meeting details efficiently

👤 User Dashboard
Track upcoming and current meetings

Upload and manage profile images

📅 Meeting Management
Create, reschedule, or end meetings

Access meeting rooms directly from the dashboard

🖼️ Profile Management
Upload and fetch profile images

## 🗂️ Project Structure
csharp
Copy
Edit
├── app.py              # Main Flask application
├── assign_trainer.py   # Trainer assignment logic
├── data.ipynb          # Data analysis notebook
├── db.py               # Database initialization
├── login.py            # Login logic
├── meetings.py         # Meeting-related functionality
├── profileimg.py       # Profile image handling
├── signup.py           # Signup functionality
├── uploadimg.py        # Image upload utility
├── test.py             # Test cases
├── requirements.txt    # Project dependencies
├── pimeet.db           # SQLite database
├── static/             # Static files (CSS, JS)
├── templates/          # HTML templates
└── README.md           # Project documentation

## 🧪 Installation & Setup
Clone the Repository


git clone https://github.com/niharikagoyal/Pimeet.git
cd Pimeet
Create a Virtual Environment & Activate It


python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Dependencies


pip install -r requirements.txt
Set Up the Database

Ensure pimeet.db is in the root folder

Or initialize it using init_db() in db.py

Run the Application

python app.py
Access the App
Open your browser and navigate to:
http://127.0.0.1:5000

## 👥 User Roles & Usage
Admin: Manage all trainers and meetings via the dashboard

Trainer: View and update assigned meetings

User: Check upcoming meetings, upload profile images

## 📦 Dependencies
Flask

SQLite

Other dependencies listed in requirements.txt

## 📄 License
Licensed under the MIT License. See the LICENSE file for more info.

## 🤝 Contributing
Contributions are welcome!
Fork the repo, make your changes, and submit a pull request. Let's build something great together!

