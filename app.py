import os
import io
import json
import uuid
import gc

from flask import Flask, request, Response
from tempfile import NamedTemporaryFile
from faster_whisper import WhisperModel
from multiprocessing import Process, Manager, set_start_method

set_start_method("fork")  # Sets the start method for child processes
gc.enable()
gc.collect()
server = Flask(__name__)
server.config['DEBUG'] = os.environ['DEBUG']

modelPath = os.environ['MODEL_PATH']

@server.route('/', methods=['GET'])
def home():
    return {"success": True, "message": "Hello World from VTT FW"}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in os.environ['ALLOWED_EXTENSIONS']

@server.route('/test_mp3', methods=['GET'])
def test_mp3():
    tempFile = "audiobook.mp3"
    # 05 Set up a process manager
    process_manager = Manager()
    shared_data = process_manager.dict()
    
    # 06 Create child process for whisper execution
    p = Process(target=_do_transcribe, args=(shared_data, "result", tempFile))
    
    p.start()      # run child process
    p.join()       # wait for the process to complete
    p.terminate()  # terminate the process (optional - should happen automatically)

    # 07 Remove uploaded file
    if os.path.isfile(tempFile):
        os.remove(tempFile)

    # 08 Get transcription from shared data and delete
    data = shared_data["result"]
    return {'success': True, 'data':data}

@server.route('/test_wav', methods=['GET'])
def test_wav():
    tempFile = "indonesian.wav"
    # 05 Set up a process manager
    process_manager = Manager()
    shared_data = process_manager.dict()
    
    # 06 Create child process for whisper execution
    p = Process(target=_do_transcribe, args=(shared_data, "result", tempFile))
    
    p.start()      # run child process
    p.join()       # wait for the process to complete
    p.terminate()  # terminate the process (optional - should happen automatically)

    # 07 Remove uploaded file
    if os.path.isfile(tempFile):
        os.remove(tempFile)

    # 08 Get transcription from shared data and delete
    data = shared_data["result"]
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
    # audio_file.save(tempFile)
    audio_data = audio_file.read()
    with open(tempFile, 'wb') as f:
        f.write(audio_data)
        f.close()
    # 05 Set up a process manager
    process_manager = Manager()
    shared_data = process_manager.dict()
    
    # 06 Create child process for whisper execution
    p = Process(target=_do_transcribe, args=(shared_data, "result", tempFile))
    
    p.start()      # run child process
    p.join()       # wait for the process to complete
    p.terminate()  # terminate the process (optional - should happen automatically)

    # 07 Remove uploaded file
    if os.path.isfile(tempFile):
        os.remove(tempFile)

    # 08 Get transcription from shared data and delete
    data = shared_data["result"]
    del audio_file
    del audio_data
    del tempFile
    del shared_data
    del process_manager

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

@server.route('/transcript_new', methods=['POST'])
def transcript_new():

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
    # audio_file.save(tempFile)
    audio_data = audio_file.read()
    with open(tempFile, 'wb') as f:
        f.write(audio_data)
        f.close()
    # 05 Set up a process manager
    process_manager = Manager()
    shared_data = process_manager.dict()
    
    # 06 Create child process for whisper execution
    p = Process(target=_do_transcribe, args=(shared_data, "result", tempFile))
    
    p.start()      # run child process
    p.join()       # wait for the process to complete
    p.terminate()  # terminate the process (optional - should happen automatically)

    # 07 Remove uploaded file
    if os.path.isfile(tempFile):
        os.remove(tempFile)

    # 08 Get transcription from shared data and delete
    data = shared_data["result"]
    del audio_file
    del audio_data
    del tempFile
    del shared_data
    del process_manager

    return {'success': True, 'data':data}

def _do_transcribe(shared_data: dict, rid: str, tempFile: str):
    try:
        model = WhisperModel(modelPath, compute_type="int8")
        segments, info = model.transcribe(tempFile, beam_size=1)
        data = ''
        for segment in segments:
            data += segment.text

        # Store data in shared data
        shared_data[rid] = data
    except Exception as e:
        # Handle the error, if needed
        print(f"Error: {e}")
        shared_data[rid] = None  # Store None in the shared data to indicate an error
    finally:
        # Release model resources
        del model
        del info
