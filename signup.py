from flask import render_template, redirect, url_for, flash

import os
from db import get_db_connection


def handle_signup(request):
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
       
        # Save user to the database
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)',
                (username, email, password, role)
            )
            conn.commit()
            conn.close()
            flash(f'Successfully signed up as {role.capitalize()}!', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
            return redirect(url_for('signup'))

    return render_template('signup.html')