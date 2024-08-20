from uuid import uuid4

from openai import OpenAI

from src.config import get_settings
from src.logger import logger
from src.text.prompts import SYSTEM_PROMPT

client = OpenAI(
    api_key=get_settings().openai_dev_service_account,
    project=get_settings().openai_project_id,
)


def generate_text_response(message: str, session_id: uuid4 = None) -> str:
    completion = client.chat.completions.create(
        model=get_settings().openai_model_name,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message},
        ],
    )
    # TODO: after each call, append role and to database
    # TODO: once initiated, use history in database
    # refer to the completion object for the role also
    logger.info(session_id)
    logger.info(completion.usage.total_tokens)
    logger.info(completion.choices[0].message.role)

    return completion.choices[0].message.content
