import json
from uuid import uuid4

from openai import OpenAI

from src.config import get_settings
from src.db import PostgreSQLMessageHistory
from src.logger import logger
from src.text.prompts import SYSTEM_PROMPT

client = OpenAI(
    api_key=get_settings().openai_dev_service_account,
    project=get_settings().openai_project_id,
)


def generate_text_response(message: str, session_id: uuid4) -> str:
    logger.info(f"{message=}")
    logger.info(f"{session_id=}")

    history = PostgreSQLMessageHistory(session_id=session_id)

    if not history.session_exists():
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message},
        ]
        history.add_message(role_name="system", message_content=SYSTEM_PROMPT)
        history.add_message(role_name="user", message_content=message)
    else:
        messages = history.get_n_messages(limit=10)
        messages = [msg.to_dict() for msg in messages]
        history.add_message(role_name="user", message_content=message)

    logger.info(f"Messages to send: {json.dumps(messages, indent=2)}")

    model_name = get_settings().openai_model_name
    logger.info(f"Using model: {model_name}")

    try:
        completion = client.chat.completions.create(
            model=model_name,
            messages=messages,
        )
        ai_response = completion.choices[0].message.content
        history.add_message(role_name="assistant", message_content=ai_response)
        return ai_response
    except Exception as e:
        logger.error(f"OpenAI API request failed: {e}")
        return "An error occurred while processing your request."


if __name__ == "__main__":
    # message = "Hello, who is this?"
    # print(f"{message=}")
    # logger.info(f"{message=}")
    # client = OpenAI(
    #     api_key=get_settings().openai_dev_service_account,
    #     project=get_settings().openai_project_id,
    # )

    # completion = client.chat.completions.create(
    #     model=get_settings().openai_model_name,
    #     messages=[
    #         {"role": "system", "content": SYSTEM_PROMPT},
    #         {"role": "user", "content": message},
    #     ],
    # )

    # ai_response = completion.choices[0].message.content
    # print(f"{ai_response=}")
    # logger.info(f"{ai_response=}")

    client = OpenAI(
        api_key=get_settings().openai_dev_service_account,
        project=get_settings().openai_project_id,
    )

    history = PostgreSQLMessageHistory("44d10f9f-b36e-458a-a3d2-58adbf054dce")
    logger.debug(f"{history.session_exists()=}")
    if history.session_exists():
        messages = history.get_n_messages(limit=10)
        messages = [msg.to_dict() for msg in messages]
        logger.debug(f"{messages=}")

    model_name = get_settings().openai_model_name
    logger.debug(f"{model_name=}")

    completion = client.chat.completions.create(
        model=model_name,
        messages=messages,
    )

    ai_response = completion.choices[0].message.content
    logger.debug(f"{ai_response=}")
