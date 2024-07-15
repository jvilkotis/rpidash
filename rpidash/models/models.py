# STDLIB
from datetime import datetime

# THIRD PARTY
from sqlalchemy import Column, DateTime, Integer, String

# FIRST PARTY
from rpidash.database import Base


class CPUTemperature(Base):
    """CPU temperature model."""
    __tablename__ = "cpu_temperature"
    id = Column(Integer, primary_key=True)
    temperature = Column(String(6))
    date = Column(DateTime())

    def __init__(self, temperature=None):
        self.temperature = temperature
        self.date = datetime.now()

    @staticmethod
    def get_value_key() -> str:
        """Return the key name for temperature value."""
        return "temperature"


class CPUUtilization(Base):
    """CPU utilization model."""
    __tablename__ = "cpu_utilization"
    id = Column(Integer, primary_key=True)
    percentage = Column(String(6))
    date = Column(DateTime())

    def __init__(self, percentage=None):
        self.percentage = percentage
        self.date = datetime.now()

    @staticmethod
    def get_value_key() -> str:
        """Return the key name for utilization percentage."""
        return "percentage"


class MemoryUtilization(Base):
    """Memory utilization model."""
    __tablename__ = "memory_utilization"
    id = Column(Integer, primary_key=True)
    percentage = Column(String(6))
    date = Column(DateTime())

    def __init__(self, percentage=None):
        self.percentage = percentage
        self.date = datetime.now()

    @staticmethod
    def get_value_key() -> str:
        """Return the key name for utilization percentage."""
        return "percentage"
