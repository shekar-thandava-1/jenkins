# Python Hello World Application

This project is a simple "Hello, World!" web application created using the Python [Flask](https://flask.palletsprojects.com/) framework. It is set up to be built, tested, and deployed using a CI/CD pipeline.

### Files

*   **`app.py`**: The main application file. It uses Flask to create a web server with a single endpoint, `/hello`, which returns a "Hello, World!" message.
*   **`requirements.txt`**: The standard Python dependency file, which lists the necessary packages for this project (i.e., Flask).
*   **`Dockerfile`**: Contains instructions to build a Docker container for the application. It uses a lightweight Python base image, installs dependencies, and configures the container to run the Flask app.
*   **`Jenkinsfile`**: A Jenkins pipeline script designed for this Python application. It automates the process of checking out the code, installing dependencies, running tests (placeholder), building a Docker image, and pushing it to a container registry.
