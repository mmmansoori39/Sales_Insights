from flask import Flask, render_template, request, redirect, url_for

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


@app.route('/signup_page', methods=['GET', 'POST'])
def signup_page():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Add code to store user information in the database (dummy data in this case)

        return redirect(url_for('login_page'))

    return render_template('signup.html')


@app.route('/dashboard')
def dashboard():
    # Add authorization code here
    return "Welcome to the Sales Insights Dashboard!"


if __name__ == '__main__':
    app.run(debug=True)

