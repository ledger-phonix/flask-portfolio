import cloudinary.uploader
from flask import render_template , Blueprint, request, flash, redirect, url_for, send_from_directory, jsonify
from .mail_utils import send_email
from .database import db_handler
from .chatbot import get_bot_response
import os
main = Blueprint('main',__name__)

@main.route('/')
def index():
    certificates = db_handler.get_all_certificates()
    testimonials = db_handler.get_active_testimonials()
     
    return render_template('main/index.html', all_certificates = certificates , active_testimonials = testimonials)

@main.route('/robots.txt')
def serve_robots():
    # Combines your root path with the static folder name
    static_folder_path = os.path.join(main.root_path, 'static')
    
    # Grabs robots.txt directly from app/static/
    return send_from_directory(static_folder_path, 'robots.txt')

@main.route('/contact', methods = ['GET','POST'])
def contact():
    if request.method== 'POST':
        
        user_data = {
            'user_name' : request.form['name'],
            'user_email' : request.form['email'],
            'user_subject' : request.form['subject'],
            'user_message' : request.form['message']
        }
        
        try:
            send_email(user_data)
            flash(f'Thanks {user_data["user_name"]}! Your message has been sent successfully', 'success')
        except Exception as e:
            print(repr(e))
            flash('Email failed to sent!', 'error') 
     
        return redirect(url_for('main.contact'))
    return render_template('main/contact.html')

@main.route('/testimonial', methods = ['GET', 'POST'] )
def testimonial():
    if request.method == 'POST':
        file_to_upload = request.files['picture']
        image_url = ""
       
        if file_to_upload:
            try:
                upload = cloudinary.uploader.upload(file_to_upload, folder = 'clients')
                image_url = upload.get('secure_url')
            except Exception as e:
                flash('Upload Failed!', 'error')    
        testimonial_data = {
            't_name': request.form['name'],
            't_title': request.form['title'],
            't_stars': int(request.form['stars']),
            't_text': request.form['description'],
            't_linkedin': request.form['linkedin'],
            't_image': image_url,
            't_display' : False
        }
        try:
            db_handler.save_testimonials(testimonial_data)
            flash('Testimonial saved successfully!', 'success')
        except Exception as e:
            flash(f"Error: {e}!!", "error")
        
        return redirect(url_for('main.testimonial'))
    return render_template('main/testimonial.html')

@main.route('/subscribe', methods = ['POST'])
def subscribe():
    email = request.form['email']
    if email:
        try:
            #check if the email is already avaiable
            existing = db_handler.subscribers.find_one({"email" : email })
            if existing:
                flash("You already subscribed!", "Info")
            else:
                db_handler.save_email(email)
                flash("Thanks for subscribing!", 'success')
        except Exception as e:
            flash(f"Subscription failed! {e}")
    return redirect(request.referrer or url_for('main.index'))  
             
@main.route('/projects')
def projects():
    selected_category = request.args.get('category')    
    projects = db_handler.get_all_projects(category=selected_category)    
    return render_template('main/projects.html', all_projects=projects, current_category=selected_category)

@main.route('/blog')
def blog():
    return render_template('main/blog.html')


@main.route('/api/chat', methods=['POST'])
def chat_api():
      # 1. Safely extract the JSON payload from the request
    data = request.get_json()
    
    # 2. Validation: Ensure a payload and message exist
    if not data or 'message' not in data:
        return jsonify({"error": "Invalid request framework. 'message' key missing."}), 400
        
    user_message = data['message'].strip()
    
    if not user_message:
        return jsonify({"error": "Empty message string received."}), 400

    # 3. Process the question using our Gemini function
    bot_reply = get_bot_response(user_message)

    # 4. Return the clean text reply back to the frontend browser as JSON
    return jsonify({"reply": bot_reply})
