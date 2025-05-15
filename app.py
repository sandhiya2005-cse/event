from flask import Flask, request, jsonify, render_template, redirect
from supabase import create_client
from gotrue.errors import AuthApiError

app = Flask(__name__)

SUPABASE_URL = "https://tpxsdzslqwknmfyfzses.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRweHNkenNscXdrbm1meWZ6c2VzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDcxMjg2ODEsImV4cCI6MjA2MjcwNDY4MX0.sUic3CMLBw3kO4VKJvJrfJkyXG56HC3k6OKOKPQT5P4"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            response = supabase.auth.sign_up({'email': email, 'password': password})
            return render_template('signup.html', message="Check your email to confirm your account.")
        except AuthApiError as e:
            return render_template('signup.html', error=str(e))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = supabase.auth.sign_in_with_password({'email': email, 'password': password})
            if user:
                return redirect('/dashboard')
        except AuthApiError as e:
            return render_template('login.html', error=str(e))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/events')
def events():
    events = supabase.table("events").select("*").execute()
    return jsonify(events.data)

@app.route('/api/attend/<event_id>', methods=['POST'])
def attend(event_id):
    return jsonify({"message": f"Attendance marked for event {event_id}!"})

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for

app = Flask(_name_)

# Sample in-memory storage for demonstration purposes
signed_up_emails = set()

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        signed_up_emails.add(email)
        return render_template('signup.html', message='Signed up successfully!')
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        if email in signed_up_emails:
            # Assuming password verification is done here
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid email or password')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if _name_ == '_main_':
    app.run(debug=True)