import camelot
import sys

def extract_tables_from_pdf(pdf_path):
    """
    Extracts tables from a PDF file using Camelot and saves them as a text file.

    Args:
        pdf_path (str): The file path of the PDF.

    Returns:
        tables (camelot.core.TableList): A list of tables extracted by Camelot.
    """
    tables = camelot.read_pdf(pdf_path, pages='all', flavor='lattice')

    if not tables:
        print("No tables found in the PDF.")
        sys.exit(1)
    
    return tables

def save_tables_as_txt(tables, output_path):
    """
    Saves the extracted tables to a text file, replacing vertical gridlines with ' + ' as a delimiter
    and removing newline characters nested within grid cells.

    Args:
        tables (camelot.core.TableList): A list of tables extracted by Camelot.
        output_path (str): The file path for the output text file.
    """
    total_tables = len(tables)
    with open(output_path, 'w', encoding='utf-8') as txt_file:
        for i, table in enumerate(tables):
            progress = (i + 1) / total_tables * 100
            print(f"Processing Table {i + 1}/{total_tables} ({progress:.2f}%)")
            for row in table.df.itertuples(index=False):
                # Remove nested newlines and join columns with ' + '
                line = ' + '.join(map(lambda cell: str(cell).replace('\n', ' '), row))
                txt_file.write(f"\n{line}")
            txt_file.write("\n")

def main():
    # Specify the path to your PDF file
    pdf_path = 'input'
    output_path = 'output'

    # Extract tables from the PDF
    tables = extract_tables_from_pdf(pdf_path)
    
    # Save the extracted tables as a text file
    save_tables_as_txt(tables, output_path)

    print(f"Tables have been saved to {output_path}")

# Execute the main function
if __name__ == '__main__':
    main()
