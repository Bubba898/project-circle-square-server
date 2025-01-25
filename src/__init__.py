from src.Session import Session

import globals

def get_or_create_session(session_id: int) -> Session:
    if session_id not in globals.sessions:
        globals.sessions[session_id] = Session(session_id)
    return globals.sessions[session_id]


def close_session(session_id: int) -> None:
    if session_id in globals.sessions:
        del globals.sessions[session_id]


def reset_sessions() -> None:
    globals.sessions = {}
