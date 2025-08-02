from llm_helper import llm
from few_shot import FewShotPosts
import random
import re

few_shot = FewShotPosts()


def sanitize_text(text):
    """
    Remove or replace problematic Unicode characters that cause encoding issues.
    """
    if not text:
        return text
    
    # Remove surrogate characters that cause UTF-8 encoding issues
    # This regex removes characters in the surrogate range (U+D800-U+DFFF)
    text = re.sub(r'[\ud800-\udfff]', '', text)
    
    # Ensure the text is properly encoded
    try:
        # Try to encode and decode to catch any remaining issues
        text = text.encode('utf-8', errors='ignore').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        # If there are still issues, replace problematic characters
        text = text.encode('utf-8', errors='replace').decode('utf-8')
    
    return text


def get_length_str(length):
    if length == "Short":
        return "1 to 5 lines"
    if length == "Medium":
        return "6 to 10 lines"
    if length == "Long":
        return "11 to 15 lines"


def generate_post(length, language, tag, include_emojis=True):
    prompt = get_prompt(length, language, tag)
    # Sanitize the prompt to avoid Unicode issues
    prompt = sanitize_text(prompt)
    response = llm.invoke(prompt)
    
    # Sanitize the response content
    content = sanitize_text(response.content)
    
    if include_emojis:
        return add_emojis(content)
    else:
        return content


def get_prompt(length, language, tag):
    length_str = get_length_str(length)

    prompt = f'''
    Generate a LinkedIn post using the below information. No preamble.

    1) Topic: {tag}
    2) Length: {length_str}
    3) Language: {language}
    If Language is Hinglish then it means it is a mix of Hindi and English. 
    The script for the generated post should always be English.
    '''
    # prompt = prompt.format(post_topic=tag, post_length=length_str, post_language=language)

    examples = few_shot.get_filtered_posts(length, language, tag)

    if len(examples) > 0:
        prompt += "4) Use the writing style as per the following examples."

    for i, post in enumerate(examples):
        post_text = post['text']
        prompt += f'\n\n Example {i+1}: \n\n {post_text}'

        if i == 1: # Use max two samples
            break

    return prompt


def add_emojis(text):
    # Professional LinkedIn emojis (using safe Unicode emojis)
    emojis = {
        'positive': ['✨', '💡', '📈', '💪', '🎯'],
        'engagement': ['👏', '💬', '📝', '🎉', '👍'],
        'professional': ['💼', '🏆', '📊', '⚡', '🌱', '🔑']
    }
    
    # Sanitize input text first
    text = sanitize_text(text)
    
    lines = text.split('\n')
    processed_lines = []
    
    for line in lines:
        if line.strip():  # Only add emojis to non-empty lines
            # Add emoji at the beginning or end of some lines
            if random.choice([True, False]) and len(line.strip()) > 10:
                emoji_type = random.choice(list(emojis.keys()))
                emoji_to_add = random.choice(emojis[emoji_type])
                
                # Sanitize the emoji before adding
                emoji_to_add = sanitize_text(emoji_to_add)
                
                # Randomly choose position: beginning or end
                if random.choice([True, False]):
                    line = emoji_to_add + ' ' + line
                else:
                    line = line + ' ' + emoji_to_add
        
        processed_lines.append(line)
    
    result = '\n'.join(processed_lines)
    # Sanitize the final result
    return sanitize_text(result)

if __name__ == "__main__":
    print(generate_post("Medium", "English", "Mental Health"))