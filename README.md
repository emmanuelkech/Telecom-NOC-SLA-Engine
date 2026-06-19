# Enterprise Telecom Network Operations Capacity & SLA Suite

## Project Context
This final portfolio piece establishes an analytics platform aggregating 25,000 hourly network logs and customer support tickets to identify hardware service degradation and calculate contract monthly recurring revenue (MRR) at risk due to infrastructure SLA breaches.

## Enterprise Architecture Stack
- **Database Storage:** PostgreSQL Instance
- **Data Generation & Orchestration:** Python (Pandas, NumPy, SQLAlchemy)
- **BI Reporting & Governance Framework:** Power BI Desktop (SLA Analytics)

## High-Impact Operational Insights Uncovered
1. **Revenue Prioritization Mapping:** Uncovered explicit hardware outages where a drop in data download speeds across specific cell tower sectors put over $15,000 in monthly enterprise subscription contracts at direct risk of cancellation.
2. **SLA Friction Points:** Discovered that corporate customer tier ticket handling times dropped by 30% when routing through legacy 4G network nodes compared to modern 5G node regions, identifying a clear infrastructure upgrade path.

## How to Deploy Locally
1. Run DDL schema initializations inside your SQL terminal database server.
2. Populate the backend datasets by launching `python generate_telecom_data.py`.
3. Open and interact with the executive control suite by launching `Telecom_NOC_SLA_Suite.pbix`.
