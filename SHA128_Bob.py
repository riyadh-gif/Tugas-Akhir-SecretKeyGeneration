import hashlib
import time
import pandas as pd
from xlwt import Workbook

def sha128_hash(input_data: str) -> str:
    """
    Computes a 128-bit hash by truncating the SHA-256 hash.
    :param input_data: Data to hash (as string).
    :return: 128-bit (16-byte) hash as hexadecimal string.
    """
    sha256_hash = hashlib.sha256(input_data.encode('utf-8')).hexdigest()
    sha128_hash = sha256_hash[:32]  # Truncate to 128 bits (16 bytes)
    return sha128_hash


def process_data_for_hashing(data: pd.DataFrame):
    """
    Process data from DataFrame, hash it, and save the result in Excel.
    :param data: DataFrame containing data to hash.
    """
    hex1 = []
    start_time = time.time()

    # Iterate over each row in the DataFrame to apply hashing
    for _, row in data.iterrows():
        row_data = row.to_string(index=False)
        hash1 = sha128_hash(row_data)
        hex1.append(hash1)

    # Output the hash results
    print("Hasil hash Alice Kunci =")
    for idx, hash_val in enumerate(hex1):
        print(f"Index {idx + 1}: {hash_val}")
    
    # Saving the hash results to an Excel file using xlwt
    book = Workbook()
    sheet1 = book.add_sheet('sha128')

    sheet1.write(0, 0, 'Bob')  # Writing header
    for i, hash_val in enumerate(hex1, start=1):
        sheet1.write(i, 0, hash_val)

    # Save the Excel file
    book.save('SHA128BOB.xls')
    print(f"Excel file saved successfully! Time taken: {time.time() - start_time:.2f} seconds")


def main():
    # Sample data (replace with reading an actual Excel file)
    file_path = 'E:\\PENS\Semester 7\\Progress PA\\codingan\\Program\\Universal_Hash_Bob_doss2.xls'  # Replace with your file path
    
    # Read data from Excel
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"Error reading the file: {e}")
        return

    # Process and hash the data
    process_data_for_hashing(df)


if __name__ == "__main__":
    main()
