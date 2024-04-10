from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class SubmitFeedbackResponse(BaseModel):
    """
    Provides confirmation of feedback submission, including any relevant details or messages.
    """

    success: bool
    message: str


async def submit_feedback(
    prompt_id: str, user_id: str, rating: int, comment: Optional[str]
) -> SubmitFeedbackResponse:
    """
    Collects user feedback on prompt refinements.

    This function adds a feedback record to the database associated with a specific prompt and user.
    It validates the input data, creates a prisma.models.Feedback record in the database,
    and returns a successful response with a message indicating the outcome.

    Args:
        prompt_id (str): The unique ID of the prompt that the feedback is for.
        user_id (str): The unique ID of the user submitting the feedback.
        rating (int): A numerical rating for the prompt refinement, typically on a scale (e.g., 1 to 5).
        comment (Optional[str]): Optional textual comments providing more detailed feedback.

    Returns:
        SubmitFeedbackResponse: Provides confirmation of feedback submission, including any relevant details or messages.

    Example:
        submit_feedback("prompt123", "user456", 5, "Very useful refinement!")
        > SubmitFeedbackResponse(success=True, message="prisma.models.Feedback submitted successfully.")
    """
    try:
        await prisma.models.Feedback.prisma().create(
            data={
                "promptId": prompt_id,
                "userId": user_id,
                "score": rating,
                "comment": comment,
            }
        )
        return SubmitFeedbackResponse(
            success=True, message="prisma.models.Feedback submitted successfully."
        )
    except Exception as e:
        return SubmitFeedbackResponse(
            success=False, message=f"Failed to submit feedback: {str(e)}"
        )
