# Golden 360: Unified E-Commerce Customer Platform

**Document Owner:** [Your Name]  
**Stack:** Python, SQL, PySpark, FastAPI  
**Architecture:** Medallion (Bronze/Silver/Gold)  
**Timeline:** 3 Months

---

## Project Overview

### The Problem
Customer data is fragmented across 9 tables in the Olist dataset. Analysts waste hours joining tables manually. Marketing can't calculate accurate LTV. Customer service can't quickly pull customer history.

### The Solution
Build an **Identity Bridge** to unify all customer data into a single Golden Record accessible via one API endpoint.

**Before:** Query 9 tables → Manual joins → Hours of work  
**After:** One API call → Complete customer profile → Milliseconds

### Core Objective
Shift from **table-centric** to **customer-centric** architecture. One customer ID, one unified record, all insights.

---

## Architecture: The Medallion Layers

### Bronze Layer (Raw Ingestion)
**Purpose:** Land raw CSV files without modification  
**Tool:** Python  
**Key Concept:** Idempotency

**What happens:**
- Ingest 9 CSV files from Olist Kaggle dataset
- Store in `/data/bronze/YYYY-MM-DD/` folder
- Calculate file checksums (MD5/SHA256)
- Check if already ingested → skip if duplicate
- Generate metadata.json for audit trail

**Critical:** Never modify Bronze files. They're your source of truth.

**Files ingested:**
1. olist_customers_dataset.csv
2. olist_orders_dataset.csv
3. olist_order_items_dataset.csv
4. olist_order_reviews_dataset.csv
5. olist_products_dataset.csv
6. olist_sellers_dataset.csv
7. olist_geolocation_dataset.csv
8. olist_order_payments_dataset.csv
9. product_category_name_translation.csv

### Silver Layer (Cleaned Data)
**Purpose:** Clean, validate, and standardize data  
**Tool:** PySpark  
**Key Concept:** Data Integrity

**Transformations per table:**

**Customers:**
- Remove duplicate customer_ids
- Convert zip_code to integer
- Uppercase and trim city/state names
- Validate no null customer_ids

**Orders:**
- Deduplicate order_ids
- Cast order_purchase_timestamp to ISO datetime
- Validate order_status in allowed values
- Ensure delivered orders have delivery dates

**Reviews:**
- One review per order
- Handle nulls: review_comment_message → "No comment provided"
- Cast review_score to integer (1-5)
- Validate scores in range

**Order Items:**
- Composite key deduplication (order_id + item_id)
- Cast price/freight to decimal(10,2)
- Validate price > 0

**Storage:** Parquet format in `/data/silver/table_name/`

### Gold Layer (Business Ready)
**Purpose:** Create the unified customer 360 view  
**Tool:** PySpark + SQL  
**Key Concept:** Serving Layer

**The Identity Bridge:**
```
golden_id = SHA256(customer_unique_id + customer_id)
```

**Join Logic:**
```
customers 
  → JOIN orders ON customer_id
  → JOIN order_items ON order_id
  → JOIN reviews ON order_id
  → JOIN payments ON order_id
  → JOIN products ON product_id
```

**Aggregated Metrics (per golden_id):**

**Financial:**
- total_spend = SUM(payment_value)
- avg_order_value = total_spend / order_count
- max_single_order = MAX(payment_value)

**Behavioral:**
- order_count = COUNT(order_id)
- first_order_date = MIN(order_date)
- last_order_date = MAX(order_date)
- days_since_last_order = today - last_order_date

**Product:**
- total_items = SUM(items)
- unique_products = COUNT(DISTINCT product_id)
- favorite_category = MODE(product_category)
- product_diversity = unique_categories / order_count

**Sentiment:**
- avg_review_score = AVG(review_score)
- total_reviews = COUNT(review_id)

**LTV Segmentation:**
- VIP: total_spend > $5000
- High: $1000 - $5000
- Medium: $200 - $1000
- Low: < $200

**Output:** PostgreSQL table `unified_customer_360`

---

## API Serving Layer

### FastAPI Backend

**Endpoint:** `GET /customer/{golden_id}`

**Response Schema (Pydantic):**
```json
{
  "golden_id": "abc123...",
  "customer_unique_id": "8d50f...",
  "customer_id": "0001...",
  "total_spend": 4523.50,
  "avg_order_value": 376.96,
  "order_count": 12,
  "avg_review_score": 4.3,
  "ltv_segment": "High",
  "first_order_date": "2023-01-15",
  "last_order_date": "2024-11-15",
  "days_since_last_order": 82,
  "favorite_category": "Electronics",
  "product_diversity": 0.75,
  "geographic_state": "SP",
  "geographic_city": "SÃO PAULO"
}
```

**Additional Endpoints:**
- `GET /customers/segment/{segment}` - Filter by LTV segment
- `GET /health` - Health check
- `GET /metrics` - Prometheus metrics

**Key Features:**
- Pydantic validation for type safety
- <100ms response time (P95)
- PostgreSQL connection pool
- Error handling and logging
- API documentation via Swagger

---

## Implementation Roadmap (3 Months)

### Month 1: Foundation
**Week 1-2: Bronze Layer**
- [ ] Set up project structure
- [ ] Download Olist dataset from Kaggle
- [ ] Write Python ingestion script
- [ ] Implement checksum-based idempotency
- [ ] Create metadata.json generator
- [ ] Test: Run ingestion twice, verify no duplicates

**Week 3-4: Silver Layer Setup**
- [ ] Set up PySpark environment
- [ ] Write transformation script for customers table
- [ ] Write transformation script for orders table
- [ ] Write transformation script for reviews table
- [ ] Implement data quality checks
- [ ] Test: Validate cleaned data quality

### Month 2: Gold Layer & Identity Bridge
**Week 5-6: Data Modeling**
- [ ] Design unified_customer_360 schema
- [ ] Implement golden_id generation logic
- [ ] Write multi-table join logic
- [ ] Calculate all financial metrics
- [ ] Calculate behavioral metrics
- [ ] Test: Verify join correctness

**Week 7-8: Aggregations**
- [ ] Implement LTV calculations
- [ ] Build RFM segmentation
- [ ] Calculate product diversity metrics
- [ ] Aggregate sentiment scores
- [ ] Set up PostgreSQL database
- [ ] Load Gold data to database
- [ ] Create indexes for performance
- [ ] Test: Query performance < 100ms

### Month 3: API & Production
**Week 9-10: FastAPI Development**
- [ ] Set up FastAPI project structure
- [ ] Create Pydantic models
- [ ] Implement GET /customer/{golden_id}
- [ ] Add PostgreSQL connection
- [ ] Add error handling
- [ ] Write unit tests
- [ ] Generate API documentation
- [ ] Test: API response validation

**Week 11-12: Polish & Deploy**
- [ ] Add logging (structured JSON)
- [ ] Set up Prometheus metrics
- [ ] Create Grafana dashboard
- [ ] Write project documentation
- [ ] Performance testing
- [ ] Security review (API auth)
- [ ] Deploy to production
- [ ] Monitor and iterate

---

## Data Engineering Lifecycle Mapping (Joe Reis)

| Lifecycle Stage | Golden 360 Implementation | Tools | Concept Applied |
|----------------|---------------------------|-------|-----------------|
| **Generation** | Olist CSV files from Kaggle | Kaggle Dataset | Source systems |
| **Storage** | Local filesystem → S3 (future) | File system | Raw data storage |
| **Ingestion** | Bronze layer Python scripts | Python, OS | Idempotent ingestion |
| **Transformation** | Silver → Gold PySpark jobs | PySpark, SQL | Data quality & modeling |
| **Serving** | FastAPI REST endpoints | FastAPI, PostgreSQL | API-driven access |

**Underpinning Concepts:**
- **Data Management:** Master Data Management via golden_id
- **DataOps:** Automated quality checks, version control
- **Architecture:** Medallion pattern, separation of concerns
- **Orchestration:** Manual → Airflow (future)
- **Software Engineering:** SOLID principles, testing, documentation

---

## Data Quality Strategy

### Bronze Layer
- File integrity: Checksum validation
- Completeness: All 9 files present
- Idempotency: No duplicate ingestions

### Silver Layer
**Quality Checks:**
- Primary key uniqueness: 100%
- Critical fields non-null: >99%
- Data type compliance: 100%
- Business rules pass rate: >99%

**Validation Rules:**
- review_score BETWEEN 1 AND 5
- order_status IN (allowed_values)
- delivery_date >= purchase_date
- payment_value > 0

### Gold Layer
**Aggregation Validation:**
- Every golden_id has complete metrics
- Total_spend = SUM of all payments (cross-check)
- Order_count matches actual orders
- No orphaned records (referential integrity)

---

## Key Technical Decisions

### Why Medallion Architecture?
- **Separation of concerns:** Each layer has one job
- **Replayability:** Can rebuild Gold from Silver without re-ingesting
- **Data lineage:** Clear path from raw → clean → aggregated
- **Team collaboration:** Different teams work on different layers

### Why PySpark over Pandas?
- **Scalability:** Works on 1GB or 1TB of data
- **Performance:** Lazy evaluation, distributed processing
- **Future-proof:** Easy to move to cloud (Databricks, EMR)

### Why FastAPI over Flask?
- **Performance:** Async support, faster than Flask
- **Type safety:** Pydantic integration catches bugs early
- **Documentation:** Auto-generated Swagger docs
- **Modern:** Built for Python 3.6+ with type hints

### Why PostgreSQL?
- **Reliability:** ACID compliance for data integrity
- **Performance:** Excellent query optimizer
- **JSON support:** Can extend schema easily
- **Ecosystem:** Mature, well-documented

---

## Success Metrics

| Metric | Target | How to Measure |
|--------|--------|----------------|
| API Response Time | <100ms P95 | Prometheus histogram |
| Data Quality Score | >99% | Automated quality checks |
| Pipeline Execution Time | <1 hour | Bronze → Gold total time |
| Test Coverage | >80% | Pytest coverage report |
| API Uptime | >99% | Availability monitoring |

---

## Why This Project Matters for Your Career

### 1. Ownership & System Design
You're not just writing scripts. You're **architecting a system** that handles real-world complexity:
- Data quality issues (nulls, duplicates, type mismatches)
- Performance optimization (indexes, query tuning)
- Scalability planning (Bronze → Silver → Gold pattern)
- API design (REST principles, validation, error handling)

### 2. Professional Documentation
This markdown document demonstrates you understand the **"why"** behind technical decisions:
- Business value proposition
- Architectural patterns
- Trade-off analysis
- Implementation roadmap

Show this to your Technical Director. It proves you think like an engineer, not just a coder.

### 3. Full-Stack Data Engineering
**Backend:** FastAPI, PostgreSQL, REST APIs  
**Data Processing:** PySpark, SQL, data transformations  
**Data Architecture:** Medallion pattern, data modeling  
**DevOps:** Testing, logging, monitoring, deployment

You touch every part of the modern data stack.

### 4. Portfolio-Ready Project
This is a **complete, working system** you can demo:
- Live API endpoint
- Real dataset (Olist public data)
- Production-grade architecture
- Full documentation

Perfect for GitHub, interviews, and your resume.

---

## The "Reset" Motto

> **"Master the concept, then the code. One project, one goal, zero distractions."**

**What this means:**
1. **Understand WHY** before writing code (Bronze = immutable raw data)
2. **One project at a time** - finish Golden 360 before starting new ideas
3. **Focus on fundamentals** - Medallion architecture, data quality, API design
4. **Ship it** - A working project beats 10 unfinished ideas

**Your North Star:** At the end of 3 months, you can type one API call and get a complete customer profile. That's the goal. Everything else is a distraction.

---

## Quick Reference

### Project Structure
```
golden-360/
├── data/
│   ├── bronze/YYYY-MM-DD/
│   ├── silver/
│   └── gold/
├── src/
│   ├── ingestion/     # Bronze layer scripts
│   ├── transformation/ # Silver layer PySpark
│   ├── aggregation/   # Gold layer SQL
│   └── api/           # FastAPI application
├── tests/
├── docs/
└── README.md
```

### Common Commands
```bash
# Ingest Bronze
python src/ingestion/ingest_bronze.py

# Transform to Silver
spark-submit src/transformation/transform_silver.py

# Build Gold layer
spark-submit src/aggregation/build_gold.py

# Start API
uvicorn src.api.main:app --reload

# Run tests
pytest tests/ --cov
```

### Database Connection
```python
# PostgreSQL connection string
postgresql://user:pass@localhost:5432/golden360
```

### API Testing
```bash
# Get customer profile
curl http://localhost:8000/customer/{golden_id}

# Health check
curl http://localhost:8000/health
```

---

**Last Updated:** February 2026  
**Version:** 1.0  
**Status:** Ready for Implementation