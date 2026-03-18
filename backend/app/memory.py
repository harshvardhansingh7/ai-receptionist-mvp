sessions = {}

def get_session(session_id):
    if session_id not in sessions:
        sessions[session_id] = {
            "messages": [],
            "data": {
                "name": None,
                "date": None,
                "time": None,
                "purpose": None
            }
        }
    return sessions[session_id]

def reset_session(session_id):
    sessions.pop(session_id, None)