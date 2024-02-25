# STDLIB
import datetime
import inspect
import logging

# THIRD PARTY
from flask_apscheduler import APScheduler

# FIRST PARTY
from rpidash import models
from rpidash.database import db_session
from rpidash.models import CPUTemperature, CPUUtilization, MemoryUtilization
from rpidash.utils import (
    get_cpu_percentage,
    get_cpu_temperature,
    get_memory_utilization,
    load_app_config,
)

logging.getLogger("apscheduler").setLevel(logging.WARNING)

scheduler = APScheduler()

config = load_app_config()


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


@scheduler.task(
    "interval",
    id="delete_old_records",
    seconds=config["RECORD_DELETE_INTERVAL"],
)
def delete_old_records():
    """Delete records older than the configured date."""
    for _, model in inspect.getmembers(models):
        if inspect.isclass(model) and model.__module__ == models.__name__:
            cutoff_date = datetime.datetime.now() - datetime.timedelta(
                seconds=config["DELETE_RECORDS_OLDER_THAN"]
            )
            records_to_delete = model.query.filter(
                model.date < cutoff_date
            ).delete()
            logging.info(
                "Deleting %s records from %s table older than %s",
                records_to_delete,
                model.__tablename__,
                cutoff_date,
            )
            db_session.commit()
