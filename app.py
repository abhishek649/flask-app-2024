import os

from flask import Flask, render_template # type: ignore

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("index.html")
@app.route('/contactus')
def contact():
    return render_template("contact.html")
@app.route('/aboutus')
def aboutus():
    return '<h1>We are an analytics firm working since 2024.</h1>'

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))