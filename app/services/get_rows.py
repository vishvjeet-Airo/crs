def parse_rowwise_text(rowwise_text: str):
    """
    Parse row-wise extracted text into a dictionary keyed by row number.
    Example:
    {
      1: ['A1 = "Filled by - kjsdb"'],
      2: ['A2 = "MOA Artificial Intelligence Questionnaire"', 'C2 = "Vendor\'s Response"'],
      ...
    }
    """
    rows = {}
    current_row = None
    
    for line in rowwise_text.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("Row "):
            # New row begins
            current_row = int(line.split()[1])
            rows[current_row] = []
        else:
            # Add cell content under current row
            if current_row is not None:
                rows[current_row].append(line)
    
    return rows


def get_rows(rowwise_text: str, row_numbers: list[int]) -> str:
    """
    Given rowwise_text and a list of row numbers,
    return the formatted string for those rows.
    """
    rows = parse_rowwise_text(rowwise_text)
    output_lines = []
    
    for num in row_numbers:
        if num in rows:
            output_lines.append(f"Row {num}")
            output_lines.extend(rows[num])
    
    return "\n".join(output_lines)


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
B5 = "If yes, please answer the following questions. If no, please proceed to question 2. "
Row 6
A6 = "1b"
B6 = "What are the intended use cases and target audience?"
Row 7
A7 = "1c"
B7 = "What are the expected inputs?"
"""

    print(get_rows(text, [6, 7]))
