import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from conf.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
import os

from dotenv import load_dotenv

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT 

from dotenv import load_dotenv


print(DB_HOST)
print(DB_PORT)
print(DB_NAME)
print(DB_USER)
print(DB_PASSWORD)


# Connect using psycopg2
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)



# Create SQLAlchemy engine
#engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Create a session using SQLAlchemy
#Session = sessionmaker(bind=engine)
#session = Session()

# Perform database operations
# ...


conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) 

pgcursor = conn.cursor()

# retrive data 
pgcursor.execute('select * from fitness.nutrition_daily nd')

for row in pgcursor.fetchall():
    print(row)

# Close the connection/session when done
#session.close()
conn.close()