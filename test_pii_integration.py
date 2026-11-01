
from unittest.mock import patch

from src.answer import answer


def test_pii_is_redacted_before_external_calls():

    question = (
        "Hi, my email is anand.sharma@company.com. "
        "My phone is +91 98765 43210 and employee ID "
        "is VX12345. My account is locked. How long "
        "until it unlocks?"
    )

    # Mock external API-related functions so no API calls
    # are made during this test.
    with patch(
        "src.answer.retrieve_documents"
    ) as mock_retrieve, patch(
        "src.answer.generate_answer"
    ) as mock_generate:

        mock_retrieve.return_value = [
            {
                "doc_id": "KB-001",
                "title": "Password reset",
                "score": 0.90,
                "text": "Accounts unlock after 30 minutes."
            }
        ]

        mock_generate.return_value = {
            "answer": "Your account unlocks after 30 minutes.",
            "citations": ["KB-001"],
            "abstained": False
        }

        answer(question)

        # Inspect what was actually passed to retrieval.
        retrieval_question = mock_retrieve.call_args[0][0]

        # Inspect what was actually passed to generation.
        generation_question = mock_generate.call_args[0][0]

        print("Retrieval received:", retrieval_question)
        print("Generation received:", generation_question)

        # Verify that sensitive information is absent.
        for sensitive_value in [
            "anand.sharma@company.com",
            "+91 98765 43210",
            "VX12345"
        ]:
            assert sensitive_value not in retrieval_question
            assert sensitive_value not in generation_question

        assert "[EMAIL_REDACTED]" in retrieval_question
        assert "[PHONE_REDACTED]" in retrieval_question
        assert "[EMPLOYEE_ID_REDACTED]" in retrieval_question

        assert retrieval_question == generation_question

        print("\nPASS: PII was masked before both external calls.")


if __name__ == "__main__":
    test_pii_is_redacted_before_external_calls()
