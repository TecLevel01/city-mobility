from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
user = "neo4j"
password = "project1"

driver = GraphDatabase.driver(uri, auth=(user, password))


# INSERT USERS
# def insert_users(users):
#     with driver.session() as session:
#         for u in users:
#             session.run("""
#                 CREATE (u:User {
#                     user_id: $id,
#                     first_name: $fn,
#                     surname: $sn
#                 })
#             """, id=u[0], fn=u[1], sn=u[2])


# CLEAR DATABASE
def clear_neo4j():
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")


def insert_users_batch(users, batch_size=1000):
    with driver.session() as session:
        for i in range(0, len(users), batch_size):
            batch = users[i:i + batch_size]

            session.run("""
                UNWIND $users AS u
                CREATE (user:User {
                    user_id: u.user_id,
                    first_name: u.first_name,
                    surname: u.surname
                })
            """, users=[
                {
                    "user_id": u["_id"],
                    "first_name": u["first_name"],
                    "surname": u["surname"]
                } for u in batch
            ])


# INSERT STATIONS

def insert_stations_batch(stations, batch_size=1000):
    with driver.session() as session:
        for i in range(0, len(stations), batch_size):
            batch = stations[i:i + batch_size]

            session.run("""
                UNWIND $stations AS s
                CREATE (st:Station {
                    station_id: s.station_id,
                    name: s.name,
                    city: s.city
                })
            """, stations=[
                {
                    "station_id": s["_id"],
                    "name": s["name"],
                    "city": s["city"]
                } for s in batch
            ])


# INSERT STATIONS AND RELATIONSHIPS
def insert_trips_batch(trips, batch_size=1000):
    with driver.session() as session:
        for i in range(0, len(trips), batch_size):
            batch = trips[i:i + batch_size]

            session.run("""
                UNWIND $trips AS t

                MATCH (u:User {user_id: t.user_id})
                MATCH (s1:Station {station_id: t.start_station})
                MATCH (s2:Station {station_id: t.end_station})

                CREATE (trip:Trip {
                    trip_id: t.trip_id,
                    start_time: t.start_time,
                    end_time: t.end_time
                })

                CREATE (u)-[:PERFORMED]->(trip)
                CREATE (trip)-[:STARTS_AT]->(s1)
                CREATE (trip)-[:ENDS_AT]->(s2)
            """, trips=[
                {
                    "trip_id": t["_id"],
                    "user_id": t["user_id"],
                    "start_station": t["start_station_id"],
                    "end_station": t["end_station_id"],
                    "start_time": t["start_time"],
                    "end_time": t["end_time"]
                } for t in batch
            ])


# INSERT EVENTS
# def insert_events_batch(events, batch_size=1000
#                         ):
#     with driver.session() as session:
#         for i in range(
#             0,
#             len(events),
#             batch_size
#         ):
#             batch = events[
#                 i:i + batch_size
#             ]
#             session.run("""
#                 UNWIND $events AS e
#                 MATCH (t:Trip {
#                     trip_id: e.trip_id
#                 })
#                 CREATE (ev:Event {
#                     event_id: e.event_id,
#                     event_type: e.event_type,
#                     event_time: e.event_time,
#                     event_value: e.event_value
#                 })
#                 CREATE (t)-[:HAS_EVENT]->(ev)
#             """, events=[
#                 {
#                     "event_id": e["_id"],
#                     "trip_id": e["trip_id"],
#                     "event_type": e["event_type"],
#                     "event_time": e["event_time"],
#                     "event_value": e["event_value"]
#                 }
#                 for e in batch
#             ])
