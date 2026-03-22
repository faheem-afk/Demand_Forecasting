<h1 align="center">🚀 Demand Forecasting System</h1>

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?size=22&duration=3000&color=36BCF7&center=true&vCenter=true&width=600&lines=12+Models.+12+Weeks+Ahead.;End-to-End+ML+Pipeline;Built+for+Real-World+Demand+Forecasting" />
</p>

<p align="center">
  <a href="https://demandforecastt.streamlit.app">
    <img src="https://img.shields.io/badge/Live-Demo-brightgreen?style=for-the-badge&logo=streamlit" />
  </a>
  <img src="https://img.shields.io/badge/Status-Development-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Data-320K%20Rows-orange?style=for-the-badge" />
</p>

---

## 📌 Overview

This is not just a model.

It’s a **production-style demand forecasting system** designed to predict meal demand across cities — built with modular pipelines, containerized services, and scalable data workflows.

⚠️ This repo represents the **development environment (Docker-based)**  
🚀 Production runs on **Neon (serverless Postgres) + Streamlit Cloud**

---

## 🧠 Problem

Forecast demand for the next **12 weeks** across multiple cities.

Not one prediction.  
A full **multi-horizon forecasting system**.

---

## ⚙️ System Architecture

<p align="center">
  <img src="https://img.shields.io/badge/Docker%20Compose-Orchestrated-blue?style=flat-square" />
</p>

Docker Compose
│
├── ML Pipeline (training + inference)
├── API Layer
├── Streamlit Dashboard
└── PostgreSQL (local DB)

Each service runs independently → clean, modular, scalable.

---

## 📊 Model Design

- Trained **12 independent XGBoost models**
- Each model predicts a specific horizon:

Week +1 → Model 1
Week +2 → Model 2
…
Week +12 → Model 12

📦 Dataset:
- ~320,000 rows  
- 32 features  

---

## 🔧 Feature Engineering

Time-series specific transformations:

- Lag features (historical demand)
- Rolling statistics (moving averages)
- Categorical encoding
- Missing value handling

---

## 🔍 Interpretability (SHAP)

Used SHAP to understand model behavior.

📈 Key drivers:
- `num_orders` (historical demand)
- `num_orders_rolling_16_week`

👉 The model heavily relies on **recent + smoothed historical trends**

---

## ⚡ Performance Optimization

- Replaced row-wise inserts with **PostgreSQL COPY**
- Achieved significantly faster ingestion
- Improved pipeline efficiency for large datasets

---

## 🐳 Dockerized Development

<p align="center">
  <img src="https://skillicons.dev/icons?i=docker,python,postgres" />
</p>

| Service        | Description                  |
|----------------|------------------------------|
| ML Pipeline    | Training + inference         |
| API            | Model interface              |
| Streamlit App  | Visualization dashboard      |
| PostgreSQL     | Local data storage           |

---

## 🚀 Production Setup

Streamlit Cloud (Frontend)
↓
Neon Postgres (Database)

Key differences:
- Local DB → Serverless Postgres  
- Docker → Cloud deployment  
- Direct DB access via Streamlit  

---

## 🖥️ Run Locally

```bash
git clone <your-repo-url>
cd demand_forecasting
docker compose up --build


⸻

📦 Project Structure

.
├── app/          # Streamlit app
├── model/        # ML pipeline
├── api/          # API layer
├── docker-compose.yaml
├── Dockerfile
├── requirements.txt
└── README.md


⸻

💡 Key Learnings
	•	Models are only one part of the system
	•	Data pipelines & storage matter just as much
	•	Containerization improves reproducibility
	•	Efficient DB operations (COPY) = major performance gains

⸻

🌐 Live Demo

👉 https://demandforecastt.streamlit.app

⸻

📫 Connect
	•	LinkedIn: https://www.linkedin.com/in/faheemb
	•	Email: adahm7114@gmail.com

⸻



⸻
