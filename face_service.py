import json
import cv2
import numpy as np
import traceback
import base64
from flask import Flask, request, jsonify
app = Flask(__name__)
from retinaface_api import RetinafaceApi


@app.route("/")
def index():
    result = {
        'code' : '200',
        'data': 'Hello, world'
    }
    return json.dumps(result)

@app.route('/regist', methods=['POST'])
def regist():
    try:
        form = request.form
        base64Data = form.get('img')
        # base64Data = request.args.get('img')
        img = base64.b64decode(base64Data)
         # file就是接收file对象
        # file = request.files.get('file')
        retinaface.save_face(img)
        face = retinaface.encode_face_dataset()
        if face != 0:
            retinaface.load_face()
            return jsonify({'code': 200, 'success': True, 'face': face})
        else:    
            return jsonify({'code': 200, 'success': False, 'face': face})
    except Exception:
        print(traceback.print_exc())
        return jsonify({'code': 500})

@app.route('/face', methods=['POST'])
def face():
    try:
        # json = request.json
        # base64Data = json['img']
        form = request.form
        base64Data = form.get('img')
        # base64Data = request.args.get('img')
        img = base64.b64decode(base64Data)
        image = cv2.imdecode(np.frombuffer(img, np.uint8), cv2.IMREAD_COLOR)
        image   = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        face, valid = retinaface.detect_image_2_name(image)
        return jsonify({'code': 200, 'success': valid, 'face': face})
    except Exception as e:
        print(traceback.print_exc())
        return jsonify({'code': 500})

''' @app.route('/face', methods=['POST'])
def face():
    try:
         # file就是接收file对象
        file = request.files.get('file')
        img = file.read()
        image = cv2.imdecode(np.frombuffer(img, np.uint8), cv2.IMREAD_COLOR)
        image   = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        valid = retinaface.detect_image_2_name(image)
        return jsonify({'status': 200, 'valid': valid})
    except Exception as e:
        print(traceback.print_exc())
        return jsonify({'status': 500}) '''

if __name__ == '__main__':
    retinaface = RetinafaceApi()
    app.run(host='0.0.0.0')    