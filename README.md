[taskpulse_api_readme.md](https://github.com/user-attachments/files/35074464/taskpulse_api_readme.md)
# TaskPulse API — End-to-End DevOps CI/CD & Kubernetes Pipeline

**TaskPulse API** is a lightweight Python (Flask) REST microservice for task management, engineered to demonstrate an automated end-to-end DevOps delivery pipeline (`Code → Build & Test → Configure → Containerize → Deploy & Scale`).

🔗 **Repository:** [https://github.com/kanishk-raj-t/devops-pipeline](https://github.com/kanishk-raj-t/devops-pipeline)

---

## Architecture Overview

1. **Source Control (Git & GitHub):** Feature-branch workflow (`feature/health-endpoint` merged into `main`) with clean artifact exclusion.
2. **Continuous Integration (Jenkins & pytest):** Declarative `Jenkinsfile` triggered automatically via SCM polling (`* * * * *`) that creates an isolated Python virtual environment, runs automated `pytest` unit tests, packages `todo-api-build.tar.gz`, and archives the build artifact.
3. **Configuration Management (Ansible):** Custom `todo_app` role created with `ansible-galaxy`, utilizing variables, handlers, and an inventory to provision the Python runtime, deploy the Jenkins build artifact, and manage the background service.
4. **Containerization (Docker):** Lightweight `python:3.11-slim` container image (`todo-api:v1`) built directly from the verified Jenkins build artifact.
5. **Container Orchestration (Kubernetes / Minikube):** Deployed with 3 replicas behind a `NodePort` Service (`todo-api-service`), tested with horizontal replica scaling (3 → 5 → 3 pods), and configured dynamically using a Kubernetes `ConfigMap`.

---

## Tech Stack

* **Application & Testing:** Python 3.11, Flask 3.0.3, pytest 8.3.4
* **Version Control & CI:** Git, GitHub, Jenkins LTS
* **Configuration & Containers:** Ansible, Docker
* **Orchestration:** Kubernetes (Minikube, `kubectl`)

---

## Project Structure

```text
devops-pipeline/
├── app.py                          # Flask REST API application
├── test_app.py                     # Automated pytest unit test suite
├── requirements.txt                # Python dependencies
├── Jenkinsfile                     # Jenkins CI pipeline definition
├── Dockerfile                      # Container image definition
├── repo_link.txt                   # Submission repository reference
├── ansible/
│   ├── inventory                   # Target host inventory
│   ├── playbook.yml                # Main Ansible playbook
│   └── roles/
│       └── todo_app/
│           ├── defaults/main.yml   # Role variables (app_port, app_dir)
│           ├── handlers/main.yml   # Service restart handler
│           └── tasks/main.yml      # Provisioning & deployment tasks
└── k8s/
    ├── configmap.yaml              # Externalized environment settings (PORT=5050)
    ├── deployment.yaml             # Kubernetes Deployment (3 replicas)
    └── service.yaml                # Kubernetes NodePort Service
```

---

## API Endpoints

| Method | Endpoint | Description | Sample Response |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | Root status check | `{"message": "Todo API is running"}` |
| `GET` | `/health` | Container & CI health check | `{"status": "healthy"}` |
| `GET` | `/todos` | Retrieve all tasks | `{"todos": [{"id": 1, "task": "Initialize DevOps pipeline", "done": true}]}` |
| `POST` | `/todos` | Create a new task (`{"task": "..."}`) | `{"id": 2, "task": "...", "done": false}` |

---

## Quick Start & Usage

### 1. Run Locally & Execute Unit Tests
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run automated pytest suite
pytest -v

# Start the API server (defaults to port 5000)
python app.py
```

### 2. Automated Server Configuration with Ansible
```bash
# Start target container
docker run -d --name ansible-target -p 5001:5000 ubuntu:22.04 sleep infinity

# Run Ansible playbook
cd ansible
ansible-playbook -i inventory playbook.yml

# Verify service
curl http://localhost:5001/todos
```

### 3. Build & Test Docker Image
```bash
docker build -t todo-api:v1 .
docker run -d --name todo-docker-test -p 5002:5000 todo-api:v1
curl http://localhost:5002/health
docker rm -f todo-docker-test
```

### 4. Deploy & Scale on Kubernetes (Minikube)
```bash
minikube start --driver=docker
minikube image load todo-api:v1

# Apply ConfigMap, Deployment, and Service
kubectl apply -f k8s/

# Verify resources
kubectl get configmap todo-api-config -o yaml
kubectl get pods
kubectl get svc

# Scale replicas
kubectl scale deployment todo-api-deployment --replicas=5
kubectl scale deployment todo-api-deployment --replicas=3

# Forward port and test live endpoint
kubectl port-forward service/todo-api-service 8085:80 &
curl http://localhost:8085/health
```

---

## Implemented Enhancements

* **CI Enhancement — Automated Unit Testing:** Integrated `pytest` directly into the `Jenkinsfile` `Test` stage so every commit is validated against automated endpoint tests before `todo-api-build.tar.gz` is packaged and archived.
* **Deployment Enhancement — Kubernetes ConfigMap:** Decoupled runtime configuration from the container image using `todo-api-config` (`PORT: "5050"`) injected via `envFrom`, allowing port updates without rebuilding `todo-api:v1`.
