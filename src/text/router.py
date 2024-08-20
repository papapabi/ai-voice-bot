from fastapi import APIRouter, Depends

from src.auth.dependencies import check_api_key
from src.text.models import GenerateTextIn, GenerateTextOut
from src.text.utils import generate_text_response

router = APIRouter(
    prefix="/v1/text",
    tags=["text"],
    # dependencies=[Depends(check_api_key)],
)


@router.post(
    "/generate",
    summary="Generate a text response using gpt-4o-mini",
    response_model=GenerateTextOut,
)
def generate_response(*, request: GenerateTextIn):
    """
    Generate a response using gpt-4o-mini with the provided data:

    - **message** - The current message to generate a response to.
    """
    ai_message = generate_text_response(
        message=request.message,
    )
    return {"message": ai_message, "session_id": request.session_id}
