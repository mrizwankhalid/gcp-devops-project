#### GCP DevOps Project

A minimal Flask web application, containerized with Docker, for practicing deployment to Google Cloud Platform.

## Project Structure

```
.
├── app.py            # Flask app with a single "/" route
├── requirements.txt  # Python dependencies (flask)
├── Dockerfile        # Container build for the app
├── cloudbuild.yaml   # CI/CD pipeline: build, push, deploy to GKE
└── README.md
```

The GKE Deployment/Service manifest (`gke.yaml`) that `cloudbuild.yaml` applies lives one level up, at the repo root.

## Prerequisites

- Python 3.8+
- Docker (for containerized run/deploy)

## Run Locally

```bash
pip3 install -r requirements.txt
python3 -m flask --app app run
```

The app will be available at http://127.0.0.1:5001.

## Run with Docker

```bash
docker build -t gcp-devops-project .
docker run -p 5001:5000 gcp-devops-project
```

The app will be available at http://127.0.0.1:5001.

## Deploying to GKE

`cloudbuild.yaml` defines a Cloud Build pipeline that:

1. Builds the Docker image, tagged with the commit SHA
2. Pushes it to Container Registry
3. Fetches credentials for the target GKE cluster
4. Applies `../gke.yaml` (Deployment + LoadBalancer Service)
5. Points the deployment at the newly built image

The cluster name and zone are configurable via the `_CLUSTER_NAME` and `_CLUSTER_ZONE` substitution variables (defaults live in `cloudbuild.yaml`). Trigger a build with:

```bash
gcloud builds submit --config cloudbuild.yaml \
  --substitutions=_CLUSTER_NAME=your-gke-cluster,_CLUSTER_ZONE=us-central1-a
```
