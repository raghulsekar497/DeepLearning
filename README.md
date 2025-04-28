# 🚀 YOLOv8 Object Tracking Flask App
This project is a real-time object tracking application built with Flask and YOLOv8. It allows users to upload videos or use a webcam to detect and track objects, displaying their speed and count. The application is Dockerized for easy deployment.​

# 📦 Features
Real-time object detection and tracking using YOLOv8.
Speed estimation of tracked objects.
Video upload and webcam support.
Live video streaming via Flask.
Dockerized for seamless deployment.​

# 🛠️ Prerequisites
1. Docker installed on your system.
2. Basic understanding of command-line operations.​

# 🚀 Getting Started
1. Clone the Repository
git clone https://github.com/yourusername/yolov8-object-tracking-flask.git
cd yolov8-object-tracking-flask

3. Build the Docker Image
docker build -t object-tracker-app .

4. Run the Docker Container
docker run -d -p 5000:5000 --name object-tracker object-tracker-app
The application will be accessible at http://localhost:5000.​

# 📁 Project Structure

#├── app.py
#├── detector.py
#├── logger.py
#├── requirements.txt
#├── Dockerfile
#├── static/
#│   └── uploads/
#├── templates/
#│   └── index.html
#├── data/
#│   └── videos/

#app.py: Main Flask application.
#detector.py: Contains object detection and tracking logic.
#logger.py: Handles logging functionalities.
#requirements.txt: Python dependencies.
#Dockerfile: Docker configuration.
#static/uploads/: Directory for uploaded videos.
#templates/index.html: HTML template for the frontend.
#data/videos/: Directory for sample videos.​

# 🐳 Docker Commands

Stop the Container:

  docker stop object-tracker
  
Remove the Container:

  docker rm object-tracker
  
View Container Logs:

  docker logs object-tracker
  
Access the Container's Shell:

  docker exec -it object-tracker /bin/bash
  
# 📝 License
This project is licensed under the MIT License.​
GitHub

# 🙏 Acknowledgements
Ultralytics YOLOv8 for the object detection model.
Flask for the web framework.
Docker for containerization.​


