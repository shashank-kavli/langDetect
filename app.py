from flask import Flask, render_template, request
import pandas as pd
import requests
from bs4 import BeautifulSoup
from langdetect import detect

app = Flask(__name__)

# Function to detect language of website
def detect_language_of_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        language = detect(text)
        return language
    except requests.exceptions.RequestException:
        return None

# Route for homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle file upload and display results in an HTML table
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    
    # Read the Excel file
    try:
        df = pd.read_excel(file)
        # Assuming the Excel file contains a column 'Website' with URLs
        websites = df['Website'].tolist()
    except Exception as e:
        return f"Error reading file: {e}"

    # Detect language for each website
    result = []
    for website in websites:
        language = detect_language_of_website(website)
        result.append((website, language if language else 'Error'))

    return render_template('results.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
