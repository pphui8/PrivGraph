import re

def clean_file(file_path):
    # Define a regular expression pattern for matching unwanted lines
    pattern = re.compile(r'^\d+$|^Q\d{6,9}$')

    # Open the file with UTF-8 encoding and read all lines
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Remove empty lines, duplicate lines, and lines matching the pattern
    unique_lines = list(dict.fromkeys(
        line for line in lines if line.strip() != "" and not pattern.match(line.strip())
    ))

    # Write the cleaned lines back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(unique_lines)

# Call the function with the path to your file
clean_file('yourfile.txt')