# 🛡️ HDFS Log Analysis System on Azure Cloud

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Azure](https://img.shields.io/badge/Cloud-Microsoft%20Azure-0078D4.svg)
![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-FF4B4B.svg)
![Status](https://img.shields.io/badge/Status-Completed-success.svg)

## 📖 Overview
This project implements an **LSTM Autoencoder-based Anomaly Detection System** for HDFS (Hadoop Distributed File System) logs.
Designed to overcome resource limitations, the system runs on a **low-spec Azure Virtual Machine**, capable of processing **10 million log lines** continuously over **70 hours** using optimized memory management techniques.

---

## 📸 Dashboard & Results

### ✅ 1. Analysis Complete (70-Hour Run)
Successfully processed **9,950,000 lines** without crashing.
![Dashboard Screenshot](images/dashboard_complete.jpg)

### 📊 2. Analysis Insights
**99.90%** of the data was identified as a specific repetitive event pattern (`E5-E22...`), highlighting the need for model tuning against frequent loops.

| Metric | Result |
| :--- | :--- |
| **Total Processed** | **9,950,000 lines** |
| **Runtime** | **~70 hours** |
| **Dominant Pattern** | `E5-E22...` (99.90%) |

#### Anomaly Score Distribution & Top Events
<p float="left">
  <img src="images/graph_score.png" width="45%" />
  <img src="images/graph_events.png" width="45%" />
</p>

---

## 🚀 Key Features

### 1. Cloud-Optimized Architecture ☁️
* **Environment:** Microsoft Azure VM (Standard_B2s).
* **Challenge:** Processing 10M lines on limited RAM (4GB).
* **Solution:** Implemented a **Chunk-based processing pipeline** with aggressive **Garbage Collection (GC)** to maintain stable memory usage (~2GB) throughout the 70-hour operation.

### 2. Robust Reliability 🛡️
* **Exception Handling:** Automated error skipping logic ensures the system never stops even when encountering corrupted log lines (e.g., Chunk 18 warning).
* **Real-time Monitoring:** Custom **Streamlit dashboard** to visualize progress, CPU/Memory usage, and real-time anomaly detection logs.

---

## 🛠️ Tech Stack
* **Infrastructure:** Microsoft Azure Virtual Machines (Ubuntu)
* **Language:** Python 3.9
* **ML Model:** LSTM Autoencoder (PyTorch)
* **Libraries:** Pandas, Scikit-learn, Streamlit, Matplotlib
* **Dataset:** HDFS System Logs

## 👨‍💻 Author
* **Keisando**
* *Project for Large-scale System Log Analysis Research*