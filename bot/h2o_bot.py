import logging
from botbuilder.core import ActivityHandler, TurnContext, MessageFactory
from botbuilder.schema import ChannelAccount
from h2ogpte import H2OGPTE
from config import Config

logger = logging.getLogger(__name__)

# One h2oGPTe client shared across all conversations
_client = H2OGPTE(address=Config.H2OGPTE_URL, api_key=Config.H2OGPTE_API_KEY)

# Map Teams conversation_id -> h2oGPTe chat_session_id (keeps conversation history)
_sessions: dict[str, str] = {}


def _get_session(conversation_id: str) -> str:
    """Return an existing chat session for this conversation, or create one."""
    if conversation_id not in _sessions:
        _sessions[conversation_id] = _client.create_chat_session()
        logger.info("Created h2oGPTe session %s for conversation %s",
                    _sessions[conversation_id], conversation_id)
    return _sessions[conversation_id]


class H2OBot(ActivityHandler):

    async def on_message_activity(self, turn_context: TurnContext) -> None:
        user_text = (turn_context.activity.text or "").strip()
        if not user_text:
            return

        conversation_id = turn_context.activity.conversation.id

        try:
            session_id = _get_session(conversation_id)
            with _client.connect(session_id) as session:
                reply = session.query(user_text, timeout=120)
            answer = reply.content
        except Exception as exc:
            logger.exception("h2oGPTe query failed")
            answer = f"Sorry, I encountered an error: {exc}"

        await turn_context.send_activity(MessageFactory.text(answer))

    async def on_members_added_activity(
        self, members_added: list[ChannelAccount], turn_context: TurnContext
    ) -> None:
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    MessageFactory.text(
                        "Hi! I'm your H2O AI assistant. Ask me anything — "
                        "I'll use h2oGPTe to answer."
                    )
                )
