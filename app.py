import os

from flask import Flask, render_template # type: ignore
from google.cloud import storage
from utils.sendpubsub import send_message

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("index.html")
@app.route('/contactus')
def contact():
    return render_template("contact.html")
@app.route('/aboutus')
def aboutus():
    return render_template("aboutus.html")
@app.route('/callpubsub')
def pubsub():
    try:
        project_id = "challenge-296807"
        topic_id = "pubsub-to-bq"
        res=send_message(project_id,topic_id)
        return res
    except Exception as e:
        print("eroor ocured",e)


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))