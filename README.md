🚀 Demand Forecasting System (Development Version)

An end-to-end multi-horizon demand forecasting system designed to predict meal demand across cities using time-series machine learning, modular pipelines, and containerized architecture.

⚠️ This repository represents the development environment (Docker-based).
The deployed version uses Neon (serverless Postgres) and Streamlit Cloud.

⸻

📌 Overview

This project goes beyond a single model and focuses on building a production-style ML system, including:
	•	Data preprocessing & feature engineering
	•	Multi-horizon forecasting
	•	Model interpretability
	•	Containerized services
	•	Efficient data storage

⸻

🧠 Problem Statement

Forecast meal demand across multiple cities for the next 12 weeks, enabling better planning and decision-making.

⸻

⚙️ System Architecture (Development)

Docker Compose
│
├── ML Pipeline (training + inference)
├── API Layer
├── Streamlit Dashboard
└── PostgreSQL (local DB)

Each component runs in its own container, enabling modular development and easy orchestration.

⸻

📊 Model Design
	•	Trained 12 independent XGBoost models, each predicting a specific forecast horizon:
	•	Model 1 → Week +1
	•	Model 2 → Week +2
	•	…
	•	Model 12 → Week +12
	•	Dataset:
	•	~320,000 rows
	•	32 features

⸻

🔧 Feature Engineering

Implemented time-series specific features:
	•	Lag features (historical demand)
	•	Rolling statistics (moving averages)
	•	Categorical encoding
	•	Missing value handling

🔍 Model Interpretability

Used SHAP (SHapley Additive Explanations) to analyze feature importance.

Key insights:
	•	Historical demand (num_orders)
	•	16-week rolling average demand

These were the most influential predictors across models.

⸻

⚡ Performance Optimization
	•	Replaced row-wise inserts with PostgreSQL COPY
	•	Achieved significantly faster bulk data ingestion
	•	Improved pipeline efficiency for large datasets

⸻

🐳 Dockerized Development

The system is fully containerized using:
	•	Docker
	•	Docker Compose

Services:

Service	Description
ML Pipeline	Training & prediction logic
API	Interface for model outputs
Streamlit App	Visualization dashboard
PostgreSQL	Local data storage


⸻

🚀 Deployment Architecture (Production)

Streamlit Cloud (Frontend)
        ↓
Neon Postgres (Database)

Key differences from development:
	•	Local PostgreSQL → Neon (serverless Postgres)
	•	Docker containers → Cloud-hosted services
	•	Direct DB connection via Streamlit

⸻

🖥️ Running Locally

1. Clone the repo

git clone <your-repo-url>
cd demand_forecasting


⸻

2. For each service

docker compose up --build


⸻

📦 Project Structure

.
├── app/                  # Streamlit app + DB utilities
├── model/                # ML pipeline (training, inference, feature engineering)
├── api/                  # API layer (if applicable)
├── docker-compose.yaml
├── Dockerfile
├── requirements.txt
└── README.md


⸻

🔐 Notes
	•	Local development uses Docker-based PostgreSQL
	•	Production uses Neon for scalability
	•	Secrets (DB credentials) are not included in the repo

⸻

💡 Key Learnings
	•	Building the model is only a small part of the system
	•	Data pipelines, storage, and deployment are equally critical
	•	Containerization simplifies reproducibility and system design
	•	Efficient database operations (e.g., COPY) significantly impact performance

⸻

🌐 Live Demo

👉 https://demandforecastt.streamlit.app

⸻

📬 Contact

If you’d like to discuss this project or collaborate:
	•	LinkedIn: https://www.linkedin.com/in/faheemb
	•	Email: adahm7114@gmail.com

⸻

⭐ If you like this project, consider giving it a star!

⸻
