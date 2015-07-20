from flask import Flask, jsonify
import config as cfg
import boto3
from boto3.s3.transer import S3Transfer

app = Flask("python_s3")

@app.route("/upload", methods=['POST'])
def upload():
    return jsonify({'test': 'test'})

@app.route("/download", methods=['POST'])
def download():
    return jsonify({'test': 'test'})

if (__name__ == "__main__" ):
    app.run()
