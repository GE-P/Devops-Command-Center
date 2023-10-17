# Name : Devops_Command_Center
# Version : Alpha
# Author : Gerhard Eibl
# INFO : The Database script creator.
# ----------------------------------- #

import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# The function to connect with the DB.
def get_db_connection():
    conn = psycopg2.connect(host=os.getenv('HOST'),
                            database=os.getenv('DB'),
                            user=os.getenv('USER'),
                            password=os.getenv('PSW'))
    return conn


# Connect to the DB
conn = get_db_connection()
# Open a cursor
cur = conn.cursor()

# Execute command to create users table
cur.execute('DROP TABLE IF EXISTS users;')
cur.execute('CREATE TABLE users (id serial PRIMARY KEY,'
            'fullname VARCHAR ( 100 ) NOT NULL,'
            'username VARCHAR ( 50 ) NOT NULL,'
            'password VARCHAR ( 255 ) NOT NULL,'
            'email VARCHAR ( 50 ) NOT NULL,'
            'date_added date DEFAULT CURRENT_TIMESTAMP);')

# Execute command to create projects table
cur.execute('DROP TABLE IF EXISTS projects;')
cur.execute('CREATE TABLE projects (project_id serial PRIMARY KEY,'
            'project_name VARCHAR ( 255 ) NOT NULL,'
            'project_cicd BOOLEAN NOT NULL,'
            'project_url VARCHAR ( 255 ) NOT NULL,'
            'date_added date DEFAULT CURRENT_TIMESTAMP);')

# Execute command to create metrics table
cur.execute('DROP TABLE IF EXISTS metrics;')
cur.execute('CREATE TABLE metrics (metric_id serial PRIMARY KEY,'
            'date_exec DATE NOT NULL,'
            'time_exec INTEGER NOT NULL,'
            'ref_key INTEGER NOT NULL,'
            'date_added date DEFAULT CURRENT_TIMESTAMP);')

cur.execute('ALTER TABLE metrics ADD CONSTRAINT "metric_fk" FOREIGN KEY ("ref_key") REFERENCES "projects" ("project_id");')

# Save the changes
conn.commit()
# Close the cursor
cur.close()
# Close the DB connection
conn.close()
