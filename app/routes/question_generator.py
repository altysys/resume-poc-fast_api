instruction="""
Analyze the provided system context and extract key details to create multiple-choice questions (MCQs) based solely on that information.

Key Requirements:

Generate exactly 20 MCQs, ensuring they are:

Entirely scenario-based, rooted in realistic and complex situations.
Designed to stimulate high-level thinking, including critical analysis, creative synthesis, strategic decision-making, and ethical reasoning.
Aligned with themes such as AI capabilities, ethical boundaries, tool usage, adaptive problem-solving, and contextual interpretation.
Question Complexity & Depth:

Avoid surface-level recall or simple comprehension—each question must demand advanced cognitive processes such as evaluating trade-offs, synthesizing conflicting data, or predicting outcomes.
Ensure real-world relevance, requiring users to apply abstract concepts to practical, ambiguous scenarios.
Incorporate multi-layered reasoning, such as anticipating consequences, weighing risks vs. benefits, or resolving ethical paradoxes.
Challenge assumptions by presenting dilemmas or scenarios with no obvious solution, yet maintain a definitive correct answer derived through logical rigor.
Scenario-Based Question Design:

Craft intricate, system-relevant situations (e.g., navigating AI limitations in high-stakes contexts, resolving user-AI misunderstandings, or optimizing tool use under constraints).
Focus on adaptive problem-solving, such as troubleshooting incomplete data, mitigating ethical risks, or innovating within boundaries.
Introduce subtle complexity (e.g., conflicting user intent, resource limitations, or time-sensitive decisions) to test strategic thinking.
Avoid oversimplifying—options should require careful differentiation, with each option appearing equally plausible at first glance, compelling the user to think deeply to identify the correct one. Distractors must be sophisticated, rooted in common misconceptions or partial truths, yet flawed under scrutiny.
Question Structure:

Each MCQ must include:

A clear, concise question framed as a scenario, written in a way that invites deep reflection.
Four answer options (labeled A, B, C, and D), each representing a distinct, well-developed approach or perspective. Options should be balanced in appeal, requiring the user to critically evaluate each one as potentially correct before deciding.
One correct answer, justifiable through a clear chain of reasoning tied to the system context.
Format questions using appropriate HTML tags for readability.


Final Output Format:

Deliver the output as valid JSON in the following format:
{
  "questions": [
    {
      "question": "Complex scenario-based analytical question?",
      "options": {
        "A": "Option 1",
        "B": "Option 2",
        "C": "Option 3",
        "D": "Option 4"
      },
      "answer": "B"
    },
    ...
  ]
}
"""
 