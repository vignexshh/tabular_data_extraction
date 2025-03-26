# legacy approach while taking distinct single folder input 
import os
import camelot
import sys
import re

def extract_tables_from_pdf(pdf_path):
    try:
        tables = camelot.read_pdf(pdf_path, pages='all', flavor='hybrid')
        if not tables:
            print(f"No tables found in the PDF: {pdf_path}")
            return None
        return tables
    except Exception as e:
        print(f"Error extracting tables from {pdf_path}: {e}")
        return None

def save_tables_as_txt(tables, output_path):
    total_tables = len(tables)
    with open(output_path, 'w', encoding='utf-8') as txt_file:
        for i, table in enumerate(tables):
            progress = (i + 1) / total_tables * 100
            print(f"Processing Table {i + 1}/{total_tables} ({progress:.2f}%)")
            for row in table.df.itertuples(index=False):
                line = ' + '.join(map(lambda cell: str(cell).replace('\n', ' '), row))
                txt_file.write(f"\n{line}")
            txt_file.write("\n")

def remove_non_numerical_chars_at_start(input_file_path, output_file_path):
    # This function removes non-numerical characters (including symbols) at the start of each line.
    with open(input_file_path, 'r', encoding='utf-8') as infile, open(output_file_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            # Use regex to find the first occurrence of a number and keep everything from there onward.
            match = re.search(r'\d', line)
            if match:
                # Find the index of the first number and slice the string from there.
                cleaned_line = line[match.start():]
                outfile.write(cleaned_line)
            else:
                # If no number is found, write an empty line or skip the line entirely.
                outfile.write("\n")  # You can choose to skip the line by not writing anything.

def remove_empty_lines(input_file_path, output_file_path):
    # This function removes all empty lines from the file.
    with open(input_file_path, 'r', encoding='utf-8') as infile, open(output_file_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            if line.strip():  # Only write non-empty lines
                outfile.write(line)

def process_directory(input_dir, extracted_text_dir, cleaned_data_dir):
    os.makedirs(extracted_text_dir, exist_ok=True)
    os.makedirs(cleaned_data_dir, exist_ok=True)
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(input_dir, filename)
            base_name = os.path.splitext(filename)[0]
            extracted_text_file = os.path.join(extracted_text_dir, f"[EXTRACTED]{base_name}.txt")
            print(f"Extracting tables from: {pdf_path}")
            tables = extract_tables_from_pdf(pdf_path)
            if tables:
                save_tables_as_txt(tables, extracted_text_file)
                print(f"Tables saved to: {extracted_text_file}")
                cleaned_text_file = os.path.join(cleaned_data_dir, f"[CLEANED]{base_name}.txt")
                print(f"Cleaning text file: {extracted_text_file}")
                remove_non_numerical_chars_at_start(extracted_text_file, cleaned_text_file)
                
                # Remove empty lines after cleaning
                final_cleaned_text_file = os.path.join(cleaned_data_dir, f"[FINAL_CLEANED]{base_name}.txt")
                remove_empty_lines(cleaned_text_file, final_cleaned_text_file)
                print(f"Final cleaned text saved to: {final_cleaned_text_file}")
            else:
                print(f"Skipping {pdf_path} due to no tables found or extraction error.")

def main():
    # Specify the input directory containing PDF files
    input_dir = 'PDFs'  # Replace with your actual path
    extracted_text_dir = 'extracted' # Replace with your actual path
    cleaned_data_dir = 'cleaned'  # Replace with your actual path
    
    # Process the directory
    process_directory(input_dir, extracted_text_dir, cleaned_data_dir)

if __name__ == '__main__':
    main()
