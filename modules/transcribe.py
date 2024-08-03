from flask import Blueprint, request, jsonify, current_app, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import whisper
import torch
from send_email import send_email  # 导入发送邮件模块
from summarize import summarize_text  # 导入新的摘要模块
from datetime import datetime

transcribe_bp = Blueprint('transcribe', __name__)
model = whisper.load_model("base")

queue = []
processing = False

@transcribe_bp.route('/gpus', methods=['GET'])
def get_gpus():
    if torch.cuda.is_available():
        gpus = [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())]
    else:
        gpus = ["CPU"]
    return jsonify(gpus)

@transcribe_bp.route('/upload', methods=['POST'])
def upload_file():
    global processing
    client_ip = request.remote_addr
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    format = request.form.get('format', 'text')
    send_email_flag = request.form.get('send_email', 'false').lower() == 'true'
    email = request.form.get('email')

    # 生成唯一文件名
    filename = secure_filename(f"{client_ip}_{current_time}_{file.filename}")
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

    # 检查是否正在处理其他文件
    if processing or len(os.listdir(current_app.config['UPLOAD_FOLDER'])) > 0:
        return jsonify({'message': '目前正在處理其他文件，請稍候'}), 202

    file.save(file_path)
    processing = True
    return process_file(file_path, format, send_email_flag, email, filename)

def process_file(file_path, format, send_email_flag, email, filename):
    global processing
    try:
        if not file_path.endswith('.mp3'):
            mp3_file_path = os.path.splitext(file_path)[0] + '.mp3'
            command = f"ffmpeg -i \"{file_path}\" \"{mp3_file_path}\""
            os.system(command)
            os.remove(file_path)
            file_path = mp3_file_path

        result = model.transcribe(file_path)
        result_filename = generate_result_file(result, format, filename)
        summary = summarize_text(result['text'])  # 调用摘要函数
        os.remove(file_path)

        if send_email_flag and email:
            result_file_path = os.path.join(current_app.config['RESULT_FOLDER'], result_filename)
            send_email(email, result_file_path, summary)

        response = {
            'download_url': url_for('transcribe.result_file', filename=result_filename),
            'view_url': url_for('transcribe.result_file', filename=result_filename, _external=True),
            'filename': result_filename,
            'summary': summary  # 返回摘要
        }
    except Exception as e:
        processing = False
        return jsonify({'error': str(e)}), 500

    processing = False

    # 处理队列中的下一个文件
    if queue:
        next_file_info = queue.pop(0)
        next_file_path = next_file_info[0]
        return process_file(next_file_path, *next_file_info[1:])

    return jsonify(response)

def generate_result_file(result, format, original_filename):
    base_filename = os.path.splitext(original_filename)[0]
    result_folder = current_app.config['RESULT_FOLDER']
    if format == 'text':
        result_filename = f"{base_filename}.txt"
        with open(os.path.join(result_folder, result_filename), 'w', encoding='utf-8') as f:
            f.write(result['text'])
    elif format == 'text-timestamp':
        result_filename = f"{base_filename}_timestamps.txt"
        with open(os.path.join(result_folder, result_filename), 'w', encoding='utf-8') as f:
            for segment in result['segments']:
                start_time = format_timestamp(segment['start'])
                end_time = format_timestamp(segment['end'])
                f.write(f"{start_time} --> {end_time}\n{segment['text']}\n\n")
    elif format == 'srt':
        result_filename = f"{base_filename}.srt"
        with open(os.path.join(result_folder, result_filename), 'w', encoding='utf-8') as f:
            for i, segment in enumerate(result['segments']):
                start_time = format_timestamp(segment['start'])
                end_time = format_timestamp(segment['end'])
                f.write(f"{i+1}\n{start_time} --> {end_time}\n{segment['text']}\n\n")
    return result_filename

def format_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:06.3f}".replace('.', ',')

@transcribe_bp.route('/results/<filename>')
def result_file(filename):
    return send_from_directory(current_app.config['RESULT_FOLDER'], filename)
