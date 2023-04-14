import os
import uuid
import json

from fastapi import FastAPI, UploadFile, File, Response
from faster_whisper import WhisperModel

app = FastAPI()

MODEL_SIZE = 'small'
UPLOAD_FOLDER = 'uploaded_files'
ALLOWED_EXTENSIONS = {'wav','mp3'}

@app.get("/")
def home():
    return {"success": True, "message": "Hello World from VTT FW"}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.get('/test_mp3')
def test_mp3():
    model_size = "small"
    model = WhisperModel(model_size, compute_type="int8")
    segments, info = model.transcribe("audiobook.mp3")
    data = ''
    for segment in segments:
        data += segment.text
    del model
    return {'success': True, 'data':data}

@app.get('/test_wav')
def test_wav():
    model_size = "small"
    model = WhisperModel(model_size, compute_type="int8")
    segments, info = model.transcribe("indonesian.wav")
    data = ''
    for segment in segments:
        data += segment.text
    del model
    return {'success': True, 'data':data}

@app.post('/transcript')
def transcript(audio_file: UploadFile = File(...)):

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
     
    # 01 field, files Validation
    if not audio_file :
        json_data = json.dumps({
            'data': False,
            'success': False,
            'message': 'Failed transcript audio to text, Request field audio_file is requied and must be audio file .mp3 or .wav',
        })
        response = Response(json_data, status_code=422)
        response.headers['Content-Type'] = 'application/json'
        return response

    # 02 format validation 
    allowed = allowed_file(audio_file.filename)
    if not allowed :
        json_data = json.dumps({
            'data': False,
            'success': False,
            'message': f'Failed transcript audio to text, File Name {audio_file.filename} Not Allowed',
        })
        response = Response(json_data, status_code=422)
        response.headers['Content-Type'] = 'application/json'
        return response

    # 03 tempFile
    tempFile = os.path.join(UPLOAD_FOLDER, f'{str(uuid.uuid4())}_{audio_file.filename}')

    # 04 Read Open & Write audio data to file uploaded files
    audio_data = audio_file.file.read()
    with open(tempFile, 'wb') as f:
        f.write(audio_data)

    # 05 load model and start transcribe audio to text
    model = WhisperModel(MODEL_SIZE, compute_type="auto", device="auto")
    segments, info = model.transcribe(tempFile)
    data = ''
    for segment in segments:
        data += segment.text

    # 06 Remove uploaded file
    if os.path.isfile(tempFile):
        os.remove(tempFile)
    
    del model

    return {'success': True, 'data':data}

@app.get('/clear_uploaded_files')
def clear_uploaded_files():
    paths = UPLOAD_FOLDER
    lenFile = 0
    for f in os.listdir(paths):
        os.remove(os.path.join(paths, f))
        lenFile += 1

    removedStr = str(lenFile)
    return {'message' : 'Removed ' + removedStr + ' Files'}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("app:app", host='0.0.0.0', port=5000, reload=True)
