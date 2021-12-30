import datetime
import dateutil.rrule as dr
import dateutil.parser as dp
import logging

from typing import Dict

from waste_collection_schedule import Collection  # type: ignore[attr-defined]

TITLE = "Waste Collection"
DESCRIPTION = "List of upcoming waste collection dates"
URL = None
TEST_CASES: Dict[str, Dict[str, str]] = {}

_LOGGER = logging.getLogger(__name__)


class Source:
    def __init__(self, collections=[]):
        self._collections = []
        for coll in collections:
            interval_type = getattr(dr, coll['interval_type'], None)
            if not interval_type:
                _LOGGER.error('interval_type specified is invalid: %s' % coll['interval_type'])
                raise('Error: interval_type invalid: %s' % coll['interval_type'])
            self._collections.append({
                'name': coll['name'],
                'sched': dr.rrule(
                    dtstart=coll.get('start_date', datetime.date.today()),
                    freq=interval_type,
                    interval=coll['interval'],
                    until=datetime.date(datetime.datetime.today().year+1,12,31),
                )
            })


    def fetch(self):
        this_date = datetime.datetime.now().date()

        entries = []

        for c in self._collections:
            for d in c['sched']:
                entries.append(
                    Collection(
                        d.date(),
                        c['name'],
                    )
                )
        return entries


