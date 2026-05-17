import time
from pyspark.sql import SparkSession
from graphframes import GraphFrame


# SPARK SESSION
spark = (
    SparkSession.builder
    .appName("Neo4jGraphFramesBenchmark")

    # GRAPHFRAMES
    .config(
        "spark.jars",
        "file:///C:/spark-jars/graphframes-0.8.3-spark3.5-s_2.12.jar,"
        "file:///C:/spark-jars/neo4j-connector-apache-spark_2.12-5.3.1_for_spark_3.jar"
    ).config(
        "spark.serializer", "org.apache.spark.serializer.KryoSerializer"
    ).getOrCreate())

spark.sparkContext.setLogLevel("ERROR")


# NEO4J CONNECTION
NEO4J_URL = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "project1"


# LOAD STATIONS FROM NEO4J
stations_df = (
    spark.read
    .format("org.neo4j.spark.DataSource")
    .option("url", NEO4J_URL)
    .option("authentication.type", "basic")
    .option("authentication.basic.username", NEO4J_USER)
    .option("authentication.basic.password", NEO4J_PASSWORD)
    .option(
        "query",
        """
        MATCH (s:Station)
        RETURN s.station_id AS id,
               s.name AS name
        """
    ).load())


# LOAD TRIPS AS EDGES
edges_df = (
    spark.read
    .format("org.neo4j.spark.DataSource")
    .option("url", NEO4J_URL)
    .option("authentication.type", "basic")
    .option("authentication.basic.username", NEO4J_USER)
    .option("authentication.basic.password", NEO4J_PASSWORD)
    .option(
        "query",
        """
        MATCH (t:Trip)-[:STARTS_AT]->(s1:Station)
        MATCH (t)-[:ENDS_AT]->(s2:Station)

        RETURN s1.station_id AS src,
               s2.station_id AS dst
        """
    ).load()
)


# CACHE DATA
stations_df.cache()
edges_df.cache()


# BUILD GRAPHFRAME
g = GraphFrame(stations_df, edges_df)


# QUERY 1: PAGERANK

print("\n================================================")
print("QUERY 1: PAGERANK")
print("================================================")
start = time.perf_counter()

pagerank = g.pageRank(resetProbability=0.15, maxIter=10)
top3 = (pagerank.vertices.select("id", "name",
        "pagerank").orderBy("pagerank", ascending=False))
top3.show(3, truncate=False)

end = time.perf_counter()
pagerank_time = end - start
print(f"\nPageRank Execution Time: {pagerank_time:.4f} seconds")


# QUERY 2: CONNECTED COMPONENTS
print("\n================================================")
print("QUERY 2: CONNECTED COMPONENTS")
print("================================================")

# REQUIRED FOR CONNECTED COMPONENTS
spark.sparkContext.setCheckpointDir("file:///C:/tmp/checkpoints")

start = time.perf_counter()

# HADOOP CAN'T ACCESS NATIVE FILESYSTEM WELLL ON WINDOWS OS
# -----------------------------------------------------------

# components = g.connectedComponents()

# components.select("id", "component") \
#     .orderBy("component") \
#     .show(50, truncate=False)


# LABELPROPAGATION WORKS ON WINDOWS
lp = g.labelPropagation(maxIter=10)

lp.select("id", "label") \
    .orderBy("label", "id") \
    .show(50, truncate=False)

end = time.perf_counter()
components_time = end - start

print(
    f"\nConnected Components Execution Time: "
    f"{components_time:.4f} seconds")


print("\n================================================")
print("SCALABILITY RESULTS")
print("================================================")

print(f"Stations: {stations_df.count()}")
print(f"Edges (Trips): {edges_df.count()}")
print(f"PageRank Time: {pagerank_time:.4f} sec")
print(
    f"Connected Components Time: "
    f"{components_time:.4f} sec\n\n\n\n")


spark.stop()
