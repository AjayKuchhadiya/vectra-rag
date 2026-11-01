
import re


# Email address pattern
EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)

# Employee ID pattern: VX followed by 5 digits
EMPLOYEE_ID_PATTERN = re.compile(
    r"\bVX\d{5}\b",
    re.IGNORECASE
)

# Phone number pattern: supports common international formats
PHONE_PATTERN = re.compile(
    r"(?<!\w)(?:\+\d{1,3}[\s.-]?)?"
    r"(?:\(?\d{2,5}\)?[\s.-]?)?"
    r"\d{3,5}[\s.-]?\d{3,5}(?!\w)"
)


def redact_pii(text):
    """
    Replace sensitive information with placeholders
    before sending text to external AI services.
    """

    text = EMAIL_PATTERN.sub("[EMAIL_REDACTED]", text)

    text = EMPLOYEE_ID_PATTERN.sub(
        "[EMPLOYEE_ID_REDACTED]", text
    )

    text = PHONE_PATTERN.sub("[PHONE_REDACTED]", text)

    return text


if __name__ == "__main__":

    sample = (
        "Hi, I am Anand Sharma. "
        "My email is anand.sharma@company.com "
        "and my phone number is +91 98765 43210. "
        "My employee ID is VX12345."
    )

    print("Original text:")
    print(sample)

    print("\nRedacted text:")
    print(redact_pii(sample))
