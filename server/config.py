import os

class Config:
    # Get the directory of the current file (config.py)
    basedir = os.path.abspath(os.path.dirname(__file__))
    
    # Create a path for the instance folder
    instance_path = os.path.join(basedir, 'instance')
    
    # Ensure the instance folder exists
    os.makedirs(instance_path, exist_ok=True)
    
    # Set the database URI to use the instance folder
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(instance_path, 'Prestige_Properties.db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'my-secret-key'