from flask import session, flash, redirect, url_for, request
from profileimg import save_profile_image  # Your BLOB-saving function

def handle_profile_image_upload():
    print('upload')
    user_id = session.get('user_id')
    if not user_id:
        flash('User ID not found in session.', 'danger')
        return redirect(url_for('home'))  

    img = request.files.get('profile_image')
    
    if img:
        # img_bytes = img.read()
        success = save_profile_image(img, user_id)
        if success:
            flash('Profile image uploaded successfully!', 'success')
        else:
            flash('Error uploading profile image.', 'danger')
           
    else:
        flash('No file selected.', 'danger')

    role = session.get('role')
    if role == 'admin':
        return redirect(url_for('admin_dashboard'))
    elif role == 'trainer':
        return redirect(url_for('trainer_dashboard'))
    elif role == 'user':
        return redirect(url_for('user_dashboard'))
    else:
        return redirect(url_for('home'))

