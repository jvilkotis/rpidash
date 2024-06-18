# STDLIB
import inspect
import logging
from datetime import datetime, timedelta

# THIRD PARTY
from flask_apscheduler import APScheduler

# FIRST PARTY
from rpidash import models
from rpidash.database import db_session
from rpidash.models import CPUTemperature, CPUUtilization, MemoryUtilization
from rpidash.system_utilization import SystemUtilization
from rpidash.utils import load_app_config

logging.getLogger("apscheduler").setLevel(logging.WARNING)

scheduler = APScheduler()

config = load_app_config()
intervals = config["scheduled_tasks"]["intervals"]


@scheduler.task(
    "interval",
    id="record_cpu_temperature",
    seconds=intervals["cpu_temperature"],
)
def record_cpu_temperature():
    """Get CPU temperature and store it in the DB."""
    reading = SystemUtilization().get_cpu_temperature().cpu_temperature
    if reading:
        logging.info("Storing CPU temperature: %s °C", reading)
        cpu_temperature = CPUTemperature(temperature=reading)
        db_session.add(cpu_temperature)
        db_session.commit()


@scheduler.task(
    "interval",
    id="record_cpu_percentage",
    seconds=intervals["cpu_percentage"],
)
def record_cpu_percentage():
    """Get CPU utilization percentage and store it in the DB."""
    reading = SystemUtilization().get_cpu_percentage().cpu_percentage
    if reading:
        logging.info("Storing CPU utilization: %s%%", reading)
        cpu_utilization = CPUUtilization(percentage=reading)
        db_session.add(cpu_utilization)
        db_session.commit()


@scheduler.task(
    "interval",
    id="record_memory_utilization",
    seconds=intervals["memory_percentage"],
)
def record_memory_utilization():
    """Get memory utilization percentage and store it in the DB."""
    reading = SystemUtilization().get_memory_utilization().memory_percentage
    logging.info("Storing memory utilization: %s%%", reading)
    memory_utilization = MemoryUtilization(percentage=reading)
    db_session.add(memory_utilization)
    db_session.commit()


@scheduler.task(
    "interval",
    id="delete_old_records",
    seconds=intervals["deletion"],
)
def delete_old_records():
    """Delete records older than the configured date."""
    delete_config = config["scheduled_tasks"]["deletion"]
    if not delete_config["enabled"]:
        return
    for _, model in inspect.getmembers(models):
        if inspect.isclass(model) and model.__module__ == models.__name__:
            cutoff_date = datetime.now() - timedelta(
                seconds=delete_config["delete_older_than"]
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
