from src.Session import Session

import sessions

def get_or_create_session(session_id: int) -> Session:
    if session_id not in sessions.sessions:
        sessions.sessions[session_id] = Session(session_id)
    return sessions.sessions[session_id]


def close_session(session_id: int) -> None:
    if session_id in sessions.sessions:
        del sessions.sessions[session_id]


def reset_sessions() -> None:
    sessions.sessions = {}
