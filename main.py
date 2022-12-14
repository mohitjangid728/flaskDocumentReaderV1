import os
import urllib.request
from app import app
from flask import Flask, request, redirect, jsonify
from werkzeug.utils import secure_filename
import aspose.words as aw
import codecs

ALLOWED_EXTENSIONS = set(['docx'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def home_page():
	return {'Error message: ' : 'You cannot access without authentication...'}

@app.route('/file-upload', methods=['POST'])
def upload_file():
	# check if the post request has the file part
    if request.args['auth'] == 'qtgaykvt857zw8v9cq5o':
        if 'file' not in request.files:
            resp = jsonify({'message' : 'No file part in the request'})
            resp.status_code = 400
            return resp
        file = request.files['file']
        if file.filename == '':
            resp = jsonify({'message' : 'No file selected for uploading'})
            resp.status_code = 400
            return resp
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'hello.docx'))
            try:
                doc = aw.Document("./uploads/hello.docx")
                doc.save("./uploads/Output.html")
                file = codecs.open("./uploads/Output.html", "r", "utf-8")
                output = file.read()
                file.close()
                resp = output
                # resp.status_code = 201
                return resp
            except Exception:
                resp = jsonify({'message' : 'There was an error reading the file'})
                resp.status_code = 201
                return resp
            finally:
                file.close()
            resp = jsonify({'message' : 'File successfully uploaded'})
            resp.status_code = 201
            return resp
        else:
            resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
            resp.status_code = 400
            return resp
    else:
        resp = jsonify({'message' : 'Invalid API Key...'})
        resp.status_code = 201
        return resp

if __name__ == "__main__":
    app.run()
