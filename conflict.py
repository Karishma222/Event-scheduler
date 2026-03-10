from models import Allocation, Event

def check_conflict(resource_id, start, end):

    allocations = Allocation.query.filter_by(resource_id=resource_id).all()

    for alloc in allocations:

        event = alloc.event

        if start < event.end_time and end > event.start_time:
            return True, f"Conflict with event {event.title}"

    return False, "No conflict"