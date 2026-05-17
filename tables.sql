
--TABLE CREATION

CREATE TABLE users (
    user_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    surname VARCHAR(50),
    birthdate TIMESTAMP,
    country_origin VARCHAR(100)
);


CREATE TABLE stations (
    station_id INT PRIMARY KEY,
    name VARCHAR(100),
    city VARCHAR(50),
    capacity INT
);



CREATE TABLE trips (
    trip_id INT PRIMARY KEY,

    user_id INT REFERENCES users(user_id),

    start_station INT REFERENCES stations(station_id),

    end_station INT REFERENCES stations(station_id),

    start_time TIMESTAMP,
    end_time TIMESTAMP,

    total_cost FLOAT
);


CREATE TABLE events (
    event_id INT PRIMARY KEY,

    trip_id INT REFERENCES trips(trip_id),

    event_type VARCHAR(100),

    event_time TIMESTAMP,

    event_value VARCHAR(100)
);


-- INDEXES

-- Speeds up joins and aggregations by user
CREATE INDEX idx_trips_user_id
ON trips(user_id);

-- Speeds up queries on start stations
CREATE INDEX idx_trips_start_station
ON trips(start_station);

-- Speeds up queries on end stations
CREATE INDEX idx_trips_end_station
ON trips(end_station);

-- Speeds up joins between events and trips
CREATE INDEX idx_events_trip_id
ON events(trip_id);

-- Speeds up filtering by event type
CREATE INDEX idx_events_event_type
ON events(event_type);

-- Composite index for filtering + joins
CREATE INDEX idx_events_type_trip
ON events(event_type, trip_id);

-- Useful for filtering stations by city
CREATE INDEX idx_stations_city
ON stations(city);