# STDLIB
import datetime

# THIRD PARTY
from sqlalchemy import Column, DateTime, Integer, String

# FIRST PARTY
from rpidash.database import Base


class CPUTemperature(Base):  # pylint: disable=too-few-public-methods
    """CPU temperature model."""
    __tablename__ = 'cpu_temperature'
    id = Column(Integer, primary_key=True)
    temperature = Column(String(50))
    date = Column(DateTime())

    def __init__(self, temperature=None):
        self.temperature = temperature
        self.date = datetime.datetime.now()


class CPUUtilization(Base):  # pylint: disable=too-few-public-methods
    """CPU utilization model."""
    __tablename__ = 'cpu_utilization'
    id = Column(Integer, primary_key=True)
    percentage = Column(String(50))
    date = Column(DateTime())

    def __init__(self, percentage=None):
        self.percentage = percentage
        self.date = datetime.datetime.now()


class MemoryUtilization(Base):  # pylint: disable=too-few-public-methods
    """Memory utilization model."""
    __tablename__ = 'memory_utilization'
    id = Column(Integer, primary_key=True)
    percentage = Column(String(50))
    date = Column(DateTime())

    def __init__(self, percentage=None):
        self.percentage = percentage
        self.date = datetime.datetime.now()
