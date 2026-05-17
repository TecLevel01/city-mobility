from config_mongo import *
from pymongo import ASCENDING


# CREATE INDEXES
def create_indexes():

    # REMOVE OLD INDEXES
    users_col.drop_indexes()
    stations_col.drop_indexes()
    trips_col.drop_indexes()

    # USERS COLLECTION INDEXES
    users_col.create_index(
        [("country_origin", ASCENDING)],
        name="idx_country_origin"
    )

    # STATIONS COLLECTION INDEXES
    stations_col.create_index(
        [("city", ASCENDING)],
        name="idx_station_city"
    )

    # TRIPS COLLECTION INDEXES

    # Query 1 & Query 2
    trips_col.create_index(
        [("user_id", ASCENDING)],
        name="idx_user_id"
    )

    # Query 1 & Query 3
    trips_col.create_index(
        [("start_station", ASCENDING)],
        name="idx_start_station"
    )

    # Query 1 & Query 3
    trips_col.create_index(
        [("end_station", ASCENDING)],
        name="idx_end_station"
    )

    # Query 4 (embedded events)
    trips_col.create_index(
        [("events.event_type", ASCENDING)],
        name="idx_event_type"
    )

    # Compound index
    trips_col.create_index(
        [
            ("user_id", ASCENDING),
            ("start_station", ASCENDING)
        ],
        name="idx_user_station"
    )

    print("Indexes created successfully.")


# CLEAR COLLECTIONS
def clear_collections():
    users_col.delete_many({})
    stations_col.delete_many({})
    trips_col.delete_many({})


# INSERT USERS
def insert_users(users):
    if users:
        users_col.insert_many(users)


# INSERT STATIONS
def insert_stations(stations):
    if stations:
        stations_col.insert_many(stations)


# INSERT TRIPS WITH EMBEDDED EVENTS
def insert_trips_with_events(trips, events):

    # CREATE TRIPS MAP
    trips_map = {}

    for trip in trips:

        trip_doc = {

            "_id": trip["_id"],
            "user_id": trip["user_id"],
            "start_station": trip["start_station_id"],
            "end_station": trip["end_station_id"],
            "start_time": trip["start_time"],
            "end_time": trip["end_time"],
            "total_cost": trip["total_cost"],

            # EMBEDDED EVENTS ARRAY
            "events": []
        }

        trips_map[trip["_id"]] = trip_doc

    # EMBED EVENTS INTO CORRESPONDING TRIP
    for event in events:

        trip_id = event["trip_id"]
        event_doc = {

            "event_type": event["event_type"],
            "event_time": event["event_time"],
            "event_value": event["event_value"]
        }

        if trip_id in trips_map:
            trips_map[trip_id]["events"].append(event_doc)

    # CONVERT TO LIST
    final_trips = list(trips_map.values())

    # INSERT INTO MONGODB
    if final_trips:
        trips_col.insert_many(final_trips)

    print(f"{len(final_trips)} trips inserted successfully.")
