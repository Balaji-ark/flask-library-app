import os  # Import os from the standard Python library
from flask import Flask, render_template
from modules import create_app

app = create_app()

# Set the secret key for session management
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'Balaji@2005')  # Use your key here

@app.route('/')
def home():
    return render_template('home.html')  # Ensure 'home.html' exists in your templates directory

if __name__ == '__main__':
    app.run(debug=True)
