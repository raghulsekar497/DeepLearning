from flask import Flask, render_template, Response, request, redirect, url_for, jsonify
import cv2
import os
from werkzeug.utils import secure_filename
from detector import process_frame
import os
from logger import create_logger

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

video_source = None
use_camera = False

object_counts = {"total": 0}
track_ids_seen = set()
speed_info = {}
prev_positions = {}
prev_times = {}


def get_available_videos():
    video_files = []
    folders = [('static/uploads', 'static/uploads'), ('data/videos', 'data/videos')]
    for full_path, web_path in folders:
        if os.path.exists(full_path):
            for file in os.listdir(full_path):
                if file.endswith(('.webm', '.mp4')):
                    video_files.append(f"{web_path}/{file}")
    return video_files


def generate_frames():
    global video_source, use_camera, object_counts, track_ids_seen, speed_info
    cap = cv2.VideoCapture(0 if use_camera else video_source)

    # Identify video type and name for logging
    video_type = "camera" if use_camera else (
        "uploaded" if video_source and "uploads" in str(video_source) else "selected"
    )
    video_name = "Live Camera" if use_camera else os.path.basename(str(video_source))
    logger = create_logger(video_type, video_name)

    while True:
        success, frame = cap.read()
        if not success:
            if not use_camera:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            else:
                break

        frame = cv2.resize(frame, (720, 480))
        annotated = process_frame(
            frame,
            object_counts,
            speed_info,
            track_ids_seen,
            logger=logger  # <- Pass logger to your frame processor
        )

        ret, buffer = cv2.imencode('.jpg', annotated)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')


@app.route('/')
def index():
    videos = get_available_videos()  # however you collect videos from /data and /uploads
    return render_template('index.html', videos=videos, object_counts={'total': 0})

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/object_count')
def object_count():
    return jsonify(object_counts)


@app.route('/upload', methods=['POST'])
def upload_video():
    global video_source, use_camera, object_counts, track_ids_seen, speed_info

    file = request.files['video']
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        video_source = filepath
        use_camera = False
        object_counts["total"] = 0
        track_ids_seen.clear()
        return redirect(url_for('index'))


@app.route('/camera', methods=['POST'])
def camera():
    global video_source, use_camera
    global object_counts, track_ids_seen, speed_info, prev_positions, prev_times

    use_camera = True
    video_source = 0  # Webcam index (0 is default)

    # Reset tracking state
    object_counts = {"total": 0}
    track_ids_seen = set()
    speed_info = {}
    prev_positions = {}
    prev_times = {}

    return redirect(url_for('index'))

@app.route('/select_video', methods=['POST'])
def select_video():
    global video_source, use_camera
    global object_counts, track_ids_seen, speed_info, prev_positions, prev_times

    selected = request.form.get('selected_video')

    if selected:
        video_source = selected
        use_camera = False

        # Safe reset
        object_counts = {"total": 0}
        track_ids_seen = set()
        speed_info = {}
        prev_positions = {}
        prev_times = {}

    return redirect(url_for('index'))


if __name__ == '__main__':
    os.makedirs('static/uploads', exist_ok=True)
    os.makedirs('data/videos', exist_ok=True)
    app.run(debug=True)

