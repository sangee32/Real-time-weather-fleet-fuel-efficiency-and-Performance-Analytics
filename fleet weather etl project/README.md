# Heavy fleet fuel and weather ETL pipeline

An end-to-end Data engineering ETL pipeline that ingests real-time weather data from the **open-meto REST API** and combines it with simulated heavy-machinery fleet trip logs to analyze fuel efficiency.

## Tech stack
* *Language:* Python
* *Ingestion & Transformation:* Requests, Pandas
* *Storage Format:* Apache Parquet (PyArrow)
* *Analytical SQL Engine:* DuckDB (CTEs & Window Functions)
* *Visualization:* Streamlit

## How to Run
1. Install dependencies: pip install -r requirements.txt
2. Extract data: python 1_extract.py
3. Clean & transform to Parquet: python 2_transform.py
4. Run SQL analytics: python 3_sql_analytics.py
5. Launch dashboard: streamlit run 4_dashboard.py