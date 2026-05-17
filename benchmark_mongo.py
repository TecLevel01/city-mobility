import time
from config_mongo import db


def query1():
    return list(db.trips.aggregate([
        {
            "$lookup": {
                "from": "users",
                "localField": "user_id",
                "foreignField": "_id",
                "as": "user"
            }
        },
        {
            "$lookup": {
                "from": "stations",
                "localField": "start_station",
                "foreignField": "_id",
                "as": "start_station"
            }
        },
        {
            "$lookup": {
                "from": "stations",
                "localField": "end_station",
                "foreignField": "_id",
                "as": "end_station"
            }
        },
        {"$unwind": "$user"},
        {"$unwind": "$start_station"},
        {"$unwind": "$end_station"},
        {
            "$project": {
                "start_time": 1,
                "end_time": 1,
                "total_cost": 1,
                "user.first_name": 1,
                "user.surname": 1,
                "start_station.name": 1,
                "end_station.name": 1
            }
        }
    ]))


# -------------------------
def query2():
    return list(db.trips.aggregate([
        {
            "$group": {
                "_id": "$user_id",
                "num_trips": {"$sum": 1},
                "avg_duration": {
                    "$avg": {
                        "$divide": [
                            {"$subtract": ["$end_time", "$start_time"]},
                            60000
                        ]
                    }
                }
            }
        }
    ]))


# -------------------------
def query3():
    return list(db.stations.aggregate([
        {
            "$lookup": {
                "from": "trips",
                "localField": "_id",
                "foreignField": "start_station",
                "as": "starting_trips"
            }
        },
        {
            "$lookup": {
                "from": "trips",
                "localField": "_id",
                "foreignField": "end_station",
                "as": "ending_trips"
            }
        },
        {
            "$project": {
                "name": 1,
                "trips_starting": {"$size": "$starting_trips"},
                "trips_ending": {"$size": "$ending_trips"}
            }
        }
    ]))


# -------------------------
def query4():
    return list(db.trips.aggregate([
        {
            "$lookup": {
                "from": "events",
                "localField": "_id",
                "foreignField": "trip_id",
                "as": "events"
            }
        },
        {
            "$match": {
                "events.event_type": "ERROR"
            }
        }
    ]))


# TIMING FUNCTION
def measure_time(func):
    start = time.perf_counter()
    func()
    end = time.perf_counter()
    return end - start


# RUN ALL QUERIES
def run_all_queries():
    return {
        "Q1_time": measure_time(query1),
        "Q2_time": measure_time(query2),
        "Q3_time": measure_time(query3),
        "Q4_time": measure_time(query4)
    }
