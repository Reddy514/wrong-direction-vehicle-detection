from collections import defaultdict
from core.config import MAX_TRACK_HISTORY

class TrackerManager:
    def __init__(self):
        # Dictionary to store vehicle track history (id -> list of centroids)
        self.track_history = defaultdict(list)
        # Store IDs already logged to avoid spamming the database per frame
        self.violation_logged = set()

    def update(self, track_id, centroid):
        """Update centroid history for a given track ID."""
        self.track_history[track_id].append(centroid)
        
        # Keep only recent history to avoid memory bloat
        if len(self.track_history[track_id]) > MAX_TRACK_HISTORY:
            self.track_history[track_id].pop(0)

    def get_history(self, track_id):
        """Get the track history for a specific ID."""
        return self.track_history.get(track_id, [])

    def is_logged(self, track_id):
        """Check if violation has already been logged for this track ID."""
        return track_id in self.violation_logged

    def mark_logged(self, track_id):
        """Mark a track ID as logged."""
        self.violation_logged.add(track_id)
