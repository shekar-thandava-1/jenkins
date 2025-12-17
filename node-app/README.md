# Jenkins Project

This project provides a comprehensive example of a CI/CD pipeline for a Node.js web application. It utilizes Jenkins for automation, Docker for containerization, and Kubernetes for deployment and orchestration.

### File-by-File Breakdown

#### **`app.js`**
This file contains the core application logic.

*   **Framework**: It uses [Express.js](https://expressjs.com/), a minimal and flexible Node.js web application framework.
*   **Functionality**: It defines a single API endpoint at `/hello`. When a `GET` request is made to this endpoint, the server responds with the plain text message, "Hello, World! Welcome!!".
*   **Port Configuration**: The application listens on the port defined by the environment variable `PORT`, defaulting to `3000` if the variable is not set. This makes the port configurable, which is essential for containerized environments.

---

#### **`package.json`**
This is the standard Node.js manifest file.

*   **Metadata**: It defines the project's name (`node-app`), version (`1.0.0`), and main entry point (`app.js`).
*   **Dependencies**: It lists `express` as the sole production dependency.
*   **Scripts**:
    *   `"start": "node app.js"`: This is the command used to run the application in production.
    *   `"test": "echo \"Error: no test specified\" && exit 0"`: This is a placeholder test script. In a real-world scenario, this would be replaced with a command to run an actual test suite (e.g., using Jest, Mocha, or Chai). The `exit 0` ensures that the Jenkins pipeline does not fail at the test stage.

---

#### **`Dockerfile`**
This file contains the instructions for building a Docker image of the application.

*   **Base Image**: It starts from the `node:alpine` image, which is a lightweight version of Node.js, resulting in a smaller final image size.
*   **Working Directory**: It sets the working directory inside the container to `/app`.
*   **Dependency Management**: It first copies `package*.json` and runs `npm install --only=production`. This step is separated from copying the rest of the code to leverage Docker's layer caching. The dependencies layer is only rebuilt if `package.json` or `package-lock.json` changes.
*   **Code Copy**: It then copies the rest of the application source code.
*   **Port Exposure**: It declares that the application will listen on port `3000`.
*   **Startup Command**: The `CMD ["npm", "start"]` instruction specifies the default command to execute when a container is started from this image.

---

#### **`Jenkinsfile`**
This is a declarative Jenkins pipeline script that automates the entire CI/CD workflow.

*   **Agent**: `agent any` specifies that the pipeline can run on any available Jenkins agent.
*   **Tools**: It requires the `NodeJS` tool to be pre-configured in the Jenkins environment.
*   **Environment Variables**: It defines `DOCKER_HUB_CREDENTIALS_ID` and `DOCKER_HUB_REPO` for interacting with Docker Hub.
*   **Stages**:
    1.  **Checkout Github**: Clones the source code from the specified GitHub repository using stored credentials.
    2.  **Install node dependencies**: Executes `npm install` to install all dependencies defined in `package.json`.
    3.  **Test Code**: Runs the `npm test` script.
    4.  **Build Docker Image**: Builds a Docker image using the `Dockerfile` and tags it with `:latest`.
    5.  **Push Image to DockerHub**: Pushes the newly built image to the specified Docker Hub repository using stored credentials.
    6.  **Deploy to Kubernetes**:
        *   It uses the `kubeconfig` step to securely connect to a Kubernetes cluster using stored credentials.
        *   It then applies the `deployment.yaml` configuration using `kubectl apply -f deployment.yaml`, which either creates or updates the application deployment.
*   **Post-build Actions**: It includes `success` and `failure` blocks to print a status message at the end of the pipeline run.

---

#### **`deployment.yaml`**
This is a Kubernetes manifest file for a Deployment object.

*   **API Version**: Uses `apps/v1`, the standard API for Deployments.
*   **Replicas**: It specifies that `2` instances (pods) of the application should be running, providing high availability and load balancing.
*   **Selector**: It uses the label `app: node-app` to identify which pods are managed by this Deployment.
*   **Pod Template**:
    *   **Labels**: Pods created from this template will have the label `app: node-app`.
    *   **Container Spec**: It defines a single container named `node-app` running the `shekthan5/shekthan5-app:latest` image from Docker Hub.
    *   **Container Port**: It specifies that the container listens on port `3000`.
    *   **Image Pull Secrets**: It references a secret named `dockerhub-secret`, which contains the credentials needed to pull the private Docker image.

---

#### **`service.yaml`**
This is a Kubernetes manifest file for a Service object, which exposes the application.

*   **API Version**: Uses the core `v1` API.
*   **Type**: `NodePort` makes the service accessible on a static port on each node in the Kubernetes cluster. This is a simple way to expose the application for development and testing.
*   **Ports**:
    *   `port: 80`: The port that the Service itself is exposed on within the cluster's virtual network.
    *   `targetPort: 3000`: The port on the application pods that the service will forward traffic to.
*   **Selector**: It uses `app: node-app` to automatically find and load-balance traffic to all pods with that label.
