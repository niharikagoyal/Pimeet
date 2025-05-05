from flask import Flask, Response, redirect, url_for, request, render_template, session, flash
from login import handle_login
from db import init_db, get_db_connection 
from functools import wraps
from assign_trainer import assign_trainer_to_db,get_all_trainers_from_db,send_email
from uploadimg import handle_profile_image_upload
from profileimg import get_image
from meetings import get_meet, create_meet, reschedule_meet, start_meet, end_meet,edit_meeting, delete_meeting_trainer,edit_meeting_ad,update_meet,cancel_meeting_ad

app = Flask(__name__) 
app.secret_key = 'Pisoft'

init_db()

def login_required():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_type' not in session:
                flash("Please log in first.", "error")
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    return handle_login(request)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))
@app.route('/admin_dashboard')
def admin_dashboard():
    # Set user_type in session for admin
    session['user_type'] = 'admin'
    success, result = get_all_trainers_from_db()
    meetings=get_meet()
    if success:
        return render_template('admindashboard.html', trainers=result,meetings=meetings)
    else:
        return render_template('admindashboard.html', error=result)



@app.route('/edit_meeting', methods=['POST'])
# @login_required()
def edit_meeting_admin():
    return edit_meeting_ad()

@app.route('/cancel_meeting/<int:meeting_id>')
# @login_required()
def cancel_meeting(meeting_id):
  return cancel_meeting_ad(meeting_id)
@app.route('/trainer_dashboard')
def trainer_dashboard():
    if 'trainer_id' not in session:
        flash("Please log in as a trainer to access the dashboard.", "error")
        return redirect(url_for('home'))

    trainer_id = session['trainer_id']

    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch trainer details
    cursor.execute("SELECT * FROM trainers WHERE trainer_id = ?", (trainer_id,))
    trainer = cursor.fetchone()

    if not trainer:
        conn.close()
        flash("Trainer not found.", "error")
        return redirect(url_for('handle_login'))

    conn.close()

    # Now fetch meetings using helper function
    meetings = get_meet()

    return render_template('trainerdashboard.html', trainer=trainer, meetings=meetings)

@app.route('/edit_meeting_trainer', methods=['POST'])
# @login_required()
def edit_meeting_trainer():
    return edit_meeting()
    


@app.route('/user_dashboard')
@login_required()
def user_dashboard():
    if session.get('user_type') != 'student':
        flash("Access denied. Please login as a student.", "error")
        return redirect(url_for('login'))
    meetings = get_meet()
    user_data = {
        'id': session.get('student_id'),
        'username': session.get('student_name')
    }
    return render_template('userdashboard.html', 
                           current_meetings=meetings['current'], 
                           upcoming_meetings=meetings['upcoming'],
                           current_user=user_data)

@app.route('/upload_profile', methods=['POST'])
@login_required()
def upload_profile():
    return handle_profile_image_upload()

@app.route('/get_profile_image/<int:user_id>')
def get_profile_image(user_id):
    image_blob = get_image(user_id)
    if image_blob:
        return Response(image_blob, mimetype='image/png')
    return 'No Image Found', 404

@app.route('/meetings', methods=['GET'])
def get_meeting():
    return get_meet()

@app.route('/create_meeting', methods=['POST'])
def create_meeting():
    return create_meet()

@app.route('/reschedule_meeting', methods=['POST'])
def reschedule_meeting():
    return reschedule_meet()

@app.route('/meeting_room/<int:meeting_id>')
def meeting_room(meeting_id):
    return render_template('meeting_room.html', meeting_id=meeting_id, username=session.get('username'))

@app.route('/end_meeting/<meeting_id>')
def end_meeting(meeting_id):
    return end_meet(meeting_id)
# @app.route('/edit_meeting/<int:meeting_id>', methods=['PUT'])
# def edit_meeting(meeting_id):
#     return edit_meeting_trainer(meeting_id)

@app.route('/assign_trainer', methods=['POST'])
def assign_trainer():
    trainer_id = request.form.get('trainer_id')
    name = request.form.get('name')
    email = request.form.get('email')
    mobile = request.form.get('mobile')
    status = request.form.get('status')
    bio = request.form.get('bio')

    success, message = assign_trainer_to_db(trainer_id, name, email, mobile, status, bio)

    if success:
        try:
            send_email(name, email, trainer_id, mobile)
        except Exception as e:
            flash(f"Trainer saved, but email failed: {str(e)}", "warning")
        else:
            flash(message, "success")
    else:
        flash(f"Failed to assign trainer: {message}", "error")

    return redirect(url_for('admin_dashboard'))
@app.route('/delete_meeting_trainer/<int:meeting_id>')
def delete_meeting(meeting_id):
    return delete_meeting_trainer(meeting_id)

@app.route('/update_meeting_id', methods=['POST'])
def update_meeting_id():
    return update_meet()

if __name__ == '__main__':
    app.run(debug=True)
