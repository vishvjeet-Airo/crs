import json
import re
from typing import Dict, List, Any, Optional, Union
from dotenv import load_dotenv
from app.services.langchain_bedrock import bedrock_client

load_dotenv()


class ExcelParserV3:
    """
    Advanced Excel parser that analyzes table text and generates detailed response instructions
    for LLM-based question answering. Focuses on creating comprehensive instructions that specify
    exactly where and how responses should be filled at cell, row, column, and header levels.
    """
    
    def __init__(self):
        self.bedrock_client = bedrock_client
    
    def analyze_table_and_generate_instructions(self, table_text: str, sheet_name: str = "Sheet1") -> Dict[str, Any]:
        """
        Main method that analyzes table text and generates simple question-response instruction pairs.
        
        Args:
            table_text: Raw table text extracted from Excel
            sheet_name: Name of the Excel sheet
            
        Returns:
            Dictionary containing questions with their cell locations and detailed response instructions
        """
        
        system_message = """You are an expert Excel analyzer that extracts questions and creates detailed response instructions for LLM-based question answering.

Your task is to analyze the provided Excel table text and extract:
1. All questions with their exact cell locations (e.g., "D23", "B15")
2. Comprehensive response instructions for each question that include everything needed to answer it properly

For each question, provide:
- The exact cell reference where the answer should be filled
- The type of response needed (Yes/No, text, options, etc.)
- All available options if it's a choice question
- Any validation rules or constraints
- Format requirements
- Any special instructions

IMPORTANT: Return ONLY valid JSON. Do not include any text before or after the JSON. Start your response with { and end with }.

OUTPUT FORMAT:
{
  "questions": [
    {
      "question_text": "The actual question text",
      "cell_location": "D23",
      "response_instruction": "Detailed instruction explaining exactly how to answer this question, what format to use, what options are available, validation rules, etc. This should be comprehensive enough for another LLM to answer the question correctly."
    }
  ]
}

Make the response_instruction field very detailed and self-sufficient - it should contain everything another LLM needs to know to answer that specific question correctly."""

        prompt = f"""Analyze the following Excel table text and extract questions with their cell locations and response instructions:

SHEET: {sheet_name}

TABLE TEXT:
{table_text}

Extract all questions from this table and for each question:
1. Identify the exact cell location where the answer should be filled (e.g., "D23", "B15")
2. Create a comprehensive response instruction that includes:
   - What type of response is needed (Yes/No, text, choice, etc.)
   - All available options if it's a choice question
   - Format requirements (dates, numbers, text length, etc.)
   - Validation rules
   - Any special instructions or constraints
   - Cell ranges if it's a table question

Make each response_instruction detailed and self-sufficient so another LLM can answer the question correctly."""

        # Use Bedrock client with tracing
        raw_output = self.bedrock_client.invoke_with_tracing(
            prompt=prompt,
            system_message=system_message
        )
        
        # Get cost estimate
        cost_estimate = self.bedrock_client.get_cost_estimate(prompt, raw_output)
        print(f"📊 Excel V3 analysis cost: ${cost_estimate['total_cost_usd']:.6f}")
        print(f"   Tokens - Input: {cost_estimate['input_tokens']:.0f}, Output: {cost_estimate['output_tokens']:.0f}")
        
        # Clean and parse the output
        cleaned_output = self._clean_llm_output(raw_output)
        
        # Try to extract JSON from the cleaned output
        json_start = cleaned_output.find('{')
        if json_start != -1:
            json_text = cleaned_output[json_start:]
            # Remove any control characters that might cause JSON parsing issues
            json_text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', json_text)
            
            # Try to find the complete JSON object by counting braces
            brace_count = 0
            json_end = 0
            for i, char in enumerate(json_text):
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        json_end = i + 1
                        break
            
            if json_end > 0:
                json_text = json_text[:json_end]
            
            try:
                parsed_output = json.loads(json_text)
                return parsed_output
            except json.JSONDecodeError as e:
                print(f"❌ JSON parsing error: {e}")
                print(f"JSON text: {json_text[:500]}...")
                return {"error": "Failed to parse JSON", "raw_output": cleaned_output}
        else:
            print(f"❌ No JSON found in output")
            print(f"Raw output: {raw_output[:500]}...")
            return {"error": "No JSON found in output", "raw_output": cleaned_output}
    
    def create_simple_guide(self, analysis_result: Dict[str, Any]) -> str:
        """
        Create a simple guide showing questions with their cell locations and response instructions.
        
        Args:
            analysis_result: The analysis result from analyze_table_and_generate_instructions
            
        Returns:
            Simple guide as a string
        """
        
        guide = []
        guide.append("# EXCEL QUESTIONS AND RESPONSE INSTRUCTIONS")
        guide.append("=" * 60)
        guide.append("")
        
        # Check if we have an error and try to extract from raw output
        if "error" in analysis_result and "raw_output" in analysis_result:
            guide.append("## Note: JSON parsing failed, showing raw output")
            guide.append("")
            guide.append(analysis_result["raw_output"])
            return "\n".join(guide)
        
        questions = analysis_result.get("questions", [])
        if questions:
            for i, question in enumerate(questions, 1):
                question_text = question.get("question_text", "Unknown question")
                cell_location = question.get("cell_location", "Unknown")
                response_instruction = question.get("response_instruction", "No instructions provided")
                
                guide.append(f"## {i}. Question")
                guide.append(f"**Question:** {question_text}")
                guide.append(f"**Cell Location:** {cell_location}")
                guide.append("")
                guide.append("**Response Instruction:**")
                guide.append(response_instruction)
                guide.append("")
                guide.append("-" * 60)
                guide.append("")
        else:
            guide.append("No questions found in the analysis result.")
        
        return "\n".join(guide)
    
    def _clean_llm_output(self, raw_output: str) -> str:
        """Clean and format the LLM output."""
        # Remove code fences if present
        cleaned = re.sub(r"^```[a-zA-Z]*\n?", "", raw_output.strip())
        cleaned = re.sub(r"\n?```$", "", cleaned).strip()
        
        # Remove reasoning blocks if present
        reasoning_pattern = r'<reasoning>.*?</reasoning>'
        cleaned = re.sub(reasoning_pattern, '', cleaned, flags=re.DOTALL)
        
        # Clean up any extra whitespace
        cleaned = re.sub(r'\n\s*\n\s*\n', '\n\n', cleaned)
        
        return cleaned.strip()


# Example usage and testing
if __name__ == "__main__":
    parser = ExcelParserV3()
    
    # Test with sample data
    with open("processed_complex_format_empty.txt", "r", encoding="utf-8") as f:
        sample_table_text = f.read()
    
    print("🚀 Starting Excel Parser V3 Analysis...")
    print("=" * 50)
    
    # Generate simple analysis
    print("📊 Extracting questions and generating response instructions...")
    analysis_result = parser.analyze_table_and_generate_instructions(
        sample_table_text, 
        "Business Continuity Assessment"
    )
    
    # Save analysis result to JSON file
    analysis_filename = "excel_v3_questions.json"
    with open(analysis_filename, "w", encoding="utf-8") as f:
        json.dump(analysis_result, f, indent=2, ensure_ascii=False)
    print(f"✅ Questions and instructions saved to: {analysis_filename}")
    
    # Generate simple guide
    print("📝 Generating simple guide...")
    simple_guide = parser.create_simple_guide(analysis_result)
    
    # Save guide to file
    guide_filename = "excel_v3_questions_guide.txt"
    with open(guide_filename, "w", encoding="utf-8") as f:
        f.write(simple_guide)
    print(f"✅ Simple guide saved to: {guide_filename}")
    
    print("\n🎉 Excel Parser V3 analysis completed successfully!")
    print("=" * 50)
    print("Generated files:")
    print(f"  📄 {analysis_filename}")
    print(f"  📄 {guide_filename}")
    print("\nThese files contain questions with their cell locations and detailed response instructions.")
