#### GCP DevOps Project

A minimal Flask web application, containerized with Docker, for practicing deployment to Google Cloud Platform.

## Project Structure

```
.
├── app.py            # Flask app with a single "/" route
├── requirements.txt  # Python dependencies (flask)
├── Dockerfile         # Container build for the app
└── README.md
```

## Prerequisites

- Python 3.8+
- Docker (for containerized run/deploy)

## Run Locally

```bash
pip3 install -r requirements.txt
python3 -m flask --app app run
```

The app will be available at http://127.0.0.1:5000.

## Run with Docker

```bash
docker build -t gcp-devops-project .
docker run -p 5001:5000 gcp-devops-project
```

The app will be available at http://127.0.0.1:5001.

## Deploying to GCP

The Docker image is ready to push to a container registry (Artifact Registry) and deploy, e.g. via Cloud Run:

```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/gcp-devops-project
gcloud run deploy gcp-devops-project --image gcr.io/PROJECT_ID/gcp-devops-project --platform managed
```
