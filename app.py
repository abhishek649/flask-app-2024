import os

from flask import Flask, render_template,request,redirect, url_for # type: ignore
from google.cloud import storage
from werkzeug.utils import secure_filename # type: ignore
from utils.sendpubsub import send_message
import logging

app = Flask(__name__)
cwd = os.getcwd()
#print(cwd)
CONFIG_FOLDER = cwd+"/config/"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "config/creds.json"
app.config['CONFIG_FOLDER'] = CONFIG_FOLDER
app.config['UPLOAD_FOLDER'] = cwd+"/uploads/"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg','pdf','xlsx','csv'])
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
@app.route('/processfile',methods=['GET'])
def processfile():
    if request.method == 'GET':
        msg=request.args.get('msg')
    return render_template("fileupload.html",msg=msg)
@app.route('/upload_document_files', methods=['GET', 'POST'])
def upload_document_files():
    try:
        pdf_file=''
        if request.method == 'POST':
            pdf_file=request.files['pdf-file']
            if pdf_file.filename == '':
                msg="File name should not be blank"
                return redirect(url_for('processfile',msg=msg))
            else:
                project_id = 'todo-219011'
                bucket_name = 'flask_app'
                storage_client = storage.Client()
                bucket = storage_client.bucket(bucket_name)
                bucket.location = 'us'
                bucket.create(project=project_id,location="us")
                if pdf_file and allowed_file(pdf_file.filename):
                    filename = secure_filename(pdf_file.filename)
                    #filename = pdf_file.filename
                    print(pdf_file.filename)
                    pdf_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                else:
                    msg="This type of file is not allowed to upload"
                    return redirect(url_for('processfile',msg=msg))
                #blob = bucket.blob("uploads/"+filename)
                #with open('uploads/'+filename, 'rb') as file:
                    #blob.upload_from_file(file)
                msg="File has been uploaded successfully!"
                return redirect(url_for('processfile',msg=msg))
               
    except Exception as e:
        print("error to upload file",e)
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))