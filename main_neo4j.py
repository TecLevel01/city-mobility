from data_generator import *
from load_neo4j import *
from benchmark_neo4j import run_benchmark

USER_SIZES = [1000, 10000, 50000]
TRIP_SIZES = [10000, 50000, 100000]
# EVENTS_PER_TRIP = [0, 2, 5, 10]

N_STATIONS = 100

insertion_id = 1

benchmark_results = []

for n_users in USER_SIZES:
    for n_trips in TRIP_SIZES:
        # for n_events in EVENTS_PER_TRIP:

        print("\n==============================")
        print(f"Neo4j Insertion #{insertion_id}")
        print(
            f"Users: {n_users}, Trips: {n_trips}, Trip(s): {n_trips}")
        print("==============================")

        # 1. CLEAR DATABASE
        clear_neo4j()

        # 2. GENERATE DATA
        users = generate_users(n_users)
        stations = generate_stations(N_STATIONS)
        trips = generate_trips(n_trips, n_users, N_STATIONS)
        # events = generate_events(trips, n_events)

        # 3. INSERT (BATCH MODE)
        insert_users_batch(users)
        insert_stations_batch(stations)
        insert_trips_batch(trips)
        # insert_events_batch(events)

        print("Data inserted successfully.")
        # run_benchmark(n_users)

        q1_time, q2_time = run_benchmark(n_users)

        benchmark_results.append({
            "insertion": insertion_id,
            "users": n_users,
            "trips": n_trips,
            # "events": n_events,
            "query1_time": round(q1_time, 4),
            "query2_time": round(q2_time, 4)
        })

        insertion_id += 1


print("\n==============================================")
print("FINAL NEO4J SCALABILITY RESULTS")
print("==============================================")

for result in benchmark_results:

    print(
        f"Insertion {result['insertion']} | "
        f"Users={result['users']} | "
        f"Trips={result['trips']} | "
        # f"Events/Trip={result['events']} | "
        f"Q1={result['query1_time']} sec | "
        f"Q2={result['query2_time']} sec"
    )
