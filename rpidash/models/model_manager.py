# STDLIB
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Type, Union

# FIRST PARTY
from rpidash.database import db_session
from rpidash.models.models import (
    CPUTemperature,
    CPUUtilization,
    MemoryUtilization,
)


class ModelManager:
    """Model manager for handling database operations."""

    def __init__(self, table_name: Optional[str] = None):
        if table_name:
            self.model = self.get_model(table_name)
            self.value_key = self.model.get_value_key()

    @staticmethod
    def get_models() -> Dict[str, Type[Union[
        CPUTemperature,
        CPUUtilization,
        MemoryUtilization,
    ]]]:
        """Return a dictionary of table names to model classes."""
        return {
            CPUTemperature.__tablename__: CPUTemperature,
            CPUUtilization.__tablename__: CPUUtilization,
            MemoryUtilization.__tablename__: MemoryUtilization,
        }

    def get_model(self, table_name: str) -> Type[Union[
        CPUTemperature,
        CPUUtilization,
        MemoryUtilization,
    ]]:
        """Return the model class for the given table name."""
        try:
            return self.get_models()[table_name]
        except KeyError as exc:
            raise ValueError(
                f"Model for table '{table_name}' not found."
            ) from exc

    def retrieve_data(
        self,
        recorded_after: Optional[str] = None,
    ) -> Dict[str, List[str]]:
        """Retrieve data from the database, optionally filtered by date."""
        query = self.model.query
        if recorded_after:
            try:
                recorded_after_dt = datetime.strptime(
                    recorded_after,
                    "%Y-%m-%dT%H:%M:%S",
                )
                query = query.filter(self.model.date > recorded_after_dt)
            except ValueError as exc:
                raise ValueError(
                    "The 'recorded_after' parameter must be in the format"
                    " 'YYYY-MM-DDTHH:MM:SS'"
                ) from exc
        data = query.all()

        values = []
        dates = []
        for item in data:
            values.append(getattr(item, self.value_key))
            dates.append(item.date.strftime("%Y-%m-%dT%H:%M:%S"))

        return {"values": values, "dates": dates}

    def store_record(self, reading: int) -> None:
        """Store a new record in the database."""
        instance = self.model()
        setattr(instance, self.value_key, reading)
        db_session.add(instance)
        logging.info("Storing %s: %s%%", self.model.__tablename__, reading)
        db_session.commit()

    def delete_records(self, older_than: int) -> None:
        """Delete records older than the specified number of seconds."""
        cutoff_date = datetime.now() - timedelta(seconds=older_than)
        for model in self.get_models().values():
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
