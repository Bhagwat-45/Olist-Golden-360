# Golden 360: Unified Customer Data Platform

Production-grade data pipeline that transforms fragmented e-commerce data into a unified customer view via REST API.

**Stack:** Python | PySpark | FastAPI | PostgreSQL  

**Architecture:** Medallion (Bronze/Silver/Gold)  

**Dataset:** Olist Brazilian E-Commerce

---

## Problem & Solution

**Before:** Customer data scattered across 9 tables requiring manual joins  

**After:** Single API call returns complete customer profile in under 100ms

---

## Architecture

**Bronze Layer** - Raw CSV ingestion with idempotency (Python)  

**Silver Layer** - Data cleaning and validation (PySpark)  

**Gold Layer** - Identity resolution and metric aggregation (PySpark + SQL)  

**Serving Layer** - REST API for unified profiles (FastAPI + PostgreSQL)

---

## Key Features

- SHA256-based customer identity resolution

- Aggregated metrics: LTV, order frequency, product preferences

- Customer segmentation: VIP/High/Medium/Low tiers

- Sub-100ms API response times

- Automated data quality validation

---

## Quick Start

```bash

# Install dependencies

pip install -r requirements.txt

# Run pipeline

python src/ingestion/ingest_bronze.py

spark-submit src/transformation/transform_silver.py

spark-submit src/aggregation/build_gold.py

# Start API

uvicorn src.api.main:app --reload

```

---

## API Usage

```bash

# Get customer profile

curl http://localhost:8000/customer/{golden_id}

# Filter by segment

curl http://localhost:8000/customers/segment/VIP

```

---

## Project Structure

```

golden-360/

├── data/bronze/          # Raw CSV files

├── data/silver/          # Cleaned Parquet

├── data/gold/            # Aggregated profiles

├── src/

│   ├── ingestion/        # Bronze layer

│   ├── transformation/   # Silver layer

│   ├── aggregation/      # Gold layer

│   └── api/              # FastAPI app

└── tests/

```

---

## Data Quality

- Primary key uniqueness: 100%

- Critical field completeness: >99%

- Business rule validation: >99%

- API response time (P95): <100ms

---

## Technical Decisions

**Medallion Pattern:** Separation of concerns, replayability, clear lineage  

**PySpark:** Scalable from GB to TB, cloud-ready  

**FastAPI:** Async, type-safe, auto-documented  

**PostgreSQL:** ACID compliance, query performance

---

## License

MIT

---

**Version:** 1.0.0  

**Status:** Active Development
