import time
from neo4j import GraphDatabase


# CONNECTION
URI = "bolt://localhost:7687"
USER = "neo4j"
PASSWORD = "project1"

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))


# QUERY 1
def query1(user_id):
    with driver.session() as session:
        result = session.run("""
            MATCH (u:User {user_id: $user_id})-[:PERFORMED]->(t:Trip)
            MATCH (t)-[:STARTS_AT|ENDS_AT]->(s:Station)
            RETURN DISTINCT s.name
        """, user_id=user_id)

        return list(result)


# QUERY 2
def query2():
    with driver.session() as session:
        result = session.run("""
            MATCH (s:Station)
            OPTIONAL MATCH (s)<-[:STARTS_AT]-(t1:Trip)
            OPTIONAL MATCH (s)<-[:ENDS_AT]-(t2:Trip)

            WITH s,
                 COUNT(DISTINCT t1) AS outgoing,
                 COUNT(DISTINCT t2) AS incoming

            RETURN s.name, (incoming + outgoing) AS total_trips
            ORDER BY total_trips DESC
            LIMIT 3
        """)

        return list(result)


# TIMER FUNCTION
def measure(func, *args):
    start = time.perf_counter()
    func(*args)
    end = time.perf_counter()
    return end - start


# RUN BENCHMARK
def run_benchmark(n_users):

    print("\nNeo4j Query Benchmark")

    # pick a valid user (e.g., middle one)
    test_user_id = n_users // 2

    q1_time = measure(query1, test_user_id)
    print(f"Query 1 (reachable stations) time: {q1_time:.4f} sec")

    q2_time = measure(query2)
    print(f"Query 2 (top stations) time: {q2_time:.4f} sec")

    return q1_time, q2_time
