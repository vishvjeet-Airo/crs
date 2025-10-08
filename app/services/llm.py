from app.prompt_library import table_text_to_knowledge_base, table_text_to_single_paragraph
from app.services.excel_processor import excel_to_table_text
from app.services.excel_parser import identify_excel_structure
from app.services.get_rows import get_rows
from dotenv import load_dotenv
import os
from app.services.vector_db import process_story_to_qdrant
from app.services.langchain_bedrock import bedrock_client

load_dotenv()

def table_to_story(table_text: str) -> str:
    final_prompt = table_text_to_knowledge_base.format(table_text=table_text)

    system_message = "You are a helpful assistant that converts tabular Q&A data into narrative paragraphs."
    
    response = bedrock_client.invoke_with_tracing(
        prompt=final_prompt,
        system_message=system_message
    )
    
    # Get cost estimate
    cost_estimate = bedrock_client.get_cost_estimate(final_prompt, response)
    print(f"📊 Story generation cost: ${cost_estimate['total_cost_usd']:.6f}")
    print(f"   Tokens - Input: {cost_estimate['input_tokens']:.0f}, Output: {cost_estimate['output_tokens']:.0f}")

    return response


def batch_to_single_paragraph(batch_text: str) -> str:
    """
    Convert a batch of related Q&A rows into a single comprehensive paragraph.
    """
    final_prompt = table_text_to_single_paragraph.format(table_text=batch_text)

    system_message = "You are a helpful assistant that converts batch Q&A data into a single comprehensive paragraph."
    
    response = bedrock_client.invoke_with_tracing(
        prompt=final_prompt,
        system_message=system_message
    )
    
    # Get cost estimate
    cost_estimate = bedrock_client.get_cost_estimate(final_prompt, response)
    print(f"📊 Single paragraph generation cost: ${cost_estimate['total_cost_usd']:.6f}")
    print(f"   Tokens - Input: {cost_estimate['input_tokens']:.0f}, Output: {cost_estimate['output_tokens']:.0f}")

    return response


def process_excel_to_story(file_path: str, output_file: str = "story_output_complex_format1.txt"):
    # Extract structured text
    table_text = excel_to_table_text(file_path)

    # Convert to narrative paragraphs
    story = table_to_story(table_text)

    # Save to file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(story)

    print(f"✅ Processed story saved at {output_file}")
    return story


def process_excel_to_story_by_batches(file_path: str, output_file: str = "story_output_batched.txt"):
    """
    Process Excel file by first identifying batches, then converting each batch to a story paragraph.
    This approach creates better RAG chunks by grouping related questions together.
    """
    print(f"🚀 Starting batch-based story processing for: {file_path}")
    
    # Extract structured text
    table_text = excel_to_table_text(file_path)
    print("✅ Excel converted to table text")
    
    # Identify structure and batches
    structure = identify_excel_structure(table_text)
    print(f"✅ Structure identified with {len(structure['batches'])} batches")
    
    all_story_paragraphs = []
    total_cost = 0.0
    
    print(f"📊 Processing {len(structure['batches'])} batches...")
    
    for i, batch in enumerate(structure["batches"], 1):
        print(f"🔄 Processing batch {i}/{len(structure['batches'])} (rows: {batch['rows']})")
        
        # Get the rows for this batch
        batch_text = get_rows(table_text, batch["rows"])
        
        # Convert batch to single paragraph
        batch_story = batch_to_single_paragraph(batch_text)
        
        # Add batch identifier
        batch_story_with_header = f"=== BATCH {i} (Rows: {batch['rows']}) ===\n{batch_story}\n"
        all_story_paragraphs.append(batch_story_with_header)
        
        # Estimate cost for this batch
        cost_estimate = bedrock_client.get_cost_estimate("", batch_story)
        total_cost += cost_estimate['total_cost_usd']
        
        print(f"✅ Batch {i} processed")
    
    # Combine all paragraphs
    combined_story = "\n".join(all_story_paragraphs)
    
    # Save to file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(combined_story)
    
    print(f"\n📈 Batch Processing Summary:")
    print(f"   Total batches processed: {len(structure['batches'])}")
    print(f"   Total estimated cost: ${total_cost:.6f}")
    print(f"   Output saved to: {output_file}")
    
    return combined_story


if __name__ == "__main__":
    file_path = "complex_format.xlsx"
    
    # Use the new batch-based processing
    story = process_excel_to_story_by_batches(file_path)
    
    # Optionally save to Qdrant
    # process_story_to_qdrant(story)
    # print("✅ Processed story saved to Qdrant")
    
    print("✅ Batch-processed story saved")

