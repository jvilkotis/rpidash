# STDLIB
import logging

# THIRD PARTY
import yaml
from flask_apscheduler import APScheduler

# FIRST PARTY
from rpidash.database import db_session
from rpidash.models import CPUTemperature, CPUUtilization, MemoryUtilization
from rpidash.utils import (
    get_cpu_percentage,
    get_cpu_temperature,
    get_memory_utilization,
)

scheduler = APScheduler()

with open("rpidash/config.yaml", encoding="utf-8") as f:
    config = yaml.safe_load(f)


@scheduler.task(
    "interval",
    id="record_cpu_temperature",
    seconds=config["CPU_TEMPERATURE_RECORD_INTERVAL"],
)
def record_cpu_temperature():
    """Get CPU temperature and store it in the DB."""
    reading = get_cpu_temperature()
    if reading:
        logging.info("Storing CPU temperature: %s °C", reading)
        cpu_temperature = CPUTemperature(temperature=reading)
        db_session.add(cpu_temperature)
        db_session.commit()


@scheduler.task(
    "interval",
    id="record_cpu_percentage",
    seconds=config["CPU_PERCENTAGE_RECORD_INTERVAL"],
)
def record_cpu_percentage():
    """Get CPU utilization percentage and store it in the DB."""
    reading = get_cpu_percentage()
    if reading:
        logging.info("Storing CPU utilization: %s%%", reading)
        cpu_utilization = CPUUtilization(percentage=reading)
        db_session.add(cpu_utilization)
        db_session.commit()


@scheduler.task(
    "interval",
    id="record_memory_utilization",
    seconds=config["MEMORY_PERCENTAGE_RECORD_INTERVAL"],
)
def record_memory_utilization():
    """Get memory utilization percentage and store it in the DB."""
    reading, _, _ = get_memory_utilization()
    logging.info("Storing memory utilization: %s%%", reading)
    memory_utilization = MemoryUtilization(percentage=reading)
    db_session.add(memory_utilization)
    db_session.commit()
