from flask import Flask, jsonify
from werkzeug import secure_filename
import config as cfg
import boto3
from boto3.s3.transer import S3Transfer

AWS_BUCKET = "test-upload"
app = Flask("python_s3")

@app.route("/upload", methods=['POST'])
def upload():
    """
    Upload files
    ---
    tags:
        - Files
    consumes: "multipart/form-data"
    parameters:
        -   name: files[]
            in: formData
            required: true
            paramType: body
            dataType: file
            type: file
        -   name: files[]
            in: formData
            required: false
            paramType: body
            dataType: file
            type: file

    responses:
        200:
            description: Returns album_id after upload
        401:
            description: Unauthorized
        400:
            description: Bad Request
        500:
            description: Server Internal error
    """
    uploaded_files = request.files.getlist("files[]")
    for upload_file in uploaded_files:
        if upload_file and allowed_file(file.filename):
            filename = secure_filename(upload_file.filename)

            username = app.current_user['username']
            dir_name = 'uploads/'
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)

            file_path = os.path.join(dir_name, filename)

            app.logger.info("Saving file: %s", file_path)
            # save to local 
            upload_file.save(file_path)
            transfer = S3Transfer(boto3.client('s3', cfg.AWS_REGION, aws_access_key_id=cfg.AWS_APP_ID,
                aws_secret_access_key=cfg.AWS_APP_SECRET))

            transfer.upload_file(file_path, AWS_BUCKET, file_path)

    return jsonify({'test': 'test'})

@app.route("/download", methods=['POST'])
def download():
    return jsonify({'test': 'test'})

def allowed_file(filename):
    return '.' in filename and \
       filename.rsplit('.', 1)[1] in cfg.ALLOWED_EXTENSIONS

if (__name__ == "__main__" ):
    app.run()

