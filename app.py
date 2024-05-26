import os

from flask import Flask, render_template,request # type: ignore
from google.cloud import storage
from utils.sendpubsub import send_message
import logging

app = Flask(__name__)
cwd = os.getcwd()
bucket_name='myawesomeapp_upload'
destination_blob_name='myawsomeapp.pdf'
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
@app.route('/processfile')
def processfile():
    return render_template("fileupload.html")
@app.route('/upload_document_files', methods=['GET', 'POST'])
def upload_document_files():
    try:
        pdf_file=''
        if request.method == 'POST':
            pdf_file=request.files['pdf-file']
            if pdf_file.filename == '':
                return render_template("fileupload.html")
            else:
                storage_client = storage.Client()
                bucket = storage_client.bucket(bucket_name)
                blob = bucket.blob(destination_blob_name)
                generation_match_precondition = 0
                blob.upload_from_filename(pdf_file, if_generation_match=generation_match_precondition)

            logging.info(f"File {pdf_file} uploaded to {destination_blob_name}.")

    except Exception as e:
        logging.info("error to upload file",e)



if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))