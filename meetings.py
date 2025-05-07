import datetime
import sqlite3
from db import get_db_connection
from datetime import datetime, timedelta
from flask import jsonify, redirect, render_template, request, flash, session, url_for
from datetime import timezone

def get_meet():
    now = datetime.now()  # Get current local time
    previous, current, upcoming = [], [], []
    trainer_id = session.get('trainer_id')

    conn = get_db_connection()
    cursor = conn.cursor()

    # Build the base query
    query = """
        SELECT m.id as meeting_id, m.title, m.date, m.time, m.description, t.name as trainer_name 
        FROM meetings m 
        LEFT JOIN trainers t ON m.trainer_id = t.trainer_id
    """
    
    # Add WHERE clause for trainer-specific meetings
    if trainer_id:
        query += " WHERE m.trainer_id = ? "
        cursor.execute(query, (trainer_id,))
    else:
        cursor.execute(query)

    rows = cursor.fetchall()

    for row in rows:
        # Convert meeting time to datetime object
        meeting_dt = datetime.strptime(f"{row['date']} {row['time']}", "%Y-%m-%d %H:%M")
        end_time = meeting_dt + timedelta(hours=1)

        item = {
            'id': row['meeting_id'],
            'title': row['title'],
            'date': row['date'],
            'time': row['time'],
            'description': row['description'],
            'trainer_name': row['trainer_name'],
            'status': 'Scheduled'
        }

        if end_time < now:
            item['status'] = 'Completed'
            previous.append(item)
        elif meeting_dt <= now < end_time:
            item['status'] = 'Ongoing'
            current.append(item)
        else:
            item['status'] = 'Scheduled'
            upcoming.append(item)

    conn.close()

    # Sort meetings by date and time
    previous.sort(key=lambda x: datetime.strptime(f"{x['date']} {x['time']}", "%Y-%m-%d %H:%M"), reverse=True)
    upcoming.sort(key=lambda x: datetime.strptime(f"{x['date']} {x['time']}", "%Y-%m-%d %H:%M"))

    return {
        'previous': previous,
        'current': current,
        'upcoming': upcoming
    }

def create_meet():
    title = request.form.get('meetingTitle')
    date = request.form.get('meetingDate')
    time = request.form.get('meetingTime')
    description = request.form.get('meetingDescription')
    trainer_id = session.get('trainer_id')  # Get trainer_id from session

    print("Title:", title)
    print("Date:", date)
    print("Time:", time)
    print("Description:", description)
    print("Trainer ID:", trainer_id)

    if not all([title, date, time, description, trainer_id]):
        return jsonify({'error': 'Missing fields or not logged in'}), 400

    try:
        conn = sqlite3.connect('pimeet.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO meetings (title, date, time, description, trainer_id)
            VALUES (?, ?, ?, ?, ?)
        """, (title, date, time, description, trainer_id))
        conn.commit()
        conn.close()
        return redirect('/trainer_dashboard')
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'Failed to create meeting'}), 500


    return jsonify({'success': True})
def edit_meeting_ad():
    data = request.form
    meeting_id = data.get('id')
    title = data.get('title')
    date = data.get('date')
    time = data.get('time')
    description = data.get('description')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE meetings
        SET title = ?, date = ?, time = ?, description = ?
        WHERE id = ?
    """, (title, date, time, description, meeting_id))
    conn.commit()
    conn.close()
    flash("Meeting updated successfully.", "success")
    return redirect(url_for('admin_dashboard'))

def edit_meeting():
    data = request.form
    meeting_id = data.get('id')
    title = data.get('title')
    date = data.get('date')
    time = data.get('time')
    description = data.get('description')
    trainer_id = session.get('trainer_id')
    
    if not all([meeting_id, title, date, time, description, trainer_id]):
        flash("Missing required fields or not logged in", "error")
        return redirect(url_for('trainer_dashboard'))
        
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE meetings
            SET title = ?, date = ?, time = ?, description = ?
            WHERE id = ? AND trainer_id = ?
        """, (title, date, time, description, meeting_id, trainer_id))
        
        if cursor.rowcount > 0:
            conn.commit()
            flash("Meeting updated successfully.", "success")
        else:
            flash("No meeting found or you don't have permission to edit this meeting.", "error")
    except Exception as e:
        flash("Failed to update meeting. Please try again.", "error")
    finally:
        conn.close()
    return redirect(url_for('trainer_dashboard'))


def delete_meeting_trainer(meeting_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM meetings WHERE id = ? AND trainer_id = ?", (meeting_id, session.get('trainer_id')))
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    if rows_affected > 0:
        flash("Meeting deleted successfully.", "warning")
    else:
        flash("Failed to delete meeting. Please try again.", "error")
    return redirect(url_for('trainer_dashboard'))

def reschedule_meet():
    meeting_id = request.form.get('meeting_id')
    new_date = request.form.get('new_date')
    new_time = request.form.get('new_time')

    if meeting_id and new_date and new_time:
        with sqlite3.connect('pimeet.db') as conn:
            c = conn.cursor()
            c.execute("UPDATE meetings SET date = ?, time = ? WHERE id = ?", (new_date, new_time, meeting_id))
            conn.commit()
        flash("Meeting rescheduled successfully.", "success")
    else:
        flash("Failed to reschedule. Please try again.", "danger")

    return redirect(url_for('trainer_dashboard'))
def start_meet(meeting_id):
    
    if 'email' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('home'))

    email = session.get('email')
    conn = sqlite3.connect('pimeet.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT username FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('home'))

    return render_template('meeting_room.html', meeting_id=meeting_id, username=user['username'])

def end_meet(meeting_id):
    if 'email' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('trainer_dashboard'))

    
    flash('Meeting ended successfully.', 'success')
    return redirect(url_for('trainer_dashboard', meeting_id=meeting_id))  # Redirect after ending


def cancel_meeting_ad(meeting_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM meetings WHERE id = ?", (meeting_id,))
    conn.commit()
    conn.close()
    flash("Meeting canceled successfully.", "warning")
    return redirect(url_for('admin_dashboard'))


def update_meet():
    data = request.json
    print("Data received:", data)
    meet_id = data.get('meetingID')
    title = data.get('title')
    date = data.get('date')
    time = data.get('time')

    if not (meet_id and title and date and time):
        return jsonify({'status': 'error', 'message': 'Missing required data'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Debugging: print out the query and parameters
        print(f"Updating meeting with meet_id={meet_id}, title={title}, date={date}, time={time}")

        cursor.execute('''
            UPDATE meetings
            SET meet_id = ?
            WHERE title = ? AND date = ? AND time = ? AND meet_id IS NULL
        ''', (meet_id, title, date, time))

        # Debugging: check how many rows were affected
        if cursor.rowcount == 0:
            return jsonify({'status': 'error', 'message': 'No matching meeting found or already updated'}), 404

        conn.commit()
        conn.close()

        return jsonify({'status': 'success', 'message': 'Meeting ID updated'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

