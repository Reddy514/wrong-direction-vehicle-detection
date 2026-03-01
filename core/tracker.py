from core.config import MAX_TRACK_HISTORY

class TrackerManager:
    def __init__(self):
        self.history = {}  # {track_id: [(cx, cy), ...]}
        self.logged_ids = set()

    def update(self, track_id, centroid):
        if track_id not in self.history:
            self.history[track_id] = []
        self.history[track_id].append(centroid)
        if len(self.history[track_id]) > MAX_TRACK_HISTORY:
            self.history[track_id].pop(0)

    def get_history(self, track_id):
        return self.history.get(track_id, [])

    def is_logged(self, track_id):
        return track_id in self.logged_ids

    def mark_logged(self, track_id):
        self.logged_ids.add(track_id)
