from enum import Enum

from pydantic import UUID4, BaseModel


class MessageRole(str, Enum):
    system = "system"
    user = "user"
    assistant = "assistant"


class Message(BaseModel):
    role: MessageRole
    content: str

    def to_dict(self):
        return {
            "role": self.role.value,
            "content": self.content,
        }


if __name__ == "__main__":
    message = Message(content="hello", role="user")
    message2 = Message(content="hello", role="user")
    print(dict(message))
    print(message.model_dump_json())
    print([message for message in [message, message2]])
    print([msg.to_dict() for msg in [message, message2]])
