# app.py
from flask import Flask, render_template, request, jsonify
from playwright.sync_api import sync_playwright

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', title='SkyScraper', message='Screenshot What?')

@app.route('/screenshot', methods=['POST'])
def take_screenshot():
    url = request.form.get('url')
    if not url:
        return render_template('err.html', title='Error Dumbass', message='no url dumbass')
    try:
        if not url.lower().startswith('http'):
            url = 'https://' + url
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url)
            screenshot = page.screenshot()
            browser.close()
    
        return screenshot, 200, {"Content-Type": "image/png"}
    
    except Exception as e:
        return render_template('err.html', title='Error Dumbass', message=str(e))

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=4200)