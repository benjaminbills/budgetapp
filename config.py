import os
import re

class Config:
  '''
  General configuration parent class
  '''

class ProdConfig(Config):
  """
  Production  configuration child class

  Args:
      Config: The parent configuration class with General configuration settings
  """
  pass

class DevConfig(Config):
    """
    Development  configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    """
    # SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://obafemi:Bentamjay1@localhost/pitches'

    DEBUG = True

class TestConfig(Config):
    # SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://obafemi:Bentamjay1@localhost/pitches_test'

config_options = {"development": DevConfig, "production": ProdConfig, 'test':TestConfig}
