import os

def analyze_noun(word):
    """
    Analyzes a noun to find its root form and determine if it is singular or plural.
    """
    # Plural endings handled
    if word.endswith("es"):
        # Check for rule 1 (E insertion for words ending in s, z, x, ch, sh)
        if any(word[:-2].endswith(suffix) for suffix in ["s", "z", "x", "ch", "sh"]):
            root = word[:-2]
            return f"{word} = {root}+N+PL"
        # Handles cases like 'apples' which are not covered by the above rule
        elif word.endswith('s'):
             root = word[:-1]
             if root.isalpha() and len(root) > 0:
                return f"{word} = {root}+N+PL"
        return "Invalid Word"

    elif word.endswith("ies"):
        # Rule 2 (Y replacement)
        root = word[:-3] + "y"
        return f"{word} = {root}+N+PL"

    elif word.endswith("s"):
        # Rule 3 (S addition) - avoid false positives like "is" or single-letter words
        root = word[:-1]
        if root.isalpha() and len(root) > 1:
            return f"{word} = {root}+N+PL"
        # If removing 's' leaves a single letter, it's likely singular (e.g., 'as', 'is')
        # Or it's the word itself if it doesn't fit plural rules
        return f"{word} = {word}+N+SG"

    else:
        # Assumed to be a singular form if no other rule matches
        return f"{word} = {word}+N+SG"

# --- Main script execution ---

# Get the absolute path of the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define file paths relative to the script's directory
input_file_path = os.path.join(script_dir, "brown_nouns.txt")
output_file_path = os.path.join(script_dir, "fst_output.txt")

words_to_analyze = []

# Safely open and read the input file
try:
    with open(input_file_path, "r", encoding="utf-8") as f:
        # Read each line, strip whitespace, and ignore empty lines
        words_to_analyze = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    print(f"❌ ERROR: The input file was not found.")
    print(f"Please make sure 'brown_nouns.txt' is in the same folder as the script: {script_dir}")
    exit() # Exit the script if the file doesn't exist

# Analyze each word
results = [analyze_noun(word) for word in words_to_analyze]

# Save the results to the output file
try:
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(results))
    print(f"✅ FST processing complete! Output saved to {output_file_path}")
except IOError as e:
    print(f"❌ ERROR: Could not write to the output file. Reason: {e}")

