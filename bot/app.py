import logging
import sys
from aiohttp import web
from aiohttp.web import Request, Response
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings
from botbuilder.schema import Activity
from config import Config
from h2o_bot import H2OBot

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

# ── Bot Framework adapter ────────────────────────────────────────────────────
SETTINGS = BotFrameworkAdapterSettings(
    app_id=Config.APP_ID,
    app_password=Config.APP_PASSWORD,
    channel_auth_tenant=Config.APP_TENANT_ID,
)
ADAPTER = BotFrameworkAdapter(SETTINGS)
BOT = H2OBot()


async def on_error(context, error: Exception):
    logger.exception("Unhandled error in bot turn")
    await context.send_activity("An unexpected error occurred. Please try again.")


ADAPTER.on_turn_error = on_error


# ── Routes ───────────────────────────────────────────────────────────────────
async def messages(req: Request) -> Response:
    if "application/json" not in req.headers.get("Content-Type", ""):
        return Response(status=415, text="Unsupported Media Type")

    body = await req.json()
    activity = Activity().deserialize(body)
    auth_header = req.headers.get("Authorization", "")

    await ADAPTER.process_activity(activity, auth_header, BOT.on_turn)
    return Response(status=200)


async def health(_req: Request) -> Response:
    return Response(text="OK")


# ── App setup ────────────────────────────────────────────────────────────────
app = web.Application()
app.router.add_get("/", health)
app.router.add_post("/api/messages", messages)

if __name__ == "__main__":
    logger.info("Starting bot on port %d", Config.PORT)
    web.run_app(app, host="0.0.0.0", port=Config.PORT)
