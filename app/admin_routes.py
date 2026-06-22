from flask import Blueprint, render_template, request, redirect, url_for , session, flash, jsonify
import os
import cloudinary
from .database import db_handler
admin = Blueprint('admin', __name__)

#login decorator
def login_required(func):
    def wrapper(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('admin.login'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


@admin.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == os.getenv('ADMIN_USER') and password == os.getenv('ADMIN_PASSWORD'):
            session['logged_in'] = True
            flash('Welcome back, Talha!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid Credentials!', 'error')
            return redirect(url_for('admin.login'))
    return render_template('admin/login.html')

@admin.route("/dashboard")
@login_required
def dashboard():
    t_count = db_handler.testimonials.count_documents({})
    p_count = db_handler.projects.count_documents({})
    c_count = db_handler.certificates.count_documents({})
    return render_template('admin/dashboard.html', t_count=t_count, p_count=p_count, c_count=c_count)

@admin.route('/projects-form', methods = ['GET', 'POST'])
@login_required
def projects_form():
    if request.method == 'POST':
        image = request.files.get('project_image')
        image_url = ""
        if image:
            try:
                upload = cloudinary.uploader.upload(image, folder = 'projects')
                image_url = upload.get('secure_url')
            except Exception as e:
                flash(f'Upload failed! Error:{e}')
                
        tags = request.form['tags']
        tags_list = tags.split(",")
        Tags = []
        for tag in tags_list:
            Tags.append(tag.strip())
            
        project_data = {
            'p_title' : request.form['title'],
            'p_link' : request.form['link'],
            'p_description' : request.form['description'],
            'p_tags' : Tags,
            'p_image' : image_url,
            'p_category': request.form['category']
        }
        try:
            db_handler.save_projects(project_data)
            flash("Project saved to DB!", "success")
        except Exception as e:
            flash(f"Error: {e}")
        return redirect(url_for('admin.projects_form'))
    return render_template('admin/projects_form.html')

@admin.route('/testimonials-list')
@login_required
def testimonials_list():
    list_testmonials = db_handler.get_all_testimonials()
    # print(list_testmonials)
    return render_template('admin/testimonials_list.html', all_testimonials = list_testmonials)

@admin.route('/update-testimonial-visibility', methods = ['POST'])
@login_required
def update_visibility():
    data = request.get_json()
    t_id = data.get('id')
    new_status = data.get('display')
    try:
        db_handler.update_testimonial_status(t_id, new_status)
        # flash('Display status updated!', 'success')
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@admin.route('/certificates-form', methods = ['POST', 'GET'])
@login_required
def certificates_form():
    if request.method == 'POST':
        image = request.files['certificate_image']
        upload = cloudinary.uploader.upload(image, folder = "certificates")
        image_url = upload.get('secure_url')
        certificate_data = {
            'c_title' : request.form['title'],
            'c_issuer' : request.form['issuer'],
            'c_year' : request.form['year'],
            'c_description' : request.form['description'],
            'c_image' : image_url
        }
        try: 
            db_handler.save_certificates(certificate_data)
            flash('Certifcate saved in DB!', 'success')
        except Exception as e:
            flash(f'Error: {e}')
        return redirect(url_for('admin.certificates_form'))
    return render_template('admin/certificates_form.html')


@admin.route('/admin-blogs')
@login_required
def admin_blogs():
    return render_template('/admin/admin_blogs.html')
@admin.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('admin.login'))