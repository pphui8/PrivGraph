# def replace_last_char_with_bracket_closure(txt_file):
#     # Open the file in read/write mode
#     with open(txt_file, 'rb+') as file:
#         file.seek(0, 2)  # Move the pointer to the end of the file
#         file_size = file.tell()  # Get the size of the file in bytes

#         # Ensure the file has at least 1 character to replace
#         if file_size >= 1:
#             # Move the pointer to the last character
#             file.seek(file_size - 1)
            
#             # Remove the last character and replace with '}]'
#             file.seek(file_size - 1)  # Move pointer to the last character to overwrite it
#             file.write(b'}]')  # Write '}]' at the end
            
#             # Truncate the file to ensure we only keep up to the point where we wrote '}]'
#             file.truncate(file_size + 1)  # File size grows by one due to the two characters replacing one
#         else:
#             print("The file is too small to remove the last character and add '}]'.")

# # # # Example usage
# txt_file_path = 'training_data.json'
# replace_last_char_with_bracket_closure(txt_file_path)


import ijson

def check_percentage_in_text(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        # Incrementally parse the JSON list
        parser = ijson.items(f, 'item')
        
        for record in parser:
            text = record.get('text', '')
            if '%' in text:
                print(f"Text contains '%': {text}")

# Call the function with your JSON file path
json_file_path = 'training_data.json'
check_percentage_in_text(json_file_path)