# AnthosGuard 🛡️

A cloud-native **fraud detection demo** built on **Google Kubernetes Engine (Autopilot)** with **Pub/Sub**, **FastAPI**, and **Kubernetes Ingress**.  
It simulates a financial system where new accounts are created and events are scored in real time for fraud risk.

---

## 🚀 Inspiration
We wanted to explore **event-driven architectures** with Anthos/GKE + Pub/Sub, showing how services can publish and subscribe securely across Kubernetes.

---

## ⚙️ What it does
- **Account Creator Service** (`account-created`)  
  Exposes a `POST /accounts` endpoint to publish new account-created events into **Pub/Sub**.  

- **Fraud Detector Service** (`fraud-detector`)  
  Subscribes to those events, applies a simple risk scoring function, and exposes:  
  - `/healthz` → readiness check  
  - `/status` → JSON summary of recent events  
  - `/dashboard` → human-friendly HTML dashboard of scored accounts  

---

## 🏗 How we built it
- **Languages**: Python (FastAPI, Pydantic)  
- **Containerization**: Docker, Artifact Registry  
- **Orchestration**: GKE Autopilot cluster  
- **Messaging**: Google Cloud Pub/Sub  
- **Ingress / Load Balancer**: Kubernetes Ingress + BackendConfig  
- **Testing**: Postman collection with automated assertions  

---

## 🧩 Repo Structure
anthosguard/
├── services/
│   ├── account-created/
│   │   ├── app/main.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   └── fraud-detector/
│       ├── app/main.py
│       ├── requirements.txt
│       └── Dockerfile
├── k8s/
│   ├── k8s-gke.yaml         # Deployments, Services, Ingress
│   ├── account-created-lb.yaml
│   └── fraud-detector-lb.yaml
├── postman/
│   ├── AnthosGuard_Demo_with_Tests.postman_collection.json
│   └── AnthosGuard_Env.postman_environment.json
├── recreate_anthosguard.sh  # script to recreate cluster + deploy
└── README.md
---

## ⚙️ Tech Stack
- **GKE Autopilot** — fully managed Kubernetes
- **Google Pub/Sub** — async event streaming
- **Workload Identity** — IAM-secure pod authentication
- **Python FastAPI** — lightweight microservices
- **Artifact Registry** — container image storage
- **Ingress (GCLB)** — external HTTP access
- **Optional AI** — Google Vertex AI model integration

---



## 🔧 Setup & Deployment

### 1. Enable APIs
### 2. Create Cluster & Namespace
### 3. Build & Push Images
### 4. Deploy Workloads
### 5. Expose Public Endpoints


## Test account creation event
curl -X POST http://$INGRESS_IP/accounts \
  -H "Content-Type: application/json" \
  -d '{"user_id":"u123","email":"test@mailinator.com","country":"ZZ"}'

#Accomplishments
	•	Fully event-driven, cloud-native stack in Kubernetes
	•	Pub/Sub integration across services
	•	Working fraud scoring with live dashboard
	•	Automated testing flow with Postman

What’s next
	•	Replace toy scoring with ML model
	•	Add CI/CD pipeline
	•	Multi-region HA deployment

#Acknowledgements
Built as part of the GKE Turns 10 Hackathon using Bank of Anthos + GKE + Google Cloud AI.


Built With
	•	Python 3.11 + FastAPI
	•	Google Kubernetes Engine (Autopilot)
	•	Google Cloud Pub/Sub
	•	Artifact Registry
	•	Docker
	•	Postman (demo & tests)