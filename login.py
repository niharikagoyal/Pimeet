from flask import render_template, redirect, url_for, session, flash, jsonify, request, current_app
from db import get_db_connection
import bcrypt
import os
from dotenv import load_dotenv

load_dotenv()

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD_HASH").encode('utf-8')



def handle_login(request):
    if request.method == 'POST':
        username = request.form.get('username')  # Admin username or trainer_id
        password = request.form.get('password')  # Admin password or trainer's mobile

        if not username or not password:
            flash("Username or password missing!", "error")
            return redirect(url_for('login'))

        # Admin login
        if username == ADMIN_USERNAME and bcrypt.checkpw(password.encode('utf-8'), ADMIN_PASSWORD_HASH):
            session['user_type'] = 'admin'
            return redirect(url_for('admin_dashboard'))

        # Trainer login from SQLite
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM trainers WHERE trainer_id = ?", (username,))
        trainer = cursor.fetchone()

        if trainer:
            db_mobile = trainer['mobile']
            if password == db_mobile:
                session['trainer_id'] = trainer['trainer_id']
                session['trainer_name'] = trainer['name']
                session['user_type'] = 'trainer'
                flash("Trainer login successful!", "success")
                return redirect(url_for('trainer_dashboard'))
            else:
                flash("Invalid mobile number", "error")
                return redirect(url_for('login'))
                # Student login from SQLite
        cursor.execute("SELECT * FROM students WHERE name = ?", (username,))
        student = cursor.fetchone()

        if student:
            db_mobile = student['contact']
            if password == db_mobile:
                session['student_id'] = student['id']
                session['student_name'] = student['name']
                session['user_type'] = 'student'
                flash("Student login successful!", "success")
                return redirect(url_for('user_dashboard'))
            else:
                flash("Invalid mobile number", "error")
                return redirect(url_for('login'))

        flash("Invalid name or mobile number", "error")
        return redirect(url_for('login'))
        conn.close()

    return render_template('login.html')
