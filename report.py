from models import Allocation, Event
from datetime import datetime


def resource_utilisation(start_date, end_date):

    allocations = Allocation.query.all()

    result = []

    for a in allocations:

        event = a.event

        if event.start_time >= start_date and event.end_time <= end_date:

            result.append({
                "event": event.title,
                "resource": a.resource.name,
                "start": event.start_time,
                "end": event.end_time
            })

    return result