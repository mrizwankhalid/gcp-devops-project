#### GCP DevOps Project

A minimal Flask web application, containerized with Docker, for practicing deployment to Google Cloud Platform.

## Project Structure

```
.
├── app.py              # Flask app: /, /healthz, /readyz, /info
├── requirements.txt    # Python dependencies (flask)
├── Dockerfile          # Container build for the app
├── cloudbuild.yaml     # CI/CD pipeline: build, push, deploy to GKE
├── k8s/                # Kubernetes manifests applied by cloudbuild.yaml
│   ├── deployment.yaml  # App Deployment
│   ├── service.yaml     # LoadBalancer Service
│   ├── hpa.yaml         # HorizontalPodAutoscaler (CPU-based, 2-5 replicas)
│   └── pdb.yaml         # PodDisruptionBudget (minAvailable: 1)
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

The app will be available at http://127.0.0.1:5001.

### Routes

| Route | Purpose |
|---|---|
| `/` | Welcome message with app version, environment, and pod hostname |
| `/healthz` | Liveness probe — process is up |
| `/readyz` | Readiness probe — ready to receive traffic |
| `/info` | App version, environment, and pod hostname as JSON |

Configurable via env vars: `APP_VERSION` (default `1.0.0`), `APP_ENV` (default `production`).

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
4. Applies everything under `k8s/` (Deployment, Service, HPA, PDB) — the Deployment wires `/healthz` and `/readyz` in as liveness/readiness probes
5. Points the deployment at the newly built image

The cluster name and zone are configurable via the `_CLUSTER_NAME` and `_CLUSTER_ZONE` substitution variables (defaults live in `cloudbuild.yaml`). Trigger a build with:

```bash
gcloud builds submit --config cloudbuild.yaml \
  --substitutions=_CLUSTER_NAME=your-gke-cluster,_CLUSTER_ZONE=us-central1-a
```
