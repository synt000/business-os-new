from pydantic import BaseModel


class FeedbackCreate(BaseModel):

    feedback_type: str

    subject: str

    message: str



class FeedbackResponse(BaseModel):

    status: str

    message: str
