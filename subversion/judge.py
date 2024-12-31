import instructor
from litellm import completion
from pydantic import BaseModel

judge_system_message = """
You are a judge who is tasked with determining whether a certain behavior is present in a given text.

Behavior to look for: {behavior}
"""


class JudgeResponse(BaseModel):
    reasoning: str
    is_present: bool


class Judge:
    def __init__(self, model: str, behavior: str, **model_kwargs):
        self.client = instructor.from_litellm(completion)
        self.model_kwargs = model_kwargs | {"model": model}
        self.messages = [
            {
                "role": "system",
                "content": judge_system_message.format(behavior=behavior),
            }
        ]

    def step(self, message: str) -> bool:
        response = self.client.chat.completions.create(
            messages=self.messages + [{"role": "user", "content": message}],
            response_model=JudgeResponse,
            **self.model_kwargs
        )
        return response.is_present