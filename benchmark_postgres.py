import time
from config import cur


def query1():
    cur.execute("""
        SELECT t.*, u.first_name, u.surname, s1.name, s2.name
        FROM trips t
        JOIN users u ON t.user_id = u.user_id
        JOIN stations s1 ON t.start_station = s1.station_id
        JOIN stations s2 ON t.end_station = s2.station_id;
    """)
    return cur.fetchall()


# -------------------------
def query2():
    cur.execute("""
        SELECT user_id,
               COUNT(*) AS trips,
               AVG(end_time - start_time) AS avg_duration
        FROM trips
        GROUP BY user_id;
    """)
    return cur.fetchall()


# -------------------------
def query3():
    cur.execute("""
        SELECT s.station_id, s.name,
            (SELECT COUNT(*) FROM trips t WHERE t.start_station = s.station_id) AS trips_starting,
            (SELECT COUNT(*) FROM trips t WHERE t.end_station = s.station_id) AS trips_ending
        FROM stations s;
    """)
    return cur.fetchall()


# -------------------------
def query4():
    cur.execute("""
        SELECT DISTINCT t.*, e.event_type
        FROM trips t
        JOIN events e ON t.trip_id = e.trip_id
        WHERE e.event_type = 'ERROR';
    """)
    return cur.fetchall()


# -------------------------
def measure_time(func):
    times = []

    start = time.perf_counter()
    func()
    end = time.perf_counter()
    times.append(end - start)

    return sum(times) / len(times)


# -------------------------
def run_all_queries():
    return {
        "Q1_time": measure_time(query1),
        "Q2_time": measure_time(query2),
        "Q3_time": measure_time(query3),
        "Q4_time": measure_time(query4)
    }
