
# 🚀 YOLOv8 Object Tracking Flask App

A real-time object tracking application built with **Flask** and **YOLOv8**.  
It allows users to upload videos or use a webcam to detect and track objects, displaying their speed and count.  
The application is **Dockerized** for easy deployment.

---

# 📦 Features

- 🔍 Real-time object detection and tracking using YOLOv8.
- 🚗 Speed estimation of tracked objects.
- 🎥 Video upload and webcam support.
- 🌐 Live video streaming via Flask.
- 🐳 Dockerized for seamless deployment.

---

# 🛠️ Prerequisites

- Docker installed on your system.
- Basic understanding of command-line operations.

---

# 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/yolov8-object-tracking-flask.git
cd yolov8-object-tracking-flask
```

### 2. Build the Docker Image
```bash
docker build -t object-tracker-app .
```

### 3. Run the Docker Container
```bash
docker run -d -p 5000:5000 --name object-tracker object-tracker-app
```

The application will be accessible at:  
👉 [http://localhost:5000](http://localhost:5000)

---

# 📁 Project Structure

```
├── app.py                 # Main Flask application
├── detector.py            # Object detection and tracking logic
├── logger.py              # Logging functionalities
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker configuration
├── static/
│   ├── uploads/           # Directory for uploaded videos
│   ├── logs/              # Directory for logs
├── templates/
│   └── index.html         # Frontend HTML template
├── data/
│   └── videos/            # Directory for sample videos
```

---

# 🐳 Useful Docker Commands

### Stop the Container:
```bash
docker stop object-tracker
```

### Remove the Container:
```bash
docker rm object-tracker
```

### View Container Logs:
```bash
docker logs object-tracker
```

### Access the Container's Shell:
```bash
docker exec -it object-tracker /bin/bash
```

---

# 📝 License

This project is licensed under the [MIT License](LICENSE).

---

# 🙏 Acknowledgements

- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics) for the object detection model.
- [Flask](https://flask.palletsprojects.com/) for the web framework.
- [Docker](https://www.docker.com/) for containerization.
