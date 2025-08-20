import os

def analyze_noun(word):
    """
    Analyzes a noun to find its root form and determine if it is singular or plural.
    """
    
    if word.endswith("es"):
       
        if any(word[:-2].endswith(suffix) for suffix in ["s", "z", "x", "ch", "sh"]):
            root = word[:-2]
            return f"{word} = {root}+N+PL"
        
        elif word.endswith('s'):
             root = word[:-1]
             if root.isalpha() and len(root) > 0:
                return f"{word} = {root}+N+PL"
        return "Invalid Word"

    elif word.endswith("ies"):
        
        root = word[:-3] + "y"
        return f"{word} = {root}+N+PL"

    elif word.endswith("s"):
       
        root = word[:-1]
        if root.isalpha() and len(root) > 1:
            return f"{word} = {root}+N+PL"
       
        return f"{word} = {word}+N+SG"

    else:
        
        return f"{word} = {word}+N+SG"


script_dir = os.path.dirname(os.path.abspath(__file__))

input_file_path = os.path.join(script_dir, "brown_nouns.txt")
output_file_path = os.path.join(script_dir, "fst_output.txt")

words_to_analyze = []

try:
    with open(input_file_path, "r", encoding="utf-8") as f:
        
        words_to_analyze = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    print(f"❌ ERROR: The input file was not found.")
    print(f"Please make sure 'brown_nouns.txt' is in the same folder as the script: {script_dir}")
    exit() 


results = [analyze_noun(word) for word in words_to_analyze]

try:
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(results))
    print(f"✅ FST processing complete! Output saved to {output_file_path}")
except IOError as e:
    print(f"❌ ERROR: Could not write to the output file. Reason: {e}")

