# city-mobility
Data Management Project in PostgreSQL, MongoDB and Neo4j using Python and PySpark library.


1. Databases Creation

PostgreSQL:
	- create a database called "project". 
	- Find the script called "coing.py" in the project folder and input your database credentials(user, port, host, password)
MongoDB:
	- create a connection (you can name it "project") and make sure your database name is "cityMobility"
	- open the script "config_mongo.py" and make sure your mongo client host correspond to the one of your database you have just created (cityMobility).
Neo4j:
	- Open Neo4j on your computer and create an instance of your choice (preferably "project").
	- Open the script called "load_neo4j.py" and make sure the credentials uri, user (most cases the user is "neo4j") and password are correct for your created database.

Spark deployment:
	- Find two folders one called "spark-jars" and another called "tmp" in the project folder, Copy these two folders and paste them in your C: driver (C:\spark-jars and C:\tmp)

The main reason for creating these two folders there was practicality and compatibility with Spark on Windows. Spark requires the GraphFrames JAR file to be loaded through a 	filesystem path. On Windows, using a short and simple path such as: C:\spark-jars\
This helps avoid common issues related to: spaces in folder names, permission restrictions, path escaping problems, Hadoop/Spark filesystem parsing errors.
For example in my case, space in folder name: C:\Users\Admin\Documents\Data Management\
	
If the path of these folders is changed, please make sure to also change the path in the spark_graph.py file, under the lines of code that create spark session.
You will see on the top of the source code:
# SPARK SESSION
#GRAPHFRAMES
.config(
      "spark.jars",
      "file:///C:/spark-jars/graphframes-0.8.3-spark3.5-s_2.12.jar,"
      "file:///C:/spark-jars/neo4j-connector-apache-spark_2.12-5.3.1_for_spark_3.jar")

2. Files and their purpose:
	1. config files(config.py and config_mongo.py): for connection your scripts to your databases. Therefore, make sure to input correct database credential in these files otherwise the 	scripts will fail to run.

	2. data_generator.py file: this file is responsible for generating our simulated data. It is connected to load files(load_postgres.py, load_mongo.py and load_neo4j.py). this file 	runs together with load files when we run the main files.

	3. main files(main_postgreSQL.py, main_mongo.py and main_neo4j.py): (all files starting with the word "main"): for each database these are the file you have to run on your IDE 	terminal.

	4. plot_results.py file: after running the main files for mongoDB(main_mongo.py) and postgreSQL(main_postgres.py) you can now run this file to produce our polts showing the 	perfomances of our queries
	
	5. load files(load_postgres.py, load_mongo.py and load_neo4j.py): these files are responsible for inserting our generated data to the database. these file run when we run main 	files.
	
	6. benchmark files (benchmark_postgres.py, benchmark_mongo.py and benchmark_neo4j.py): these files have our queries that run when you run the main files and return for us results 	(printed on the terminal or saved in csv files).

	7. spark files(spark_q2mongo.py and spark_graph.py): run these files on your terminal to see you query spark-based implementation and scalability analysis were done using spark.


3. Commands for installing libraries used:
pip install pandas
pip install faker
pip install pymongo
pip install neo4j
pip install pyspark
pip install graphframes
pip install matplotlib
pip install psycopg2-binary
Java JDK 17
Hadoop winutils.exe
	

