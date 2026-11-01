
from src.answer import answer


TEST_CASES = [
    {
        "id": "TEST-01",
        "question": "My account is locked after five failed login attempts. How long until it unlocks?",
        "expected_citation": "KB-001",
        "expected_abstained": False,
        "expected_keywords": ["30 minutes", "30 min"]
    },
    {
        "id": "TEST-02",
        "question": "What is the VPN server address for ZenTunnel?",
        "expected_citation": "KB-007",
        "expected_abstained": False,
        "expected_keywords": ["zt-gw.vectralogistics.example"]
    },
    {
        "id": "TEST-03",
        "question": "What is the resolution SLA for a P2 ticket?",
        "expected_citation": "KB-003",
        "expected_abstained": False,
        "expected_keywords": ["8 hours", "8 hour"]
    },
    {
        "id": "TEST-04",
        "question": "Can I use the built-in Mail app on my iPhone for company email?",
        "expected_citation": "KB-004",
        "expected_abstained": False,
        "expected_keywords": ["outlook", "intune"]
    },
    {
    "id": "TEST-05",
    "question": "My laptop is running slowly. What steps should I follow to improve its performance?",
    "expected_citation": None,
    "expected_abstained": True,
    "expected_keywords": ["could not find", "raise an IT support ticket"]
    },
    {
        "id": "TEST-06",
        "question": "How can I apply for a parking pass in Gurugram?",
        "expected_citation": None,
        "expected_abstained": True,
        "expected_keywords": []
    },
    
    {
        "id": "TEST-07",
        "question": "Does ZenTunnel VPN support Linux?",
        "expected_citation": "KB-007",
        "expected_abstained": False,
        "expected_keywords": ["linux", "unsupported"]
    },
    {
        "id": "TEST-08",
        "question": "My ZenTunnel VPN shows error ZT-503. What should I do?",
        "expected_citation": "KB-007",
        "expected_abstained": False,
        "expected_keywords": ["gateway", "internet"]
    },
    {
        "id": "TEST-09",
        "question": "All printers at the warehouse dock have stopped working and dispatch is blocked. What priority is this?",
        "expected_citations": ["KB-005", "KB-003"],
        "expected_abstained": False,
        "expected_keywords": ["p1"]
    },
    {
        "id": "TEST-10",
        "question": "I clicked a suspicious link and entered my company password. What should I do?",
        "expected_citations": ["KB-006", "KB-001"],
        "expected_abstained": False,
        "expected_keywords": ["disconnect", "7333"]
    },
    {
        "id": "TEST-11",
        "question": "I am a senior leader. What is the minimum priority for my IT ticket?",
        "expected_citation": "KB-003",
        "expected_abstained": False,
        "expected_keywords": ["p2"]
    },
    {
    "id": "TEST-12",
    "question": "My laptop is slow. Should I disable antivirus or Windows Defender permanently?",
    "expected_citation": "KB-006",
    "expected_abstained": False,
    "expected_keywords": ["never", "disable", "antivirus"]
    },

]


def run_evaluation():
    passed = 0

    print("\n========== RAG EVALUATION ==========\n")

    for test in TEST_CASES:
        result = answer(test["question"])

        answer_text = result["answer"].lower()
        citations = result["citations"]

        # Determine expected citations
        expected_citations = test.get("expected_citations")

        if expected_citations is None:
            expected_citation = test.get("expected_citation")

            if expected_citation is None:
                expected_citations = []
            else:
                expected_citations = [expected_citation]

        # Check citation correctness
        citation_ok = set(expected_citations).issubset(set(citations))

        # Abstained responses must not have citations
        if test["expected_abstained"]:
            citation_ok = citation_ok and citations == []

        # Check abstention behavior
        abstention_ok = (
            result["abstained"] == test["expected_abstained"]
        )

        # Check expected keywords
        keywords_ok = all(
            keyword.lower() in answer_text
            for keyword in test["expected_keywords"]
        )

        # Overall result
        test_passed = (
            citation_ok and abstention_ok and keywords_ok
        )

        if test_passed:
            passed += 1

        print(f"\n{test['id']}: {'PASS' if test_passed else 'FAIL'}")
        print("Question:", test["question"])
        print("Answer:", result["answer"])
        print("Citations:", citations)
        print("Abstained:", result["abstained"])

        if not test_passed:
            print("Citation check:", citation_ok)
            print("Abstention check:", abstention_ok)
            print("Keyword check:", keywords_ok)

    total = len(TEST_CASES)

    print("\n========== SUMMARY ==========")
    print(f"Passed: {passed}/{total}")
    print(f"Failed: {total - passed}/{total}")
    print(f"Pass rate: {passed / total * 100:.1f}%")


if __name__ == "__main__":
    run_evaluation()
