
from data_generator import *
from load_postgres import *
from benchmark_postgres import run_all_queries
import csv

USER_SIZES = [1000, 10000, 50000]
TRIP_SIZES = [10000, 50000, 100000]
EVENTS_PER_TRIP = [0, 2, 5, 10]

N_STATIONS = 100
results = []


insertion_id = 1  # MY COUNTERR

for n_users in USER_SIZES:
    for n_trips in TRIP_SIZES:
        for n_events in EVENTS_PER_TRIP:

            print("\n==============================")
            print(f"Insertion #{insertion_id}")
            print(
                f"Users: {n_users}, Trips: {n_trips}, Events/Trip: {n_events}")
            print("==============================")

            # 1. CLEAN DATABASE
            clear_tables()

            # 2. GENERATE DATA
            users = generate_users(n_users)
            stations = generate_stations(N_STATIONS)
            trips = generate_trips(n_trips, n_users, N_STATIONS)
            events = generate_events(trips, n_events)

            # 3. INSERT DATA
            insert_users(users)
            insert_stations(stations)
            insert_trips(trips)
            insert_events(events)

            print("Data inserted successfully.")

            # 4. RUN QUERIES
            timings = run_all_queries()

            print("Query times:", timings)

            # 5. STORE RESULTS
            results.append({
                "Run": insertion_id,
                "Users": n_users,
                "Trips": n_trips,
                "Events_per_trip": n_events,
                **timings
            })
            insertion_id += 1


# SAVE RESULTS
with open("postgres_results.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print("Results saved to postgres_results.csv")
