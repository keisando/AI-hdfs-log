# 🛡️ AI-Based HDFS Log Anomaly Detection System

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15-orange?logo=tensorflow&logoColor=white)
![Azure](https://img.shields.io/badge/Cloud-Microsoft%20Azure-0078D4?logo=microsoftazure&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Container-2496ED?logo=docker&logoColor=white)

**[English]** / [日本語](#-大規模システムログ異常検知システム-japanese)

## 📖 Overview
This project is an **AIOps (Artificial Intelligence for IT Operations)** solution designed to detect anomalies in large-scale system logs (HDFS) using **Deep Learning (LSTM Autoencoder)**.

Unlike typical research that uses small sampled datasets, this project focuses on **scalability and production-readiness**. It successfully processed **10 million lines (1.5 GB)** of raw logs by leveraging cloud infrastructure (Azure) and memory-optimized engineering techniques.

### 🚀 Key Achievements
- **Scalability**: Processed **9,950,000 log lines** on a 16GB RAM environment using stream processing (Chunking).
- **Stability**: Achieved **70 hours of continuous operation** without Memory Error (OOM).
- **Infrastructure**: Fully containerized application using **Docker** on **Microsoft Azure VM**.
- **Analysis**: Identified structural issues in static thresholding for large-scale real-world data (99.9% anomaly rate).

---

## 🏗️ System Architecture

The system consists of three main layers designed to handle "Big Data" on limited resources.

```mermaid
graph TD
    subgraph Azure_Cloud [Microsoft Azure VM (Standard D4s v3)]
        style Azure_Cloud fill:#f9f9f9,stroke:#333,stroke-width:2px
        
        Input[(HDFS Raw Logs<br/>1.5GB)] -->|Stream Read| Pipe[Data Pipeline]
        
        subgraph Docker_Container [Docker Container]
            style Docker_Container fill:#e1f5fe,stroke:#0277bd,stroke-width:2px
            
            Pipe -->|Chunking & GC| Parser[Log Parser<br/>(Drain Algorithm)]
            Parser -->|Templates| Vector[Feature Engineering]
            Vector -->|Sequences| Model[LSTM Autoencoder<br/>(TensorFlow)]
            Model -->|Reconstruction Error| Score[Anomaly Score]
        end
        
        Score -->|Visualization| Dash[Streamlit Dashboard]
    end
