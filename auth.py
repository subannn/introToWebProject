import uuid
import time
import threading
import datetime

class Auth:
    sessions = {}

    def __init__(self):
        thread = threading.Thread(target=self._clear_sessions_daily, daemon=True)
        thread.start()

    def _clear_sessions_daily(self):
        while True:
            now = datetime.datetime.now()
            next_midnight = (now + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
            seconds_until_midnight = (next_midnight - now).total_seconds()
            time.sleep(seconds_until_midnight)
            Auth.sessions.clear()

    def login(self, user_name, user_id):
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {"user_name": user_name, "user_id": user_id}
        return session_id

    def logout(self, session_id):
        for session in self.sessions:
            print(session)
        self.sessions.pop(session_id)
        print("Logged out")
        for session in self.sessions:
            print(session)

    def check_session(self, session_id):
        return session_id in self.sessions

    def get_user_id(self, session_id):
        return self.sessions[session_id]["user_id"]