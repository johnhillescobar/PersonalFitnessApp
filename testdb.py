import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from conf.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

# Connect using psycopg2
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

# Create SQLAlchemy engine
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Create a session using SQLAlchemy
Session = sessionmaker(bind=engine)
session = Session()

# Perform database operations
# ...

# Close the connection/session when done
session.close()
conn.close()