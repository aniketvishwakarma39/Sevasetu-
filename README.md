🚀 SevaSetu – Community Service Platform

-"Django" (https://img.shields.io/badge/Django-5.2-green?style=for-the-badge&logo=django)
-"Python" (https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python)
-"Status" (https://img.shields.io/badge/Status-Active-success?style=for-the-badge)
-"License" (https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

---

🌟 Overview

SevaSetu is a community-driven platform that connects volunteers, sponsors, and event creators to collaborate for social good.

It enables:

- 🤝 Seamless participation in social events
- 🚨 Real-time SOS emergency support
- 🏆 Reward system with badges & certificates

---

🎯 Objective

«To create a trusted and efficient digital ecosystem where people can help others, verify contributions, and respond to emergencies quickly.»

---

⚡ Features

👤 Multi-Role System

- Volunteer
- Event Creator
- Sponsor

---

📅 Event Management

- Create & manage events
- Location-based filtering
- Auto-delete expired events

---

✅ Approval System (Core Feature 🔥)

- Volunteers request to join
- Sponsors request funding
- Creator approves/rejects

---

🚨 SOS Emergency System

- Create urgent help requests
- Volunteers can respond instantly
- Email alert system 📧
- Creator verifies helpers

---

🏆 Gamification

- Points system
- Badges (Beginner → Champion)
- Leaderboard

---

🎓 Certificate Generation

- Dynamic certificate generation
- Downloadable PDF
- User-specific achievements

---

🤖 Smart Chatbot

- Rule-based assistant
- Location-based seva suggestions

---

🧠 Challenges & Solutions

Challenge| Solution
Fake participation| Approval system
Fake sponsorship| Verification workflow
SOS urgency| Email alerts + control
Location accuracy| Reverse geocoding
Trust issues| Role-based system

---

🛠️ Tech Stack

- Backend: Django
- Frontend: HTML, CSS, JS
- Database: SQLite
- Email: SMTP (Gmail)
- PDF: pdfkit / wkhtmltopdf

---

🚀 Installation

git clone https://github.com/your-username/sevasetu.git
cd sevasetu

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver

---

⚙️ Setup

📧 Email Configuration

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'

---

📸 Screenshots

- Event Dashboard
- SOS Page
- Certificate
- Leaderboard

(Add images here)

---

🔮 Future Improvements

- 📍 Google Maps integration
- 🔔 Real-time notifications
- 🤖 AI chatbot
- 💳 Payment gateway
- 📱 Mobile app

---

🧑‍💻 Author

Community Sevasetu Team

---

⭐ Support

If you like this project, give it a ⭐ on GitHub!

---

📜 License

This project is licensed under the MIT License.