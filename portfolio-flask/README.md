# Portfolio Flask App (Mahi)

## Setup
1. Create a virtual env:
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate      # Windows

2. Install deps:
   pip install -r requirements.txt

3. Create a `.env` file in the project root with:
   SECRET_KEY=replace-with-random
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=youremail@example.com
   MAIL_PASSWORD=your_smtp_password_or_app_password
   MAIL_DEFAULT_SENDER=youremail@example.com
   MAIL_RECEIVER=your_receive_email@example.com

   Note: For Gmail, set up an App Password if you have 2FA. Or use any SMTP provider.

4. Run:
   flask run
   # or
   python app.py

5. Open http://127.0.0.1:5000

## Notes
- Contact sends email to MAIL_RECEIVER and appends a copy to messages.csv.
- Replace sample projects in `app.py` or connect to a database if you prefer.
- Add `static/Mahi_Resume.pdf` to enable Resume download link.
