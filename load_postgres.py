from config import cur, myConnect


# CLEAR TABLES
def clear_tables():
    cur.execute("TRUNCATE events, trips, stations, users CASCADE;")
    myConnect.commit()


# INSERT USERS
def insert_users(users):
    users_tuples = [
        (
            u["_id"],
            u["first_name"],
            u["surname"],
            u["birthdate"],
            u["country_origin"]
        )
        for u in users
    ]

    cur.executemany("""
        INSERT INTO users (user_id, first_name, surname, birthdate, country_origin)
        VALUES (%s, %s, %s, %s, %s)
    """, users_tuples)

    myConnect.commit()


# INSERT STATIONS
def insert_stations(stations):
    stations_tuples = [
        (
            s["_id"],
            s["name"],
            s["city"],
            s["capacity"]
        )
        for s in stations
    ]

    cur.executemany("""
        INSERT INTO stations (station_id, name, city, capacity)
        VALUES (%s, %s, %s, %s)
    """, stations_tuples)

    myConnect.commit()


# INSERT TRIPS
def insert_trips(trips):
    trips_tuples = [
        (
            t["_id"],
            t["user_id"],
            t["start_station_id"],
            t["end_station_id"],
            t["start_time"],
            t["end_time"],
            t["total_cost"]
        )
        for t in trips
    ]

    cur.executemany("""
        INSERT INTO trips (trip_id, user_id, start_station, end_station, start_time, end_time, total_cost)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, trips_tuples)

    myConnect.commit()


# INSERT EVENTS
def insert_events(events):
    events_tuples = [
        (
            e["_id"],
            e["trip_id"],
            e["event_type"],
            e["event_time"],
            e["event_value"]
        )
        for e in events
    ]

    cur.executemany("""
        INSERT INTO events (event_id, trip_id, event_type, event_time, event_value)
        VALUES (%s, %s, %s, %s, %s)
    """, events_tuples)

    myConnect.commit()
