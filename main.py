from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

from src import get_or_create_session, Session

app = FastAPI()


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <label>Session ID: <input type="text" id="session_id" autocomplete="off" value="foo"/></label>
            <label>Client Type (unity_ws | web_client_ws): <input type="text" id="client_type" autocomplete="off" value="unity_ws"/></label>
            <button onclick="connect(event)">Connect</button>
            <hr>
            <label>Message: <input type="text" id="messageText" autocomplete="off"/></label>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
        var ws = null;
            function connect(event) {
                var session_id = document.getElementById("session_id")
                var client_type = document.getElementById("client_type")
                ws = new WebSocket("ws://localhost:8000/" + client_type.value + "/" + session_id.value);
                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages')
                    var message = document.createElement('li')
                    var content = document.createTextNode(event.data)
                    message.appendChild(content)
                    messages.appendChild(message)
                };
                event.preventDefault()
            }
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/unity_ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: int):
    print("!!!")
    await websocket.accept()
    session: Session = get_or_create_session(session_id)
    await session.connect_unity_client(websocket)
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"You: {data}")
        await session.receive_unity(data)

@app.websocket("/web_client_ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: int):
    await websocket.accept()
    session: Session = get_or_create_session(session_id)
    await session.connect_web_client(websocket)
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"You: {data}")
        await session.receive_web_client(data)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
