# Function to replace even occurrences of a word with one string and odd occurrences with another
def replace_even_odd_occurrences(text, word, even_replace, odd_replace):
    words = text.split()
    count = 0
    for i in range(len(words)):
        if words[i] == word:
            count += 1
            if count % 2 == 0:
                words[i] = even_replace
            else:
                words[i] = odd_replace
    return ' '.join(words)

# Read the content of file_to_read.txt
with open('file_to_read.txt', 'r') as file:
    content = file.read()

# Count the total occurrences of the word "terrible"
total_terrible_occurrences = content.count('terrible')

# Replace even occurrences with "pathetic" and odd occurrences with "marvellous"
modified_content = replace_even_odd_occurrences(content, 'terrible', 'pathetic', 'marvellous')

# Write the modified text to result.txt
with open('result.txt', 'w') as result_file:
    result_file.write(modified_content)

# Display the total times "terrible" appears
print(f'Total occurrences of "terrible": {total_terrible_occurrences}')

print("File 'result.txt' has been created with the modified text.")