from src.Session import Session

sessions: dict[int, Session] = {}


def get_or_create_session(session_id: int) -> Session:
    if session_id not in sessions:
        sessions[session_id] = Session(session_id)
    return sessions[session_id]


def close_session(session_id: int) -> None:
    if session_id in sessions:
        del sessions[session_id]
