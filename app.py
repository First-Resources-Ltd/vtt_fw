import os
import io
import json
import uuid

from flask import Flask, request, Response
from tempfile import NamedTemporaryFile
from faster_whisper import WhisperModel

server = Flask(__name__)
server.config['DEBUG'] = os.environ['DEBUG']

modelPath = os.environ['MODEL_SIZE']

@server.route('/', methods=['GET'])
def home():
    return {"success": True, "message": "Hello World from VTT FW"}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in os.environ['ALLOWED_EXTENSIONS']

@server.route('/test_mp3', methods=['GET'])
def test_mp3():
    model = WhisperModel(modelPath, compute_type="int8")
    segments, info = model.transcribe("audiobook.mp3")
    data = ''
    for segment in segments:
        data += segment.text
    del model
    return {'success': True, 'data':data}

@server.route('/test_wav', methods=['GET'])
def test_wav():
    model = WhisperModel(modelPath, compute_type="int8")
    segments, info = model.transcribe("indonesian.wav")
    data = ''
    for segment in segments:
        data += segment.text
    del model
    return {'success': True, 'data':data}

@server.route('/transcript', methods=['POST'])
def transcript():

    # 01 field, files Validation
    audio_file = request.files.get("audio_file")
    if not audio_file :
        return {
            'data': False,
            'success': False,
            'message': 'Failed transcript audio to text, Request field audio_file is requied and must be audio file .mp3 or .wav',
        }

    # 02 format validation 
    allowed = allowed_file(audio_file.filename)
    if not allowed :
        return {
            'data': False,
            'success': False,
            'message': f'Failed transcript audio to text, File Name {audio_file.filename} Not Allowed',
        }

    if not os.path.exists(os.environ['UPLOAD_FOLDER']):
        os.makedirs(os.environ['UPLOAD_FOLDER'])

    # 03 Write unique file
    tempName = str(uuid.uuid4())
    tempFile = os.path.join(os.environ['UPLOAD_FOLDER'], f'{tempName}_{audio_file.filename}')
    
    # 04 Read Open & Write audio data to file uploaded files
    audio_data = audio_file.read()
    with open(tempFile, 'wb') as f:
        f.write(audio_data)

    # 05 load model and start transcribe audio to text
    model = WhisperModel(modelPath, compute_type="int8")
    segments, info = model.transcribe(tempFile)
    data = ''
    for segment in segments:
        data += segment.text

    # 06 Remove uploaded file
    if os.path.isfile(tempFile):
        os.remove(tempFile)
    
    del model

    return {'success': True, 'data':data}

@server.route('/clear_uploaded_files', methods=['GET'])
def clear_uploaded_files():
    paths = os.environ['UPLOAD_FOLDER']
    lenFile = 0
    if os.path.exists(paths):
        for f in os.listdir(paths):
            os.remove(os.path.join(paths, f))
            lenFile += 1

    removedStr = str(lenFile)
    return {'message' : 'Removed ' + removedStr + ' Files'}
