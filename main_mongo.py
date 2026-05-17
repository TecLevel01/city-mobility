from data_generator import *
from load_mongo import *
from benchmark_mongo import run_all_queries
import csv

USER_SIZES = [1000, 10000, 50000]
TRIP_SIZES = [10000, 50000, 100000]
EVENTS_PER_TRIP = [0, 2, 5, 10]

N_STATIONS = 100

results = []

create_indexes()

insertion_id = 1

for n_users in USER_SIZES:
    for n_trips in TRIP_SIZES:
        for n_events in EVENTS_PER_TRIP:

            print("\n==============================")
            print(f"Mongo Insertion #{insertion_id}")
            print(
                f"Users: {n_users}, Trips: {n_trips}, Events/Trip: {n_events}")
            print("==============================")

            # 1. CLEAR DB
            clear_collections()

            # 2. GENERATE DATA
            users = generate_users(n_users)
            stations = generate_stations(N_STATIONS)
            trips = generate_trips(n_trips, n_users, N_STATIONS)
            events = generate_events(trips, n_events)

            # 3. INSERT
            insert_users(users)
            insert_stations(stations)
            insert_trips_with_events(trips, events)

            print("MongoDB data inserted successfully.")

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

# SAVE TO CSV
with open("mongo_results.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print("Results saved to mongo_results.csv")
