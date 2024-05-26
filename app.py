import os

from flask import Flask, render_template,request,redirect, url_for # type: ignore
from google.cloud import storage
from oauth2client.service_account import ServiceAccountCredentials
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
                credentials_dict = {
                'type': 'service_account',
                'client_id': "113264080047417106622",
                'client_email': "challenge-296807@appspot.gserviceaccount.com",
                'private_key_id': "3611371b0b98a32c1bfceca64392646b157f5c9d",
                'private_key': "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQC56acATPMIoHYw\nb2eG9Hq6DYz04XjfJn+2WlGANIyFzsS/Jy5MuQRiOEkHVzkKgPwQKYIOAjxjz1tu\ny7gbA/VAJBkIsk59894597suhtnAHOCP5VHwKLCtHrlmHmRTqVh5p/8/lPFPaNZb\nbC7GnvV11ST/vTa5PVq0rgqXd1oMz/xwvhss+j5XXtFkZ4q7RaJc/cgTdGgsRLB6\nLBqUILL5nlxUvSgarLSdi4AN6YhOmWeWDVeCVbKg2XZlKaeCIClKCKyxhhzTTR4x\n97z7TIjEtQkc8IUkYziQsjfWCSdIzRo/+RnmlpYM7w4T4stWykSlBA7ZEqBKBi2E\ntYxazNQVAgMBAAECggEAF/5JqUZFD1X2KuYVzFr9A8n/6RK4UMRdMyGQ5yThBdvb\nlHfwB8LRCAQPmLzvBaYD4eoZeMldFdyLBk+QYRwvqKl/+ZlZe/PfOEf6hlStAZg4\nexmza3U06ALRFpbRh+KRIpJF5OTKB9+V2pKprsSRFTX+4mp/B4UdkbfscgPbQU/W\nCjYvkSaZXMteh7y0Do+IqZDfnIcjfYnf0ab9VKJhJYLvIe77adfNzazp326yOpQ/\naPuGO/O2RulnI+pkZGh82Ktgc6qEqBdEFISjMZhE9jb4kY7WQDW7Sao4qb1UPwSR\nzMtAYOVRquamE06U9LN4GSn2Yy3fk9NfJeBvVKjQOQKBgQDcamcV5MuNbMuEyCFc\nlUzOUaVN1JP5r3q4lFDcDS+d2byM6KdEwUaNGU/f1lD8l8Vo+TTBbMfd3zMiRZ+h\nDkA8tptKNGSwhbgRmMyjrxNRS3mDTDxe/08YggQ2xhL9wj68rdW3T8rnh+wJOKfx\nZsN4/tPCEXakGX8RAdN7+5ypGwKBgQDX7UWX6pdW64WUEW5xHyTcPmPiBQsrF5g6\ngANZS3H3hsnCMw8BxeZ/fSDxoB8fviNqgh9A7Zpa0j7vLCT75Tqgkfe7gNq1iAAR\noROexOKDu3WNLzdFtk0acicQIvg4hxOENgiX6leexiMiGIgGVL4wyHMFvQIF8diP\nq6Kl29L6jwKBgQCcodBXspskCSgnV8C9dit6gnKh+GqfiKABAwTjG0u3NL/UspAL\nP/3Ozyn/uuEaXxAeJNnkilUNyksgE7H4VZQ4kNuRw+G5v4yqlJb3yrZDkwrqzwYn\ny+59UAeGlQNx6NOEaVPyTHW4StLlSqmt1oUaOpxo0NgqjSPLBi0vcgJF+QKBgQCV\ngUrbaenJnB+MKxmeJ6M8/9Hmz/kwqBCWCMbI0A0kBuaxmOq+Hol/ImNqCaUjNGKP\nP3NmYF2snsBGl/kvlEMopIi0Af7tDDKIAlB0cPwpm+VDkTqjARuXwQw9Bwl5EkW4\nGDWRAggS/jubQwMD5y8c1d2WTo0VEqQQrhVa477MDwKBgQC84mt/jbiisGFeexI0\nnT/NV5T5cKwdM+hKIZRufi3Lv45nmZsaYYnvbYCQr8fccv/0dC82N77hv7Qv1Hr+\nCSOYKC2BcpTFtxV6Vuxsvtvas3zfvSTWrgWbWtcLf4f+mAmqOmKkcWvx2UmO1eet\nlCMq1Ck4s1SdDTLBj8RKt2LYiA==\n-----END PRIVATE KEY-----\n",
                }
                credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict)
                client = storage.Client(credentials=credentials, project='challenge')
                bucket = client.get_bucket('myawesomeapp_upload')
                blob = bucket.blob('pdf_file')
                blob.upload_from_filename('pdf_file')
                return blob.public_url
               
    except Exception as e:
        logging.info("error to upload file",e)



if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))