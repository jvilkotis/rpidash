# STDLIB
import unittest
from datetime import datetime

# FIRST PARTY
from rpidash import create_app
from rpidash.database import db_session
from rpidash.models.models import (
    CPUTemperature,
    CPUUtilization,
    MemoryUtilization,
)


class TestModels(unittest.TestCase):
    """A test suite for the database models."""

    @classmethod
    def setUpClass(cls):
        """Set up the test environment."""
        cls.app = create_app()
        cls.context = cls.app.app_context()
        cls.context.push()

    def tearDown(self):
        """Rollback uncommitted changes after each test if any."""
        db_session.rollback()

    @classmethod
    def tearDownClass(cls):
        """Tear down the test environment."""
        cls.context.pop()

    def test_create_and_query_cpu_temperature(self):
        """Test creating a CPUTemperature instance and querying it."""
        cpu_temp = CPUTemperature(temperature="49.00")
        db_session.add(cpu_temp)
        db_session.commit()
        result = db_session.query(CPUTemperature).filter_by(
            temperature="49.00",
        ).first()
        self.assertEqual(result.temperature, "49.00")
        self.assertIsInstance(result.date, datetime)

    def test_create_and_query_cpu_utilization(self):
        """Test creating a CPUUtilization instance and querying it."""
        cpu_percent = CPUUtilization(percentage="50.00")
        db_session.add(cpu_percent)
        db_session.commit()
        result = db_session.query(CPUUtilization).filter_by(
            percentage="50.00",
        ).first()
        self.assertEqual(result.percentage, "50.00")
        self.assertIsInstance(result.date, datetime)

    def test_create_and_query_memory_utilization(self):
        """Test creating a MemoryUtilization instance and querying it."""
        mempory_percent = MemoryUtilization(percentage="51.00")
        db_session.add(mempory_percent)
        db_session.commit()
        result = db_session.query(MemoryUtilization).filter_by(
            percentage="51.00",
        ).first()
        self.assertEqual(result.percentage, "51.00")
        self.assertIsInstance(result.date, datetime)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
