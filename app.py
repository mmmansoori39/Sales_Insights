from flask import Flask, render_template, request, redirect, url_for
import os
import pandas as pd

app = Flask(__name__)

# Dummy database (replace with an actual database in a real project)
users = [{'username': 'user1', 'password': 'password1'}, {'username': 'user2', 'password': 'password2'}]

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = next((user for user in users if user['username'] == username and user['password'] == password), None)

    if user:
        # Add authentication code here (e.g., session management)
        return redirect(url_for('dashboard'))
    else:
        return "Invalid credentials. Please try again."



@app.route('/signup')
def signup_page():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    # Check if username is unique (you might want to add email uniqueness as well)
    if next((user for user in users if user['username'] == username), None):
        return "Username already exists. Please choose a different one."

    users.append({'username': username, 'email': email, 'password': password})
    return redirect(url_for('login_page'))



# Create a directory to store uploaded files if it doesn't exist
if not os.path.exists('uploads'):
    os.makedirs('uploads')

@app.route('/upload_page')
def upload_page():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']

    if file and allowed_file(file.filename):
        filename = os.path.join('uploads', secure_filename(file.filename))
        file.save(filename)

        # Add code for data cleaning and preprocessing (using pandas)
        df = pd.read_excel(filename)
        
        # Example data cleaning: Drop rows with missing values
        df = df.dropna()

        # Example data preprocessing: Add a new column
        df['Total Sales'] = df['Quantity'] * df['Price']

        # Save the cleaned and preprocessed data
        cleaned_filename = os.path.join('uploads', 'cleaned_' + secure_filename(file.filename))
        df.to_excel(cleaned_filename, index=False)

        return redirect(url_for('dashboard'))
    else:
        return "Invalid file format. Please upload an Excel file."

# Helper function to check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'xlsx', 'xls'}



@app.route('/dashboard_page')
def dashboard_page():
    return render_template('dashboard.html')


@app.route('/feedback_page')
def feedback_page():
    return render_template('feedback.html')

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    feedback = request.form['feedback']

    # Add code to handle feedback (e.g., store in a database)

    return "Thank you for your feedback!"

@app.route('/explore_page')
def explore_page():
    return render_template('explore.html')

@app.route('/accessible_page')
def accessible_page():
    return render_template('accessible.html')

if __name__ == '__main__':
    app.run(debug=True)

