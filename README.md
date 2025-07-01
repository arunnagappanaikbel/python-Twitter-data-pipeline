**🔧 Project: Twitter Data ETL Pipeline**
---
**Objective**
Extract tweets from the Twitter API (X API v2 or from a sample file), perform 20+ complex transformations, and load the cleaned, enriched data into a PostgreSQL database.

## 📂 Repository Structure
```
twitter_etl_project/
│
├── config/
│   └── config.yaml
│
├── data/
│   ├── raw/
│   └── processed/
│
├── logs/
│   └── etl.log
│
├── src/
│   ├── extractor.py
│   ├── transformer.py
│   ├── loader.py
│   └── utils.py
│
├── .env
├── main.py
├── requirements.txt
└── README.md

```
---

**✅ Features**
 - Real-time Twitter API extraction (or sample file)
 - 20+ complex transformations: text cleaning, NLP-based features, date parsing, user stats
 - Error handling & logging
 - Config-driven (.env + YAML)
 - Modular code (extractor, transformer, loader)
 - PostgreSQL load
 - Designed for Airflow and Docker
