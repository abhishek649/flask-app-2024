import os

from flask import Flask, render_template,request,redirect, url_for # type: ignore
from google.cloud import storage

from utils.sendpubsub import send_message
import logging

app = Flask(__name__)
cwd = os.getcwd()
#print(cwd)
CONFIG_FOLDER = cwd+"/config/"
app.config['CONFIG_FOLDER'] = CONFIG_FOLDER
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
                storage_client = storage.Client.from_service_account_json(app.config['CONFIG_FOLDER']+'/creds.json')
                bucket = storage_client.get_bucket(bucket_name)
                blob = bucket.blob(destination_blob_name)
                blob.upload_from_filename(pdf_file)
                
                

            logging.info(f"File {pdf_file} uploaded to {destination_blob_name}.")
            msg = 'File upload success !'
            return render_template('fileupload.html', msg = msg)
            

    except Exception as e:
        logging.info("error to upload file",e)



if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))