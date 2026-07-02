from typing import List, Dict

from app.llm import llm
from app.prompts import (
    RECOMMENDATION_PROMPT,
    COMPARISON_PROMPT,
)


class ResponseGenerator:

    def generate_recommendation(
        self,
        context: Dict,
        assessments: List[Dict],
    ) -> str:
        """
        Generate explanation for recommended assessments.
        """

        if not assessments:
            return (
                "I couldn't find suitable SHL assessments "
                "based on the provided requirements."
            )

        docs = []

        for item in assessments:

            docs.append(
                f"""
Assessment Name: {item['name']}
Test Type: {item['test_type']}
Description: {item.get('description', '')}
"""
            )

        prompt = RECOMMENDATION_PROMPT.format(
            context=context,
            docs="\n".join(docs),
        )

        return llm.generate_reply(prompt)

    def generate_comparison(
        self,
        query: str,
        assessments: List[Dict],
    ) -> str:
        """
        Compare assessments using retrieved catalog entries only.
        """

        docs = []

        for item in assessments:

            docs.append(
                f"""
Assessment Name: {item['name']}
Test Type: {item['test_type']}
Description: {item.get('description', '')}
"""
            )

        prompt = COMPARISON_PROMPT.format(
            query=query,
            docs="\n".join(docs),
        )

        return llm.generate_reply(prompt)


generator = ResponseGenerator()