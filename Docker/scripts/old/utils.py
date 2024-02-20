from typing import List, Optional

def normalize_string(input_str: str, chars_to_normalize: List[str], normalizer: Optional[str] = '_') -> str:
    """
    Normalizes the input string by replacing specified characters with a normalizer.

    Args:
    - input_str (str): The string to normalize.
    - chars_to_normalize (List[str]): A list of characters in the string to be replaced.
    - normalizer (str): The character to replace the specified characters with. Defaults to '_'.

    Returns:
    - str: The normalized string.
    """
    for char in chars_to_normalize:
        input_str = input_str.replace(char, normalizer)
    return input_str

## Example usage
#input_str = 'cortex:m7-cortex.m4'
#chars_to_normalize = [':', '-', '.']
#normalizer = '_'
#normalized_str = normalize_string(input_str, chars_to_normalize, normalizer)
#print(f"Original: {input_str}\nNormalized: {normalized_str}")
