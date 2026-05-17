from pymongo import MongoClient
from datetime import datetime, timedelta
import random
import time
from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StructType,
    StructField,
    IntegerType,
    DoubleType,
    StringType,
    ArrayType,
    TimestampType
)

from pyspark.sql.functions import (
    col,
    count,
    avg,
    unix_timestamp
)

# MONGODB CONNECTION
mongo_client = MongoClient("mongodb://127.0.0.1:27017/")
db = mongo_client["cityMobility"]
trips_col = db["trips"]


# SPARK SESSION
spark = SparkSession.builder \
    .appName("MongoSparkQuery2Benchmark") \
    .config(
        "spark.jars.packages",
        "org.mongodb.spark:mongo-spark-connector_2.12:10.3.0"
    ) \
    .config(
        "spark.mongodb.read.connection.uri",
        "mongodb://127.0.0.1:27017/cityMobility.trips"
    ) \
    .getOrCreate()
spark.sparkContext.setLogLevel("ERROR")


# EVENT SCHEMA
event_schema = StructType([
    StructField(
        "event_type",
        StringType(),
        True
    ),
    StructField(
        "event_time",
        TimestampType(),
        True
    ),
    StructField(
        "event_value",
        StringType(),
        True
    )
])


# TRIP SCHEMA
trip_schema = StructType([
    StructField(
        "_id",
        IntegerType(),
        True
    ),
    StructField(
        "user_id",
        IntegerType(),
        True
    ),
    StructField(
        "start_station",
        IntegerType(),
        True
    ),
    StructField(
        "end_station",
        IntegerType(),
        True
    ),
    StructField(
        "start_time",
        TimestampType(),
        True
    ),
    StructField(
        "end_time",
        TimestampType(),
        True
    ),
    StructField(
        "total_cost",
        DoubleType(),
        True
    ),
    StructField(
        "events",
        ArrayType(event_schema),
        True
    )
])


# GENERATE RANDOM EVENT
def generate_event(base_time):
    event_types = [
        "GPS",
        "BATTERY",
        "ERROR"
    ]

    return {

        "event_type": random.choice(event_types),

        "event_time": (
            base_time +
            timedelta(
                minutes=random.randint(1, 30)
            )
        ),

        "event_value": random.choice([
            "weak signal",
            "no signal",
            "battery low",
            "sensor malfunction"
        ])
    }


# GENERATE SIMULATED DATA
def generate_data(num_users, num_trips, events_per_trip):
    print("\n=================================================")
    print("GENERATING DATASET")
    print(f"Users: {num_users}")
    print(f"Trips: {num_trips}")
    print(f"Events per Trip: {events_per_trip}")
    print("=================================================")

    # CLEAR OLD DATA
    trips_col.delete_many({})
    trips = []
    base_date = datetime(2026, 1, 1, 8, 0, 0)

    for trip_id in range(num_trips):

        user_id = random.randint(1, num_users)
        start_time = (
            base_date +
            timedelta(minutes=random.randint(0, 100000)))
        duration_minutes = random.randint(5, 90)
        end_time = (
            start_time +
            timedelta(minutes=duration_minutes))

        # GENERATE EVENTS
        events = []

        for _ in range(events_per_trip):
            events.append(generate_event(start_time))

        trip_doc = {

            "_id": trip_id,
            "user_id": user_id,
            "start_station": random.randint(1, 50),
            "end_station": random.randint(1, 50),
            "start_time": start_time,
            "end_time": end_time,
            "total_cost": round(
                random.uniform(2.0, 15.0), 2),
            "events": events
        }

        trips.append(trip_doc)

    # INSERT INTO MONGODB
    if trips:
        trips_col.insert_many(trips)
    print(f"{len(trips)} trips inserted into MongoDB.")


# LOAD DATAFRAME
def load_dataframe():
    df = spark.read \
        .format("mongodb") \
        .schema(trip_schema) \
        .load()
    return df


# QUERY 2 IMPLEMENTATION
def query2_spark(trips_df):

    result = trips_df.groupBy(
        "user_id"
    ).agg(count("*").alias("num_trips"),
          avg((unix_timestamp(col("end_time"))-unix_timestamp(col("start_time"))
               ) / 60).alias("avg_duration_minutes"))
    return result


# INSERTION CONFIGURATIONS
user_sizes = [1000, 10000, 50000]
trip_sizes = [10000, 50000, 100000]
event_sizes = [0, 2, 5, 10]


# STORE BENCHMARK RESULTS
benchmark_results = []

# RUN ALL ISERTIONS
insertion_id = 1

for users in user_sizes:
    for trips in trip_sizes:
        for events in event_sizes:

            print("\n")
            print("#################################################")
            print(f"INSERTION {insertion_id}")
            print("#################################################")

            # GENERATE DATA
            generate_data(
                num_users=users,
                num_trips=trips,
                events_per_trip=events
            )

            # LOAD DATAFRAME
            trips_df = load_dataframe()

            # RUN QUERY 2
            start = time.perf_counter()
            result_df = query2_spark(trips_df)

            # FORCE EXECUTION
            result_count = result_df.count()
            end = time.perf_counter()
            execution_time = end - start

            # STORE RESULTS
            benchmark_results.append({
                "insertion": insertion_id,
                "users": users,
                "trips": trips,
                "events_per_trip": events,
                "rows_returned": result_count,
                "execution_time": round(
                    execution_time,
                    4
                )
            })

            # PRINT SCALABILITY RESULT
            print("\nSCALABILITY RESULT")
            print(
                f"Execution Time: "
                f"{execution_time:.4f} seconds"
            )

            print(
                f"Rows Returned: "
                f"{result_count}"
            )

            # DISPLAY ONLY 10 USERS
            print("\nTOP 10 USERS")
            result_df.orderBy(col("user_id")).show(10, truncate=False)
            insertion_id += 1


# FINAL SUMMARY
print("\n")
print("========================================================")
print("FINAL SCALABILITY EVALUATION")
print("========================================================")

for result in benchmark_results:
    print(
        f"Insertion {result['insertion']} | "
        f"Users={result['users']} | "
        f"Trips={result['trips']} | "
        f"Events/Trip={result['events_per_trip']} | "
        f"Rows={result['rows_returned']} | "
        f"Time={result['execution_time']} sec"
    )


spark.stop()
