from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('index_coffee.html')

@app.route('/sike_HAHA', methods=['GET'])
def new_page():
    return render_template('homepage.html')

if __name__ == '__main__':
    app.run(debug=True)