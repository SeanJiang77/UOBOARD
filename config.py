import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_very_secure_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URL') or \
        'postgresql://uoboard_user:your_password@dpg-crje8rv2p9s7s83j2pt0-a.oregon-postgres.render.com:5432/uoboard?sslmode=require'
    SQLALCHEMY_TRACK_MODIFICATIONS = False