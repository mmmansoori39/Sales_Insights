from flask import Flask, render_template, request, redirect, url_for, session
import os
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from flask_socketio import SocketIO


app = Flask(__name__)
app.secret_key = 'mdmoinuddinmansoori'
socketio = SocketIO(app)


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
        return redirect(url_for('dashboard_page'))
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

@app.route('/upload_page')
def index():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        data = pd.read_excel(uploaded_file)
        cleaned_data = data.drop_duplicates()  # Remove duplicates

        # Save cleaned data in session for later use
        session['cleaned_data'] = cleaned_data.to_html(classes='data')
        return render_template('display.html', tables=[data.to_html(classes='data')], titles=['Data'])

    return render_template('index.html', error='Please upload a file.')

@app.route('/bar_graph', methods=['GET', 'POST'])
def bar_graph():
    if 'cleaned_data' not in session:
        # Redirect to the index page if data is not available
        return redirect(url_for('index'))

    if request.method == 'POST':
        x_axis = request.form.get('x_axis')
        y_axis = request.form.get('y_axis')

        # Generate bar graph
        cleaned_data = pd.read_html(session['cleaned_data'], index_col=0)[0]
        plt.bar(cleaned_data[x_axis], cleaned_data[y_axis])
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)
        plt.title('Bar Graph')

        # Save the plot to a BytesIO object
        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode('utf8')

        # Render the template with the bar graph
        return render_template('bar_graph.html', plot_url=plot_url)

    return render_template('bar_graph_input.html')

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



@app.route('/voice_activation_page')
def voice_activation_page():
    return render_template('voice_activation.html')



@app.route('/text_to_speech_page')
def text_to_speech_page():
    return render_template('text_to_speech.html')

@app.route('/logout_page')
def logout_page():
    return render_template('logout.html')

@app.route('/setting_page')
def setting_page():
    return render_template('setting.html')

@app.route('/history_page')
def history_page():
    return render_template('history.html')


@app.route('/voice_command')
def voice_command():
    return render_template('voice.html')

if __name__ == '__main__':
    import eventlet
    eventlet.monkey_patch()

    # Start the Flask-SocketIO application
    socketio.run(app, debug=True)
