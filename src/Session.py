import asyncio

from fastapi import WebSocket


class Session:
    def __init__(self, session_id: int):
        self.session_id: int = session_id
        self.unity_ws: WebSocket | None = None
        self.web_client_ws: WebSocket | None = None

    async def connect_unity_client(self, websocket: WebSocket):
        print("Connecting unity client")
        self.unity_ws = websocket
        if self.both_clients_connected:
            await self.send_game_started()

    async def connect_web_client(self, websocket: WebSocket):
        print("Connecting web client")
        self.web_client_ws = websocket
        if self.both_clients_connected:
            await self.send_game_started()

    async def receive_unity(self, data: str):
        print(f"Received unity data {data}")
        await self.web_client_ws.send_text(f"Other: {data}")

    async def receive_web_client(self, data: str):
        print(f"Received web client {data}")
        await self.unity_ws.send_text(f"Other: {data}")

    @property
    def both_clients_connected(self) -> bool:
        return self.web_client_ws is not None and self.unity_ws is not None

    async def send_game_started(self):
        if self.both_clients_connected:
            await asyncio.gather(
                self.unity_ws.send_text("GameStart"),
                self.web_client_ws.send_text("GameStart"),
            )
