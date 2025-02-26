# This code automatically flavours extraction type based on first 1 to 2 pages, so uniform consistency is required for it decide (stream / lattice / hybrid)
import os
import camelot
import re

def detect_table_type(pdf_path):
   
    try:
        
        lattice_tables = camelot.read_pdf(pdf_path, pages='1,2', flavor='lattice')
        stream_tables = camelot.read_pdf(pdf_path, pages='1,2', flavor='stream')

      
        lattice_count = len(lattice_tables)
        stream_count = len(stream_tables)

       
        if lattice_count > stream_count:
            return 'lattice'
        elif stream_count > lattice_count:
            return 'stream'
        else:
            
            return 'lattice' if lattice_count > 0 else None
    except Exception as e:
        print(f"Error detecting table type in {pdf_path}: {e}")
        return None


def extract_tables_from_pdf(pdf_path, table_type):
    
    try:
        tables = camelot.read_pdf(pdf_path, pages='all', flavor=table_type)
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
              
                line = ' + '.join(map(lambda cell: str(cell).replace('\n', ' ').strip(), row))
                txt_file.write(f"{line}\n")
            txt_file.write("\n")  


def remove_non_numerical_chars_at_start(input_file_path, output_file_path):
    
    with open(input_file_path, 'r', encoding='utf-8') as infile, open(output_file_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            match = re.search(r'\d', line)
            if match:
                cleaned_line = line[match.start():]
                outfile.write(cleaned_line)
            else:
                outfile.write("\n")


def remove_empty_lines(input_file_path, output_file_path):
     
    with open(input_file_path, 'r', encoding='utf-8') as infile, open(output_file_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            if line.strip():
                outfile.write(line)


def process_directory(input_dir, output_base_dir):
    
    extracted_text_dir = os.path.join(output_base_dir, 'extracted')
    cleaned_data_dir = os.path.join(output_base_dir, 'cleaned')
    os.makedirs(extracted_text_dir, exist_ok=True)
    os.makedirs(cleaned_data_dir, exist_ok=True)

    for root, _, files in os.walk(input_dir):
        for filename in files:
            if filename.lower().endswith('.pdf'):
                pdf_path = os.path.join(root, filename)
                relative_path = os.path.relpath(root, input_dir)
                extracted_subdir = os.path.join(extracted_text_dir, relative_path)
                cleaned_subdir = os.path.join(cleaned_data_dir, relative_path)

                os.makedirs(extracted_subdir, exist_ok=True)
                os.makedirs(cleaned_subdir, exist_ok=True)

                base_name = os.path.splitext(filename)[0]
                extracted_text_file = os.path.join(extracted_subdir, f"[EXTRACTED]{base_name}.txt")

                print(f"Processing PDF: {pdf_path}")
                table_type = detect_table_type(pdf_path)

                if table_type:
                    print(f"Detected table type: {table_type}")
                    tables = extract_tables_from_pdf(pdf_path, table_type)
                    if tables:
                        save_tables_as_txt(tables, extracted_text_file)
                        print(f"Tables saved to: {extracted_text_file}")

                        cleaned_text_file = os.path.join(cleaned_subdir, f"[CLEANED]{base_name}.txt")
                        print(f"Cleaning text file: {extracted_text_file}")
                        remove_non_numerical_chars_at_start(extracted_text_file, cleaned_text_file)

                        final_cleaned_text_file = os.path.join(cleaned_subdir, f"[FINAL_CLEANED]{base_name}.txt")
                        remove_empty_lines(cleaned_text_file, final_cleaned_text_file)
                        print(f"Final cleaned text saved to: {final_cleaned_text_file}")
                    else:
                        print(f"No tables found in {pdf_path}. Skipping.")
                else:
                    print(f"Could not detect table type in {pdf_path}. Skipping.")


def main():
   
    input_dir = 'main directory input path'  # use [ r'] to specify abosolute paths 
    output_base_dir = os.path.dirname(input_dir)   

  
    process_directory(input_dir, output_base_dir)


if __name__ == '__main__':
    main()
