from flask_mail import Message
from flask import current_app
from . import mail

def send_email(user_data):
    
    msg = Message(
        subject=f"Inquiry: {user_data['user_subject']}",
        sender= current_app.config['MAIL_USERNAME'],
        recipients = [current_app.config['MY_PERSONAL_EMAIL']]
    )
    #Create the Formal HTML Body
   
    msg.html = f"""
    <html>
        <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #333; line-height: 1.6; background-color: #f9f9f9; padding: 20px;">
            <div style="max-width: 600px; margin: auto; background: #ffffff; border: 1px solid #ddd; border-radius: 8px; overflow: hidden;">
                
                <div style="background-color: #7c3aed; color: #ffffff; padding: 20px; text-align: center;">
                    <h2 style="margin: 0;">New Portfolio Message</h2>
                </div>

                <div style="padding: 30px;">
                    <p style="font-size: 16px;">Hello Talha, you have received a new inquiry from your contact form.</p>
                    
                    <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
                        <tr>
                            <td style="padding: 10px; border-bottom: 1px solid #eee; font-weight: bold; width: 30%;">Name:</td>
                            <td style="padding: 10px; border-bottom: 1px solid #eee;">{user_data['user_name']}</td>
                        </tr>
                        <tr>
                            <td style="padding: 10px; border-bottom: 1px solid #eee; font-weight: bold;">Email:</td>
                            <td style="padding: 10px; border-bottom: 1px solid #eee;">
                                <a href="mailto:{user_data['user_email']}" style="color: #7c3aed;">{user_data['user_email']}</a>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 10px; border-bottom: 1px solid #eee; font-weight: bold;">Subject:</td>
                            <td style="padding: 10px; border-bottom: 1px solid #eee;">{user_data['user_subject']}</td>
                        </tr>
                    </table>

                    <div style="margin-top: 25px;">
                        <h4 style="margin-bottom: 10px; color: #7c3aed;">Message Content:</h4>
                        <div style="background: #f4f4f4; padding: 15px; border-radius: 5px; white-space: pre-wrap;">
                            {user_data['user_message']}
                        </div>
                    </div>
                </div>

                <div style="padding: 15px; background: #eee; text-align: center; font-size: 12px; color: #777;">
                    This email was generated from your TechNest Portfolio Contact Form.
                </div>
            </div>
        </body>
    </html>
    """
    mail.send(msg)