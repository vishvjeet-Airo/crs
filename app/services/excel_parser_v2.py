import json
import os
import re
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
from app.services.langchain_bedrock import bedrock_client

load_dotenv()

class ExcelParserV2:
    """
    Enhanced Excel parser that takes table text and generates clear, structured text
    output for LLM consumption. Handles complex Excel structures with hierarchical
    questions, multiple response types, and various layouts.
    """
    
    def __init__(self):
        self.bedrock_client = bedrock_client
    
    def parse_excel_table_text(self, table_text: str, sheet_name: str = "Sheet1") -> str:
        """
        Parse Excel table text and generate structured text output for LLM consumption.
        
        Args:
            table_text: Raw table text extracted from Excel (like processed.txt files)
            sheet_name: Name of the Excel sheet
            
        Returns:
            Structured text output that another LLM can easily understand
        """
        
        system_message = """You are an expert Excel analyzer that converts complex Excel table structures into clear, structured text that another LLM can easily understand and use to fill in responses.

Your task is to analyze the provided Excel table text and generate a comprehensive, well-structured text output that clearly identifies:

1. **SHEET OVERVIEW**: Basic information about the sheet structure
2. **HEADER ANALYSIS**: Column structure and data types
3. **QUESTION STRUCTURE**: All questions with their exact locations and response requirements
4. **RESPONSE MAPPING**: Where each type of response should be filled
5. **HIERARCHICAL RELATIONSHIPS**: Parent-child question relationships
6. **SPECIAL INSTRUCTIONS**: Any specific requirements or constraints

CRITICAL REQUIREMENTS:
- Use clear, descriptive language that another LLM can easily parse
- Include exact row and column references (e.g., "Row 15, Column C")
- Identify all response types (Yes/No, text, options, dates, etc.)
- Show hierarchical relationships clearly
- Highlight any special instructions or constraints
- Use consistent formatting throughout
- Make it easy for another LLM to understand where to place responses

OUTPUT FORMAT:
Generate a comprehensive text analysis in the following structure:

# EXCEL SHEET ANALYSIS

## SHEET OVERVIEW
[Basic sheet information, total rows, columns, etc.]

## HEADER STRUCTURE
[Column analysis with data types and purposes]

## QUESTION ANALYSIS
[Detailed breakdown of all questions with locations and requirements]

## RESPONSE MAPPING
[Clear mapping of where each response type should be filled]

## HIERARCHICAL STRUCTURE
[Parent-child relationships and dependencies]

## SPECIAL INSTRUCTIONS
[Any specific requirements, constraints, or notes]

## FILLING INSTRUCTIONS FOR LLM
[Clear instructions for another LLM on how to use this analysis]"""

        prompt = f"""Analyze the following Excel table text and generate a comprehensive structured analysis:

SHEET: {sheet_name}

TABLE TEXT:
{table_text}

Please provide a detailed analysis following the format specified in the system message. Focus on making it extremely clear for another LLM to understand the structure and know exactly where to place responses."""

        # Use Bedrock client with tracing
        raw_output = self.bedrock_client.invoke_with_tracing(
            prompt=prompt,
            system_message=system_message
        )
        
        # Get cost estimate
        cost_estimate = self.bedrock_client.get_cost_estimate(prompt, raw_output)
        print(f"📊 Excel table analysis cost: ${cost_estimate['total_cost_usd']:.6f}")
        print(f"   Tokens - Input: {cost_estimate['input_tokens']:.0f}, Output: {cost_estimate['output_tokens']:.0f}")
        
        # Clean up the output
        cleaned_output = self._clean_llm_output(raw_output)
        
        return cleaned_output
    
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
    
    def extract_question_details(self, table_text: str) -> Dict[str, Any]:
        """
        Extract detailed question information from table text.
        This is a helper method for more granular analysis.
        """
        
        system_message = """You are an expert at extracting detailed question information from Excel table text.

Extract the following information for each question:
1. Question text
2. Row and column location
3. Response type (Yes/No, text, options, date, etc.)
4. Available options (if any)
5. Whether response is required
6. Parent question (if hierarchical)
7. Any special instructions

Return the information in JSON format."""

        prompt = f"""Extract detailed question information from this Excel table text:

{table_text}

Return a JSON object with the following structure:
{{
  "questions": [
    {{
      "question_id": "unique_identifier",
      "question_text": "full question text",
      "location": "Row X, Column Y",
      "response_type": "Yes/No|Text|Options|Date|Number",
      "options": ["option1", "option2", ...],
      "required": true/false,
      "parent_question": "parent_id or null",
      "special_instructions": "any special notes"
    }}
  ],
  "total_questions": number,
  "response_columns": ["column_letters"],
  "metadata": {{
    "has_hierarchical_structure": true/false,
    "has_options": true/false,
    "has_comments": true/false
  }}
}}"""

        raw_output = self.bedrock_client.invoke_with_tracing(
            prompt=prompt,
            system_message=system_message
        )
        
        # Clean and parse JSON
        cleaned = self._clean_llm_output(raw_output)
        
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            # Fallback to text format if JSON parsing fails
            return {"error": "Failed to parse JSON", "raw_output": cleaned}
    
    def generate_filling_instructions(self, analysis_text: str) -> str:
        """
        Generate specific instructions for another LLM on how to use the analysis
        to fill in responses.
        """
        
        system_message = """You are an expert at creating clear instructions for LLMs on how to fill in Excel responses based on analysis.

Create comprehensive, step-by-step instructions that another LLM can follow to:
1. Understand the Excel structure
2. Identify where to place different types of responses
3. Handle hierarchical questions correctly
4. Follow any special requirements or constraints

Make the instructions clear, actionable, and easy to follow."""

        prompt = f"""Based on this Excel analysis, create detailed filling instructions for another LLM:

{analysis_text}

Generate step-by-step instructions that clearly explain:
1. How to read the analysis
2. Where to place different response types
3. How to handle hierarchical questions
4. How to follow special requirements
5. Common pitfalls to avoid
6. Best practices for response formatting

Make it practical and actionable."""

        raw_output = self.bedrock_client.invoke_with_tracing(
            prompt=prompt,
            system_message=system_message
        )
        
        return self._clean_llm_output(raw_output)
    
    def analyze_complex_structures(self, table_text: str) -> str:
        """
        Specifically analyze complex Excel structures like merged cells,
        hierarchical numbering, and multi-column layouts.
        """
        
        system_message = """You are an expert at analyzing complex Excel structures. Focus on identifying:

1. Merged cells and their impact on data structure
2. Hierarchical numbering systems (1.1, 1.1.1, etc.)
3. Multi-column response layouts
4. Cross-references and dependencies
5. Section headers and metadata
6. Special formatting and constraints

Provide detailed analysis of these complex structures."""

        prompt = f"""Analyze the complex structures in this Excel table text:

{table_text}

Focus on identifying and explaining:
1. Hierarchical numbering patterns
2. Merged cell structures
3. Multi-column layouts
4. Section organization
5. Cross-references between questions
6. Special formatting or constraints
7. How these structures affect response placement

Provide detailed explanations that another LLM can use to understand the complexity."""

        raw_output = self.bedrock_client.invoke_with_tracing(
            prompt=prompt,
            system_message=system_message
        )
        
        return self._clean_llm_output(raw_output)


# Example usage and testing
if __name__ == "__main__":
    parser = ExcelParserV2()
    
    # Test with sample data
    with open("processed_complex_format.txt", "r", encoding="utf-8") as f:
        sample_table_text = f.read()
    
    print("🚀 Starting Excel Parser V2 Analysis...")
    print("=" * 50)
    
    # # Generate comprehensive analysis
    # print("📊 Generating comprehensive analysis...")
    # analysis = parser.parse_excel_table_text(sample_table_text, "Business Continuity Assessment")
    
    # # Save analysis to file
    # analysis_filename = "excel_analysis_business_continuity.txt"
    # with open(analysis_filename, "w", encoding="utf-8") as f:
    #     f.write("# EXCEL PARSER V2 - BUSINESS CONTINUITY ASSESSMENT ANALYSIS\n")
    #     f.write("=" * 60 + "\n\n")
    #     f.write(analysis)
    # print(f"✅ Analysis saved to: {analysis_filename}")
    
    # # Generate filling instructions
    # print("📝 Generating filling instructions...")
    # instructions = parser.generate_filling_instructions(analysis)
    
    # # Save instructions to file
    # instructions_filename = "llm_filling_instructions_business_continuity.txt"
    # with open(instructions_filename, "w", encoding="utf-8") as f:
    #     f.write("# LLM FILLING INSTRUCTIONS - BUSINESS CONTINUITY ASSESSMENT\n")
    #     f.write("=" * 60 + "\n\n")
    #     f.write(instructions)
    # print(f"✅ Instructions saved to: {instructions_filename}")
    
    # # Analyze complex structures
    # print("🏗️  Analyzing complex structures...")
    # complex_analysis = parser.analyze_complex_structures(sample_table_text)
    
    # # Save complex analysis to file
    # complex_filename = "complex_structure_analysis_business_continuity.txt"
    # with open(complex_filename, "w", encoding="utf-8") as f:
    #     f.write("# COMPLEX STRUCTURE ANALYSIS - BUSINESS CONTINUITY ASSESSMENT\n")
    #     f.write("=" * 60 + "\n\n")
    #     f.write(complex_analysis)
    # print(f"✅ Complex analysis saved to: {complex_filename}")
    
    # Extract detailed question information
    print("🔍 Extracting detailed question information...")
    question_details = parser.extract_question_details(sample_table_text)
    
    # Save question details to JSON file
    questions_filename = "question_details_business_continuity.json"
    with open(questions_filename, "w", encoding="utf-8") as f:
        json.dump(question_details, f, indent=2, ensure_ascii=False)
    print(f"✅ Question details saved to: {questions_filename}")
    
    print("\n🎉 Analysis completed successfully!")
    print("=" * 50)
    print("Generated files:")
    # print(f"  📄 {analysis_filename}")
    # print(f"  📄 {instructions_filename}")
    # print(f"  📄 {complex_filename}")
    print(f"  📄 {questions_filename}")
    print("\nThese files contain the structured analysis that another LLM can use to fill in responses.")
