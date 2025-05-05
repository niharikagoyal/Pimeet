# services/trainer_service.py (or inline if not modularized)
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from db import get_db_connection

def assign_trainer_to_db(trainer_id, name, email, mobile, status, bio):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO trainers (trainer_id, name, email, mobile, status, bio)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (trainer_id, name, email, mobile, status, bio))
        conn.commit()
        return True, "Trainer assigned successfully!"
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()

def get_all_trainers_from_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM trainers')
        rows = cursor.fetchall()
        trainers = []
        for row in rows:
            trainers.append({
    'trainer_id': row[1],
    'name': row[2],
    'email': row[3],
    'mobile': row[4],
    'status': row[5],
    'bio': row[6],
})

        return True, trainers
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()
def send_email(name, recipient_email, username, password):
    sender_email = "20211460@sbsstc.ac.in"
    sender_password = "afvg zbgz anhe zdaa"

    subject = "Trainer Assignment & Login Credentials"
    body = f"""
    Hi {name},

    You have been successfully assigned as a trainer.

    Here are your login credentials:

    Username: {username}
    Password: {password}

    Please keep these details safe and contact us if you need assistance.

    Best regards,
    Admin Team
    """

    # Setup MIME
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    # Send Email
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, message.as_string())
