from fastapi import APIRouter, Depends, status

from src.auth.dependencies import check_api_key
from src.text.models import DeleteHistoryIn, GenerateTextIn, GenerateTextOut
from src.text.utils import delete_history, generate_text_response

router = APIRouter(
    prefix="/v1/text",
    tags=["text"],
    # dependencies=[Depends(check_api_key)],
)


@router.post(
    "/generate",
    summary="Generate a text response using gpt-4o-mini",
    response_model=GenerateTextOut,
    status_code=status.HTTP_201_CREATED,
)
def generate_response(*, request: GenerateTextIn):
    """
    Generate a response using gpt-4o-mini with the provided data:

    - **message** - The current message to generate a response to.
    """
    ai_message = generate_text_response(
        session_id=request.session_id,
        message=request.message,
    )
    return {"message": ai_message, "session_id": request.session_id}
