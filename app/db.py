from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Replace 'sqlite:///:memory:' with your database connection string
engine = create_engine('sqlite:///:memory:', echo=False)

# Bind the engine to a sessionmaker
Session = sessionmaker(bind=engine)

# Function to initialize the database
def initialize_database():
    # Create tables based on the models
    Base.metadata.create_all(engine)

# Function to get a new session
def get_session():
    return Session()
