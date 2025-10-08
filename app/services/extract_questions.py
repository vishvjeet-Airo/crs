import re

def extract_questions(rowwise_text: str, question_col: str) -> list[str]:
    """
    Extract all questions from the given column in the rowwise extracted text.
    
    Args:
        rowwise_text (str): Extracted Excel content in row-wise format.
        question_col (str): Column letter where questions are stored (e.g., "B").
    
    Returns:
        list[str]: List of question texts.
    """
    questions = []
    col_pattern = re.compile(rf"^{question_col}\d+\s*=\s*\"(.*)\"$")
    
    for line in rowwise_text.strip().splitlines():
        match = col_pattern.match(line.strip())
        if match:
            questions.append(match.group(1))
    
    return questions


# Example usage
if __name__ == "__main__":
    text = """
Row 1
A1 = "Filled by - kjsdb"
Row 2
A2 = "MOA Artificial Intelligence Questionnaire"
C2 = "Vendor's Response"
Row 4
A4 = "1"
B4 = "Does the software/service we use as part of our contract with you currently use or make available to us Artificial Intelligence (“AI”) features, components, tools, or models (collectively “models”)?  Y/N"
Row 5
A5 = "1a"
B5 = "If yes, please answer the following questions. If no, please proceed to question 2."
Row 6
A6 = "1b"
B6 = "What are the intended use cases and target audience?"
Row 7
A7 = "1c"
B7 = "What are the expected inputs?"
"""
    
    qs = extract_questions(text, "B")
    print(qs)
