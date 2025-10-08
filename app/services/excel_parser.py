import json
import os
from dotenv import load_dotenv
import re
from app.services.langchain_bedrock import bedrock_client

load_dotenv()

def identify_excel_structure(extracted_rows: str):
    """
    Given a row-wise extracted excel sheet (text), use LLM to:
    - Identify header row
    - Identify question/answer/comment columns
    - Create batches of related questions
    Returns: dict with sheet structure info
    """

    system_message = """You are an expert at analyzing Excel sheet structures. Your task is to analyze the structure and return metadata that will allow filling answers in the same sheet.

Steps you must follow:
1. Detect the **row number of the header** (the row that defines columns such as Question, Answer, Comments, etc.).
2. Identify which **columns correspond to Question, Answer, and other fillable fields** (such as Comment, Remark, Notes).  
   - Use the exact Excel column letters (e.g., "B", "C", "D").
3. Determine from which **row the actual questions start**, ignoring metadata like instructions, titles, or submitter details.
4. Group the questions into **batches**.  
   - A batch must contain all related questions (e.g., main question and its follow-ups).  
   - Each batch should have sequential row numbers that can be answered together in a single RAG call.
5. Output the result **strictly in JSON only**, without explanations, code fences, or additional text.

Format:
{
  "sheet_name": "<sheet_name>",
  "header_row": <row number>,
  "columns": {"Question": "<col>", "Answer": "<col>", "Comment": "<col>"},
  "batches": [
    {"batch_id": 1, "rows": [..]},
    {"batch_id": 2, "rows": [..]}
  ]
}"""

    prompt = f"""Here is the extracted sheet:
{extracted_rows}"""

    # Use Bedrock client with tracing
    raw_output = bedrock_client.invoke_with_tracing(
        prompt=prompt,
        system_message=system_message
    )
    
    # Get cost estimate
    cost_estimate = bedrock_client.get_cost_estimate(prompt, raw_output)
    print(f"📊 Excel structure analysis cost: ${cost_estimate['total_cost_usd']:.6f}")
    print(f"   Tokens - Input: {cost_estimate['input_tokens']:.0f}, Output: {cost_estimate['output_tokens']:.0f}")
    
    cleaned = re.sub(r"^```[a-zA-Z]*\n?", "", raw_output.strip())
    cleaned = re.sub(r"\n?```$", "", cleaned).strip()
    reasoning = r'<reasoning>.*?</reasoning>'
    cleaned = re.sub(reasoning, '', cleaned, flags=re.DOTALL)

    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError:
        raise ValueError(f"Failed to parse JSON from LLM output:\n{raw_output}")

    return parsed


# Example usage
if __name__ == "__main__":
    # Simulated extracted rows (replace with your real extraction)

    with open("processed_complex_format.txt", "r", encoding="utf-8") as f:
        extracted_rows = f.read()

    structure = identify_excel_structure( extracted_rows)
    print(json.dumps(structure, indent=2))
