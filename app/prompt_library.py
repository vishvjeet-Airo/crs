
table_text_to_knowledge_base ="""
You are given content extracted from an Excel workbook that contains due-diligence
questions from clients and the responses provided by Compass Group.
The text is structured as rows with cell references, questions, and answers.

Your task:
- Rewrite this table into a knowledge-base style narrative, consisting of self-contained atomic paragraphs optimized for RAG retrieval.
- Each paragraph should group together related Q&A rows into a single coherent topic for optimal semantic search.
- Each paragraph must be substantial enough to act as a RAG chunk (at least 4–6 sentences) and contain
  sufficient context to answer questions independently.
- Rephrase questions and answers naturally into factual statements about Compass Group.
- Ensure that no factual information from any table is omitted. Every detail must be represented
  in one paragraph.
- Each output must cover **all rows from the table in one comprehensive narrative**. Do not split the table into multiple chunks under any circumstances.

CHUNKING STRATEGY:
- Group follow-up questions with their main questions into single paragraphs
- Consolidate entire tables into single comprehensive paragraph , dont break it 
- If a question has no follow-ups or related content, create a standalone paragraph
- Prioritize semantic coherence - questions that would be retrieved together should be in the same chunk
- Ensure each chunk contains enough context for independent understanding

CONTENT GUIDELINES:
- Do not include metadata such as row numbers, cell coordinates, or who completed the form.
- Do not list dropdown options unless they add meaning to the answer.
- Focus only on content that is useful for understanding Compass Group's security, compliance,
  and risk posture.
- Take care not to make up information that is not present.
- Do not consider the information that is provided only to identify who filled out the form.
- Always frame the output as factual knowledge about Compass Group, not as a conversation.
- Do not add summary or any other info which is not mentioned in the sheet.
- Make facts clear and well-explained without over-explanation.

Example transformation

Input (table extract):
Row 7
A7 = "If you have experienced any breaches or incidents in the last 5 years explain them in detail along with the remediation actions taken."
D7 = "No"
Row 9
A9 = "Are internal or external key audits done at least annually..."
D9 = "Yes"
Row 10
A10 = "Has your organization undergone a SOC 2 Type 2..."
D10 = "Yes"

Output (paragraph):
Compass Group has not experienced any breaches or incidents in the past five years.
The company conducts internal and external audits annually, covering areas such as access
management, system configuration, and penetration testing. In addition, Compass Group has
undergone a SOC 2 Type 2 audit, providing evidence of compliance with industry standards.

Now use this style to rewrite the following extracted table text:

{table_text}
"""

table_text_to_knowledge_base_v2 ="""
You are given content extracted from an Excel workbook that contains due-diligence
questions from clients and the responses provided by Compass Group.
The text is structured as rows with cell references, questions, and answers.

Your task:
- Rewrite this table into a knowledge-base style narrative, consisting of self-contained atomic paragraphs optimized for RAG retrieval.
- Each paragraph should group together related Q&A rows into a single coherent topic for optimal semantic search.
- Each paragraph must be substantial enough to act as a RAG chunk (at least 4–6 sentences) and contain
  sufficient context to answer questions independently.
- Rephrase questions and answers naturally into factual statements about Compass Group.
- Ensure that no factual information from the table is omitted. Every detail must be represented
  in at least one paragraph.

CHUNKING STRATEGY:
- Group follow-up questions with their main questions into single paragraphs
- Consolidate entire tables into single comprehensive paragraphs
- Merge related questions on the same topic (e.g., all security questions, all audit questions)
- If a question has no follow-ups or related content, create a standalone paragraph
- Prioritize semantic coherence - questions that would be retrieved together should be in the same chunk
- Ensure each chunk contains enough context for independent understanding

CONTENT GUIDELINES:
- Do not include metadata such as row numbers, cell coordinates, or who completed the form.
- Do not list dropdown options unless they add meaning to the answer.
- Focus only on content that is useful for understanding Compass Group's security, compliance,
  and risk posture.
- Take care not to make up information that is not present in the table.
- Do not consider the information that is provided only to identify who filled out the form.
- Always frame the output as factual knowledge about Compass Group, not as a conversation.
- Do not add summary or any other info which is not mentioned in the sheet.
- Make facts clear and well-explained without over-explanation.

Example transformation

Input (table extract):
Row 7
A7 = "If you have experienced any breaches or incidents in the last 5 years explain them in detail along with the remediation actions taken."
D7 = "No"
Row 9
A9 = "Are internal or external key audits done at least annually..."
D9 = "Yes"
Row 10
A10 = "Has your organization undergone a SOC 2 Type 2..."
D10 = "Yes"

Output (paragraph):
Compass Group has not experienced any breaches or incidents in the past five years.
The company conducts internal and external audits annually, covering areas such as access
management, system configuration, and penetration testing. In addition, Compass Group has
undergone a SOC 2 Type 2 audit, providing evidence of compliance with industry standards.

Now use this style to rewrite the following extracted table text:

{table_text}
"""

table_text_to_single_paragraph ="""
You are given content extracted from an Excel workbook that contains due-diligence
questions from clients and the responses provided by Compass Group.
The text is structured as rows with cell references, questions, and answers.

Your task:
- Convert this batch of related Q&A rows into a SINGLE, comprehensive paragraph optimized for RAG retrieval.
- The paragraph should be substantial enough to act as a RAG chunk (at least 4–6 sentences) and contain
  sufficient context to answer questions independently.
- Rephrase questions and answers naturally into factual statements about Compass Group.
- Ensure that no factual information from the batch is omitted.

SINGLE PARAGRAPH REQUIREMENTS:
- Create ONE cohesive paragraph that flows naturally
- Group all related information together in a logical sequence
- Use transitional phrases to connect different aspects of the topic
- Make it read like a comprehensive knowledge base entry
- Ensure the paragraph is self-contained and can stand alone

CONTENT GUIDELINES:
- Do not include metadata such as row numbers, cell coordinates, or who completed the form.
- Do not list dropdown options unless they add meaning to the answer.
- Focus only on content that is useful for understanding Compass Group's security, compliance,
  and risk posture.
- Take care not to make up information that is not present in the table.
- Do not consider the information that is provided only to identify who filled out the form.
- Always frame the output as factual knowledge about Compass Group, not as a conversation.
- Do not add summary or any other info which is not mentioned in the sheet.
- Make facts clear and well-explained without over-explanation.

Example transformation

Input (batch extract):
Row 7
A7 = "If you have experienced any breaches or incidents in the last 5 years explain them in detail along with the remediation actions taken."
D7 = "No"
Row 9
A9 = "Are internal or external key audits done at least annually..."
D9 = "Yes"
Row 10
A10 = "Has your organization undergone a SOC 2 Type 2..."
D10 = "Yes"

Output (single paragraph):
Compass Group has not experienced any breaches or incidents in the past five years, demonstrating a strong security track record. The company maintains robust audit practices by conducting both internal and external key audits annually, covering critical areas such as access management, system configuration, and penetration testing. In addition, Compass Group has successfully undergone a SOC 2 Type 2 audit, providing independent verification of their compliance with industry standards and controls.

Now use this style to rewrite the following batch text into a single paragraph:

{table_text}
"""