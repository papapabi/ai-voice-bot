import json
from uuid import uuid4

from openai import OpenAI

from src.config import get_settings
from src.db import PostgreSQLMessageHistory
from src.logger import logger
from src.rag.qdrant import search
from src.text.prompts import faq_prompt
from src.text.tools import openai_tools

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
            {"role": "system", "content": faq_prompt},
            {"role": "user", "content": message},
        ]
        history.add_message(role_name="system", message_content=faq_prompt)
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
            tools=openai_tools,
            tool_choice="auto",
        )

        tool_calls = completion.choices[0].message.tool_calls

        if tool_calls:
            if tool_calls[0].function.name == "search_vector_database":
                tool_query_string = json.loads(tool_calls[0].function.arguments)["q"]
                results = search(q=tool_query_string, limit=3)
                logger.info(f"Search result: {results}")
                logger.info(f"Matched question: {results[0].get('match')}")
                context = results[0].get("answer")

                # Append OpenAI ChatCompletionMessage(content=None, role='assistant', tool_calls=[ChatCompletionMessageToolCall(...)])
                # important line; without this, it won't work
                # This is done so another message with the role "tool" can be appended
                messages.append(completion.choices[0].message)
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_calls[0].id,
                        "name": tool_calls[0].function.name,
                        "content": context,
                    }
                )

                completion = client.chat.completions.create(
                    model=get_settings().openai_model_name,
                    messages=messages,
                )

        logger.info(completion.choices[0].message.content)
        ai_response = completion.choices[0].message.content
        history.add_message(role_name="assistant", message_content=ai_response)
        return ai_response
    except Exception as e:
        logger.error(f"OpenAI API request failed: {e}")
        return "An error occurred while processing your request."


def delete_history(session_id: uuid4) -> None:
    history = PostgreSQLMessageHistory(session_id=session_id)
    history.delete()
    return


if __name__ == "__main__":
    from src.text.prompts import faq_prompt
    from src.text.tools import openai_tools

    message = "Good morning! Just wanted to ask you, how can I pay for BillEase outstanding balance?"
    # message = "Tell me about the weather today?"
    logger.info(f"{message=}")

    client = OpenAI(
        api_key=get_settings().openai_dev_service_account,
        project=get_settings().openai_project_id,
    )

    messages = [
        {"role": "system", "content": faq_prompt},
        {"role": "user", "content": message},
    ]

    logger.info(f"Messages to send: {json.dumps(messages, indent=2)}")

    response = client.chat.completions.create(
        model=get_settings().openai_model_name,
        messages=messages,
        tools=openai_tools,
        tool_choice="auto",
    )

    tool_calls = response.choices[0].message.tool_calls
    if tool_calls:
        tool_call_id = tool_calls[0].id
        tool_function_name = tool_calls[0].function.name
        tool_query_string = json.loads(tool_calls[0].function.arguments)["q"]

        from src.rag.qdrant import search

        if tool_function_name == "search_vector_database":
            results = search(q=tool_query_string, limit=3)
            logger.info(f"Search results: {results}")
            logger.info(f"Matched question: {results[0].get('match')}")
            context = results[0].get("answer")

            logger.info(response.choices[0].message)
            # important line; without this, it won't work.
            messages.append(
                response.choices[0].message,
            )

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call_id,
                    "name": tool_function_name,
                    "content": context,
                }
            )

            logger.info(f"Messages to send: {messages}")

            model_response_with_function_call = client.chat.completions.create(
                model=get_settings().openai_model_name,
                messages=messages,
            )
            print(model_response_with_function_call.choices[0].message.content)
        else:
            print(f"Error: function {tool_function_name} does not exist")
    else:
        print(response.choices[0].message)
