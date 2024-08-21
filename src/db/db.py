import psycopg
from psycopg.rows import class_row

from src.config import get_database_settings
from src.db.queries import *
from src.db.schemas import Message
from src.logger import logger
from src.text.prompts import SYSTEM_PROMPT

settings = get_database_settings()

CONNECTION_STRING = f"host={settings.postgres_host} user={settings.postgres_user} password={settings.postgres_password} port={settings.postgres_port} dbname={settings.postgres_dbname}"


class PostgreSQLMessageHistory:
    """DB abstraction for handling message history"""

    def __init__(self, session_id: str, connection_string: str = CONNECTION_STRING):
        self.session_id = session_id
        self.connection_string = connection_string

    def session_exists(self) -> bool:
        with psycopg.connect(conninfo=self.connection_string) as conn:
            with conn.cursor() as cur:
                cur.execute(CHECK_SESSION_EXISTS, (self.session_id,))
                return cur.fetchone() is not None

    def get_all_messages(self) -> list[Message]:
        with psycopg.connect(conninfo=self.connection_string) as conn:
            with conn.cursor(row_factory=class_row(Message)) as cur:
                messages = cur.execute(
                    GET_ALL_MESSAGES_BY_SESSION_ID, (self.session_id,)
                ).fetchall()
        return messages

    def get_n_messages(self, limit: int = 10):
        with psycopg.connect(conninfo=self.connection_string) as conn:
            with conn.cursor(row_factory=class_row(Message)) as cur:
                messages = cur.execute(
                    GET_N_MOST_RECENT_MESSAGES_BY_SESSION_ID, (self.session_id, limit)
                ).fetchall()
        # reverse messages to get them in chronological order
        # this is needed for OpenAI to properly understand context
        return messages[::-1]

    def add_message(self, role_name: str, message_content: str):
        with psycopg.connect(conninfo=self.connection_string) as conn:
            with conn.cursor() as cur:
                # Step 1: Retrieve the role_id from the msg_roles table
                cur.execute(GET_ROLE_ID, (role_name,))
                role = cur.fetchone()
                if not role:
                    raise ValueError(f"Role '{role_name}' not found")
                role_id = role[0]

                # Step 2: Retrieve the sess_id from the sess table using the session_id
                cur.execute(GET_SESS_ID, (self.session_id,))
                session = cur.fetchone()
                if not session:
                    cur.execute(INSERT_SESS, (self.session_id,))
                    session = cur.fetchone()
                sess_id = session[0]

                # Step 3: Insert the message into the msg table
                cur.execute(INSERT_MSG, (message_content, role_id))
                message = cur.fetchone()
                message_id = message[0]

                # Step 4: Link the message to the session in the sess_msg_link table
                cur.execute(INSERT_SESS_MSG_LINK, (sess_id, message_id))


if __name__ == "__main__":
    history = PostgreSQLMessageHistory("44d10f9f-b36e-458a-a3d2-58adbf054dce")
    logger.debug(history.session_exists())
    history.add_message(role_name="system", message_content=SYSTEM_PROMPT)
    history.add_message(
        role_name="user",
        message_content="hello i'd like to inquire regarding your services",
    )
    messages = history.get_all_messages()
    logger.debug(f"Message models: {messages}")
    logger.debug(f"to_dict(): {[msg.to_dict() for msg in messages]}")

    messages = history.get_n_messages(10)
    logger.debug(f"Message models: {messages}")
    logger.debug(f"to_dict(): {[msg.to_dict() for msg in messages]}")
