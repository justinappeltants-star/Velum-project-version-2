"""VELUM - relais WebSocket "zéro connaissance".
Le serveur ne voit QUE du texte chiffré (AES-256-GCM côté navigateur). Aucune clé,
aucun message en clair, aucune écriture disque. Tout vit en RAM et disparaît."""
import asyncio, json, re, time
from contextlib import asynccontextmanager
from pathlib import Path
from urllib.parse import urlparse

from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

TTLS = {900, 1800, 3600, 10800, 86400, 259200, 604800}  # 15m 30m 1h 3h 24h 72h 7j
IDLE_SECONDS = 300          # destruction après 5 min sans message (si option cochée)
MAX_ROOMS, MAX_USERS, MAX_MSG = 5000, 50, 16384
ID_RE = re.compile(r"^[0-9a-f]{64}$")
INDEX = (Path(__file__).parent / "index.html").read_text(encoding="utf-8")

rooms: dict = {}
create_log: dict = {}       # anti-abus, en RAM, purgé en continu


class Room:
    def __init__(self, ttl: int, idle: bool):
        self.expires = time.time() + ttl
        self.idle = idle
        self.last = time.time()
        self.socks: set = set()


async def send(ws, payload):
    try:
        await ws.send_text(json.dumps(payload))
    except Exception:
        pass


async def broadcast(room, payload):
    await asyncio.gather(*(send(w, payload) for w in list(room.socks)))


async def destroy(rid, reason):
    room = rooms.pop(rid, None)
    if not room:
        return
    for w in list(room.socks):
        await send(w, {"type": "destroyed", "reason": reason})
        try:
            await w.close(4000)
        except Exception:
            pass
    room.socks.clear()


async def reaper():
    while True:
        await asyncio.sleep(2)
        now = time.time()
        for rid, r in list(rooms.items()):
            if now >= r.expires:
                await destroy(rid, "expired")
            elif r.idle and now - r.last >= IDLE_SECONDS:
                await destroy(rid, "idle")
        for ip in list(create_log):
            create_log[ip] = [t for t in create_log[ip] if now - t < 60]
            if not create_log[ip]:
                del create_log[ip]


@asynccontextmanager
async def lifespan(_):
    task = asyncio.create_task(reaper())
    yield
    task.cancel()


app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None, openapi_url=None)


@app.middleware("http")
async def security_headers(request: Request, call_next):
    resp = await call_next(request)
    resp.headers.update({
        "Content-Security-Policy": "default-src 'none'; script-src 'self' 'unsafe-inline'; "
            "style-src 'unsafe-inline'; connect-src 'self' ws: wss:; base-uri 'none'; "
            "form-action 'none'; frame-ancestors 'none'",
        "Referrer-Policy": "no-referrer",
        "Cache-Control": "no-store",
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "Strict-Transport-Security": "max-age=63072000; includeSubDomains",
        "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
    })
    return resp


@app.get("/", response_class=HTMLResponse)
async def home():
    return INDEX


class NewRoom(BaseModel):
    id: str
    ttl: int
    idle: bool = False


@app.post("/api/rooms")
async def create_room(body: NewRoom, request: Request):
    ip = request.client.host if request.client else "?"
    log = create_log.setdefault(ip, [])
    if len(log) >= 10:
        raise HTTPException(429, "Trop de créations, réessayez dans une minute.")
    if not ID_RE.match(body.id) or body.ttl not in TTLS or body.id in rooms or len(rooms) >= MAX_ROOMS:
        raise HTTPException(400, "Requête invalide.")
    log.append(time.time())
    rooms[body.id] = Room(body.ttl, body.idle)
    return {"ok": True}


@app.websocket("/ws/{rid}")
async def ws_room(ws: WebSocket, rid: str):
    origin = ws.headers.get("origin")
    await ws.accept()
    if origin and urlparse(origin).netloc != ws.headers.get("host"):
        await ws.close(4403)
        return
    room = rooms.get(rid) if ID_RE.match(rid) else None
    if not room or len(room.socks) >= MAX_USERS:
        await send(ws, {"type": "destroyed", "reason": "unknown"})
        await ws.close(4404)
        return
    room.socks.add(ws)
    await send(ws, {"type": "info", "expires_in": int(room.expires - time.time()),
                    "idle": room.idle, "idle_in": IDLE_SECONDS})
    await broadcast(room, {"type": "count", "n": len(room.socks)})
    bucket: list = []
    try:
        while True:
            data = await ws.receive_text()
            now = time.time()
            bucket = [t for t in bucket if now - t < 10]
            if len(data) > MAX_MSG or len(bucket) >= 20:
                continue
            bucket.append(now)
            room.last = now
            await broadcast(room, {"type": "msg", "d": data})
    except WebSocketDisconnect:
        pass
    finally:
        room.socks.discard(ws)
        if rooms.get(rid) is room:
            await broadcast(room, {"type": "count", "n": len(room.socks)})
