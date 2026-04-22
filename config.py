import os

class Config:
    # --- Database ---
    # Format: mysql+pymysql://user:password@host:port/dbname
    # Override by setting the DATABASE_URL environment variable
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'mysql+pymysql://root:password@localhost:3306/BakeryManagementDB'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- General ---
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    JSON_SORT_KEYS = False
