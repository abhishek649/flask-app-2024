import os

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    target = os.environ.get('TARGET', 'World')
    return 'Hello {}!\n'.format(target)
@app.route('/contactus')
def contact():
    return 'Here is my contact!!'
@app.route('/aboutus')
def aboutus():
    return 'We are an analytics firm working since 2024'

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))