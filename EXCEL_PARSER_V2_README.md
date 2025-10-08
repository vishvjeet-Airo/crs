# Excel Parser V2 - Enhanced Excel Table Text Analyzer

## Overview

Excel Parser V2 is an advanced tool that takes Excel table text (like the processed files from your Excel extraction) and generates clear, structured text output that another LLM can easily understand and use to fill in responses. It handles complex Excel structures including hierarchical questions, multiple response types, merged cells, and various layouts.

## Key Features

### 🎯 **Clear Text Output for LLM Consumption**
- Generates paragraph-format text that another LLM can easily parse
- Includes precise row and column references (e.g., "Row 15, Column C")
- Identifies all response types (Yes/No, text, options, dates, etc.)
- Shows hierarchical relationships clearly

### 🏗️ **Complex Structure Handling**
- Hierarchical numbering systems (1.1, 1.1.1, etc.)
- Merged cells and multi-column layouts
- Section headers and metadata
- Cross-references and dependencies
- Special formatting and constraints

### 📊 **Comprehensive Analysis**
- Sheet overview and structure analysis
- Header structure and column mapping
- Detailed question analysis with locations
- Response mapping for different types
- Hierarchical structure identification
- Special instructions and constraints

## Usage

### Basic Usage

```python
from app.services.excel_parser_v2 import ExcelParserV2

# Initialize parser
parser = ExcelParserV2()

# Parse table text
analysis = parser.parse_excel_table_text(table_text, "Sheet Name")

# Generate filling instructions for another LLM
instructions = parser.generate_filling_instructions(analysis)
```

### Advanced Usage

```python
# Extract detailed question information
question_details = parser.extract_question_details(table_text)

# Analyze complex structures
complex_analysis = parser.analyze_complex_structures(table_text)
```

## Output Format

The parser generates structured text in the following format:

```
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
[Clear instructions for another LLM on how to use this analysis]
```

## Example Output

For a complex Excel sheet with hierarchical questions, the parser might generate:

```
# EXCEL SHEET ANALYSIS

## SHEET OVERVIEW
- Sheet Name: Business Continuity Assessment
- Total Rows: 157
- Total Columns: 5 (A-E)
- Structure: Hierarchical questionnaire with main questions and sub-questions

## HEADER STRUCTURE
- Column A: Question ID (hierarchical numbering like 3.1, 3.1.1)
- Column B: Question Text (detailed security questions)
- Column C: Vendor Response (Yes/No/NA/Partial options)
- Column D: Comments (text field for explanations)
- Column E: Additional Notes (optional field)

## QUESTION ANALYSIS

### Main Question 3.1 (Row 18, Column B)
- **Question**: "Is there an established incident management program that has been approved by management, communicated to appropriate constituents and an owner to maintain and review the program?"
- **Response Location**: Row 18, Column C
- **Response Type**: Yes/No with comment requirement
- **Options**: Yes, No, NA, Partial
- **Required**: Yes
- **Special Instructions**: If yes, attach Incident Mgmt/Crisis Mgmt Plan

### Sub-Question 3.2 (Row 19, Column B)
- **Question**: "Does the Incident Response Plan include guidance for recovery procedures?"
- **Response Location**: Row 19, Column C
- **Response Type**: Yes/No
- **Parent Question**: 3.1
- **Required**: Yes

## RESPONSE MAPPING
- **Yes/No Questions**: Place in Column C with exact row reference
- **Text Responses**: Use Column D for detailed explanations
- **Comments**: Required for No/NA/Partial responses in Column E
- **Attachments**: Reference in Column D when required

## HIERARCHICAL STRUCTURE
- Level 1: Main categories (3, 4, 5, etc.)
- Level 2: Sub-categories (3.1, 3.2, etc.)
- Level 3: Detailed questions (3.1.1, 3.1.2, etc.)
- Dependencies: Sub-questions depend on parent question responses

## SPECIAL INSTRUCTIONS
- All responses must be complete, timely, and accurate
- Non-applicable responses require thorough explanations
- Attachments must be provided when specified
- Comments required for No/NA/Partial responses

## FILLING INSTRUCTIONS FOR LLM
1. Read the question text carefully from Column B
2. Identify the response type and available options
3. Place the response in the correct column (C for main response, D for comments)
4. Follow hierarchical dependencies (sub-questions may depend on parent responses)
5. Include required comments for No/NA/Partial responses
6. Reference any required attachments in the comments field
```

## Methods

### `parse_excel_table_text(table_text, sheet_name)`
Main method that analyzes Excel table text and generates comprehensive structured output.

**Parameters:**
- `table_text`: Raw table text extracted from Excel
- `sheet_name`: Name of the Excel sheet

**Returns:** Structured text analysis

### `extract_question_details(table_text)`
Extracts detailed question information in JSON format.

**Returns:** Dictionary with questions, metadata, and structure information

### `generate_filling_instructions(analysis_text)`
Generates specific instructions for another LLM on how to use the analysis.

**Parameters:**
- `analysis_text`: Output from `parse_excel_table_text`

**Returns:** Step-by-step filling instructions

### `analyze_complex_structures(table_text)`
Analyzes complex Excel structures like merged cells and hierarchical layouts.

**Returns:** Detailed analysis of complex structures

## Testing

Run the test suite to see the parser in action:

```bash
python test_excel_parser_v2.py
```

Run the usage examples:

```bash
python example_usage_excel_parser_v2.py
```

## Integration

The parser integrates with your existing LangChain Bedrock setup and includes:
- Cost estimation and tracking
- Tracing for debugging
- Error handling and validation
- Clean output formatting

## Use Cases

1. **Risk Assessment Questionnaires**: Parse complex security questionnaires
2. **Compliance Forms**: Handle regulatory compliance forms with hierarchical structures
3. **Survey Processing**: Analyze survey data with multiple response types
4. **Data Migration**: Convert Excel structures to LLM-friendly formats
5. **Automated Form Filling**: Generate instructions for automated form completion

## Benefits

- **LLM-Friendly Output**: Clear, structured text that another LLM can easily understand
- **Complex Structure Support**: Handles the most complex Excel layouts
- **Precise Location Mapping**: Exact row and column references for accurate filling
- **Hierarchical Understanding**: Maintains parent-child relationships
- **Flexible Response Types**: Supports all common response formats
- **Comprehensive Analysis**: Provides complete understanding of Excel structure

This enhanced parser ensures that another LLM can easily understand where questions are located and where responses should be filled, even in the most complex Excel structures.
