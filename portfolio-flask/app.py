import os
import csv
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from dotenv import load_dotenv

# load .env if present
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")

# Flask-Mail config (read from env)
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() in ('true', '1', 'yes')
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL', 'False').lower() in ('true', '1', 'yes')
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')  # your SMTP username/email
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  # your SMTP password / app password
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', app.config['MAIL_USERNAME'])

mail = Mail(app)

# Example projects list (edit as needed)
PROJECTS = [
    {"title": "Text-to-Image Generator", "desc": "Generative model using diffusion & Hugging Face", "link": "#"},
    {"title": "Hospital Biometric System", "desc": "Face and fingerprint based biometric system", "link": "#"},
    {"title": "IronMan Subway Surfer", "desc": "Pygame-based arcade project", "link": "#"},
]

MESSAGES_CSV = "messages.csv"

def save_message_csv(name, email, subject, message):
    header = ['name', 'email', 'subject', 'message']
    write_header = not os.path.exists(MESSAGES_CSV)
    with open(MESSAGES_CSV, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(header)
        writer.writerow([name, email, subject, message])

@app.route('/')
def home():
    return render_template('index.html', projects=PROJECTS)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/projects')
def projects():
    return render_template('projects.html', projects=PROJECTS)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', 'Portfolio Contact').strip()
        message_body = request.form.get('message', '').strip()

        if not name or not email or not message_body:
            flash("Please fill in name, email and message.", "danger")
            return redirect(url_for('contact'))

        # Save to CSV (backup)
        try:
            save_message_csv(name, email, subject, message_body)
        except Exception as e:
            app.logger.error("Error writing CSV: %s", e)

        # Send email via SMTP (Flask-Mail)
        try:
            msg = Message(subject=f"[Portfolio Contact] {subject}",
                          sender=app.config.get('MAIL_DEFAULT_SENDER'),
                          recipients=[os.getenv('MAIL_RECEIVER', app.config.get('MAIL_USERNAME'))])
            msg.body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message_body}"
            mail.send(msg)
            flash("Message sent successfully! Thank you.", "success")
        except Exception as e:
            app.logger.error("Mail send failed: %s", e)
            flash("Could not send email. Message saved locally. Check server logs.", "warning")

        return redirect(url_for('contact'))

    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
