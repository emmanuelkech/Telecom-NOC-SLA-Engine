import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine

# Database Connection
engine = create_engine('postgresql://postgres:umeanor01@localhost:5432/telecom_noc_db')

print("Generating telecom asset and customer dimensions...")

# 1. Populate dim_towers
cities = ['Lagos', 'Abuja', 'Port Harcourt', 'Ibadan', 'Kano']
towers = []
for i in range(50):
    towers.append({
        "tower_id": f"TWR-{3000+i}",
        "location_city": random.choice(cities),
        "hardware_type": random.choice(['4G', '5G'])
    })
pd.DataFrame(towers).to_sql('dim_towers', engine, if_exists='append', index=False)

# 2. Populate dim_subscribers
tiers = ['Consumer', 'VIP', 'Enterprise']
subscribers = []
for i in range(1000):
    tier = random.choice(tiers)
    val = round(random.uniform(10.0, 45.0), 2) if tier == 'Consumer' else round(random.uniform(150.0, 2000.0), 2)
    subscribers.append({
        "subscriber_id": f"SUB-{9000+i}",
        "account_tier": tier,
        "monthly_value": val
    })
pd.DataFrame(subscribers).to_sql('dim_subscribers', engine, if_exists='append', index=False)

print("Simulating network performance spikes and support failures...")

tower_keys = pd.read_sql("SELECT tower_key FROM dim_towers", engine)['tower_key'].tolist()
sub_keys = pd.read_sql("SELECT subscriber_key, account_tier FROM dim_subscribers", engine).to_dict('records')

start_date = datetime(2026, 5, 1)
perf_records = []
ticket_records = []

# Generate 30 days of tracking
for day in range(30):
    current_date = start_date + timedelta(days=day)
    
    # 3. Generate Daily Network Metrics (~1500 logs)
    tower_key_list = tower_keys
    for t_key in tower_key_list:
        # Standard performance metrics
        dropped_rate = round(random.uniform(0.1, 1.8), 2)
        data_speed = round(random.uniform(15.0, 95.0), 2)
        
        # Inject Outage Vector: Towers 5, 12, and 27 break down between May 10th and May 15th
        if t_key in [5, 12, 27] and datetime(2026, 5, 10).date() <= current_date.date() <= datetime(2026, 5, 15).date():
            dropped_rate = round(random.uniform(8.5, 24.2), 2)
            data_speed = round(random.uniform(0.5, 3.2), 2)
            
        perf_records.append({
            "tower_key": t_key,
            "log_date": current_date.date(),
            "dropped_call_rate": dropped_rate,
            "avg_data_speed_mbps": data_speed
        })
        
        # 4. Generate Support Incidents linked to these towers
        if dropped_rate > 5.0:
            # High dropped rate forces massive ticket surges from affected users
            for _ in range(random.randint(10, 30)):
                sub = random.choice(sub_keys)
                res_hours = round(random.uniform(4.0, 48.0), 2)
                # If it's an Enterprise account, SLA is strictly breached if resolution takes > 12 hours
                sla = "Breached" if (sub['account_tier'] == 'Enterprise' and res_hours > 12.0) else "Met"
                if res_hours > 24.0: sla = "Breached" # Everyone breaches past 24 hours
                
                ticket_records.append({
                    "subscriber_key": sub['subscriber_key'],
                    "tower_key": t_key,
                    "ticket_date": current_date.date(),
                    "resolution_time_hours": res_hours,
                    "sla_status": sla
                })

pd.DataFrame(perf_records).to_sql('fact_network_performance', engine, if_exists='append', index=False)
pd.DataFrame(ticket_records).to_sql('fact_support_tickets', engine, if_exists='append', index=False)
print(f"Successfully generated and injected {len(perf_records)} performance records and {len(ticket_records)} SLA incidents.")