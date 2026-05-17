import random
from faker import Faker
from datetime import timedelta, datetime

fake = Faker()

# ITALIAN CITIES
ITALIAN_CITIES = [
    "Milan", "Rome", "Naples", "Turin", "Palermo",
    "Genoa", "Bologna", "Florence", "Bari", "Catania",
    "Venice", "Verona", "Messina", "Padua", "Trieste",
    "Monza", "Bergamo", "Brescia", "Como", "Varese", "Pavia"
]


# USERS
def generate_users(n):
    return [
        {
            "_id": i,
            "first_name": fake.first_name(),
            "surname": fake.last_name(),
            "birthdate": datetime.combine(
                fake.date_of_birth(minimum_age=18, maximum_age=70),
                datetime.min.time()
            ),
            "country_origin": fake.country()
        }
        for i in range(n)
    ]


# STATIONS
def generate_stations(n):
    stations = []

    for i in range(n):
        city = random.choice(ITALIAN_CITIES)
        stations.append({
            "_id": i,
            "name": f"{fake.street_name()} Station - {city}",
            "city": city,
            "capacity": random.randint(10, 50)
        })
    return stations


# TRIPS (NO EVENTS HERE)
def generate_trips(n_trips, n_users, n_stations):
    trips = []
    for i in range(n_trips):
        start_time = fake.date_time_this_year()
        end_time = start_time + timedelta(minutes=random.randint(5, 60))

        trips.append({
            "_id": i,
            "user_id": random.randint(0, n_users - 1),
            "start_station_id": random.randint(0, n_stations - 1),
            "end_station_id": random.randint(0, n_stations - 1),
            "start_time": start_time,
            "end_time": end_time,
            "total_cost": round(random.uniform(1, 10), 2)
        })

    return trips


# EVENTS (SEPARATE)
EVENT_VALUES = {
    "GPS": ["no signal", "weak signal", "low accuracy"],
    "ERROR": ["system crash", "sensor malfunction"],
    "BATTERY": ["low battery (20%)", "critical battery (5%)"],
    "DELAY": ["heavy rain", "traffic congestion"]
}


def generate_events(trips, events_per_trip):
    events = []
    event_id = 0

    for trip in trips:
        for _ in range(events_per_trip):

            event_type = random.choice(list(EVENT_VALUES.keys()))
            event_value = random.choice(EVENT_VALUES[event_type])

            events.append({
                "_id": event_id,
                "trip_id": trip["_id"],
                "event_type": event_type,
                "event_time": fake.date_time_between(
                    start_date=trip["start_time"],
                    end_date=trip["end_time"]
                ),
                "event_value": event_value
            })

            event_id += 1

    return events
