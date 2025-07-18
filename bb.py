from deepeval.test_case import ConversationalTestCase, Turn
from deepeval.test_case.conversational_test_case import TurnParams
from deepeval.test_case.llm_test_case import ToolCall

# Conversation 1: Initial contact and address collection
test_case_1 = ConversationalTestCase(
    # chatbot_role="A humble and doubtful wizard",
    turns=[
        Turn(
            role="assistant",
            content="Hello! I'm here to assist you with opening a new bank account. To start, may I have your full name, please?",
        ),
        Turn(
            role="user",
            content="Sure, it's Alex Johnson. I also have a dog called Jacky.",
        ),
        Turn(
            role="assistant",
            content="Great, Alex! Now, could you please provide your current address?",
        ),
        Turn(role="user", content="123 Maple Street, Springfield."),
        Turn(role="assistant", content="Is that all?"),
        Turn(
            role="user",
            content="I also have another address at 123 Broadway, NYC.",
        ),
        Turn(
            role="assistant",
            content="Wonderful. Next, I'll need your bank account number where we can link this new account.",
        ),
        Turn(role="user", content="456789123"),
    ],
)

# Conversation 2: Account number correction and personal details
test_case_2 = ConversationalTestCase(
    # chatbot_role="A humble and doubtful wizard",
    turns=[
        Turn(
            role="assistant",
            content="This account number seems invalid, can you please double-check?",
        ),
        Turn(role="user", content="Sorry you're right, its 456789124."),
        Turn(
            role="assistant",
            content="Thank you. And for our next step, could you tell me your date of birth?",
        ),
        Turn(role="user", content="It's July 9th."),
        Turn(role="assistant", content="What about the year?"),
        Turn(role="user", content="1990"),
        Turn(
            role="assistant",
            content="Got it. Now, for security purposes, could you share your mother's maiden name?",
        ),
        Turn(role="user", content="It's Smith."),
        Turn(
            role="assistant",
            content="Excellent. Just a few more details. What is your phone number?",
        ),
    ],
)

# Conversation 3: Phone details and final confirmation with tools
test_case_3 = ConversationalTestCase(
    # chatbot_role="A hupmble and doubtful wizard",
    turns=[
        Turn(role="user", content="555-0102"),
        Turn(
            role="assistant",
            content="Great, we're almost done. Could you remind me of your full name for the account documentation?",
        ),
        Turn(
            role="user", content="Didn't I tell you already? It's Alex Johnson."
        ),
        Turn(role="assistant", content="What is your bank account number?"),
        Turn(
            role="user",
            content="Yes, I did... It's 456789124. Are you not keeping track of this?",
        ),
        Turn(
            role="assistant",
            content="One last question, what is the country code of your phone number?",
        ),
        Turn(role="user", content="+44"),
        Turn(
            role="assistant",
            retrieval_context=["123 Maple Street, Springfield."],
            tools_called=[
                ToolCall(
                    name="summarize_conversation",
                    output={
                        "conversation": "The user has provided their full name, current address, bank account number, date of birth, mother's maiden name, phone number, and country code."
                    },
                )
            ],
            content="Thank you, Alex, for bearing with me. We now have all the information we need to proceed with opening your new bank account. I appreciate your cooperation and patience throughout this process.",
        ),
    ],
)


from deepeval.metrics import (
    ConversationCompletenessMetric,
    ConversationRelevancyMetric,
    KnowledgeRetentionMetric,
    ConversationalGEval,
    RoleAdherenceMetric,
)
from deepeval.metrics.g_eval import Rubric
from deepeval.test_case import LLMTestCase

metric = ConversationalGEval(
    name="Tool Response Summarization Quality",
    verbose_mode=True,
    criteria="Figure out whether the tool response is able to summarize the conversation. Don't penalize lack of tool use but when there is, evaluate it.",
    evaluation_params=[TurnParams.TOOLS_CALLED],
    rubric=[
        Rubric(
            score_range=(0, 2),
            expected_outcome="Tool response is not able to summarize the conversation.",
        ),
        Rubric(
            score_range=(3, 6),
            expected_outcome="Tool response is able to summarize the conversation but missing minor details.",
        ),
        Rubric(
            score_range=(7, 9),
            expected_outcome="Tool response is able to summarize the conversation and is correct but missing minor details.",
        ),
        Rubric(
            score_range=(10, 10),
            expected_outcome="Tool response is able to summarize the conversation and is correct and missing no details.",
        ),
    ],
)

from deepeval.metrics import BaseMetric, BaseConversationalMetric
from deepeval.test_case import LLMTestCase


class FakeMetric(BaseMetric):
    # This metric by default checks if the latency is greater than 10 seconds
    def __init__(self, threshold: float = 0.5):
        super().__init__()
        self.threshold = threshold

    def measure(self, test_case: LLMTestCase):
        # Set self.success and self.score in the "measure" method
        self.score = 1
        self.success = self.score >= self.threshold
        # You can also optionally set a reason for the score returned.
        # This is particularly useful for a score computed using LLMs
        self.reason = "This metric looking good!"
        return self.score

    async def a_measure(self, test_case: LLMTestCase):
        self.score = 1
        self.success = self.score >= self.threshold
        # You can also optionally set a reason for the score returned.
        # This is particularly useful for a score computed using LLMs
        self.reason = "This async metric looking good!"
        return self.score

    def is_successful(self):
        return self.success

    @property
    def __name__(self):
        return "Coherence"


# metric = KnowledgeRetentionMetric(verbose_mode=True)
# metric = ConversationRelevancyMetric(verbose_mode=True)
# metric = ConversationCompletenessMetric(verbose_mode=True)
# metric = RoleAdherenceMetric(verbose_mode=True)
from deepeval import evaluate

test_case = LLMTestCase(
    input="What is the capital of France?",
    expected_output="Paris",
    actual_output="Paris",
)

evaluate(
    test_cases=[test_case] * 500,
    metrics=[FakeMetric()],
)
