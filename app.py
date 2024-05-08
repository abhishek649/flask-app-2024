import os

from flask import Flask, render_template # type: ignore
from google.cloud import pubsub_v1

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
    publisher = pubsub_v1.PublisherClient()
    topic_name = 'projects/{project_id}/topics/{topic}'.format(
    project_id='challenge-296807',
    topic='pubsub-to-bq',  # Set this to something appropriate.
    )
    publisher.create_topic(name=topic_name)
    future = publisher.publish(topic_name, b'My first message!', spam='eggs')
    result=future.result()
    return result


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))