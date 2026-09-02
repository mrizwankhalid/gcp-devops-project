#### GCP DevOps Project

A minimal Flask web application, containerized with Docker, for practicing deployment to Google Cloud Platform.

## Project Structure

```
.
├── app.py              # Flask app: /, /healthz, /readyz, /info
├── requirements.txt    # Python dependencies (flask)
├── Dockerfile          # Container build for the app
├── cloudbuild.yaml     # CI/CD pipeline: build, push, deploy to GKE
├── k8s/                 # Kubernetes manifests, built with kustomize
│   ├── base/            # Shared Deployment, Service, HPA, PDB
│   └── overlays/        # Per-environment patches
│       ├── dev/          # 1 replica, no HPA/PDB, smaller resources
│       ├── stage/        # HPA capped at 3 replicas
│       └── prod/         # Base defaults as-is (2-5 replicas)
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
4. Applies `k8s/overlays/<env>` via `kubectl apply -k` (Deployment, Service, and — for stage/prod — HPA/PDB) — the Deployment wires `/healthz` and `/readyz` in as liveness/readiness probes
5. Points the deployment at the newly built image, in that environment's namespace

### Environments

`dev`, `stage`, and `prod` each deploy to their own namespace on the same GKE cluster, via a kustomize overlay under `k8s/overlays/`:

| Env | Namespace | Replicas | HPA / PDB | `APP_ENV` |
|---|---|---|---|---|
| dev | `dev` | 1 | none | `dev` |
| stage | `stage` | 2 (up to 3 via HPA) | yes | `stage` |
| prod | `prod` | 2 (up to 5 via HPA) | yes | `production` |

Which environment and cluster to deploy to is controlled by the `_ENV`, `_CLUSTER_NAME`, and `_CLUSTER_ZONE` substitution variables (defaults live in `cloudbuild.yaml`, defaulting to `dev`). In practice, set up one Cloud Build trigger per environment (e.g. on branch/tag patterns) each with its own substitutions, or trigger manually:

```bash
gcloud builds submit --config cloudbuild.yaml \
  --substitutions=_ENV=stage,_CLUSTER_NAME=your-gke-cluster,_CLUSTER_ZONE=us-central1-a
```

To preview or apply an overlay directly with kubectl:

```bash
kubectl kustomize k8s/overlays/dev   # preview the rendered manifests
kubectl apply -k k8s/overlays/dev
```
