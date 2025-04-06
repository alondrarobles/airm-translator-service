import openai
import os

client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def get_translation(post: str) -> str:
    context = ("You are a helpful assistant that translates any non-English text into English."
                "If you cannot translated the text, return the word 'NONE'."
                "Else, respond with only the English translation."
          )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": context
            },
            {
                "role": "user",
                "content": f"Translate the following post to English:\n\n{post}"
            }
        ]
    )

    return response.choices[0].message.content.strip()

def get_language(post: str) -> str:
    context = (
        "You are an assistant that accurately identifies the language of a given text. "
        "If you can't get the language of it, return the word 'NONE'."
        "Else, if the text is in English, and it's a dialect (like AAVE, British English, or Indian English), "
        "respond with 'English'. Only return the name of the language."
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": f"What language is this post written in?\n\n{post}"}
        ]
    )

    return response.choices[0].message.content.strip()

def translate_content(content: str) -> tuple[bool, str]:
    # Use try/except block for error handling
    try:
        language = get_language(content)
        if not isinstance(language, str):
            raise ValueError("Expected a string from get_language")
        if language.strip().lower() == "none":
            raise ValueError("Language detection error")

        if language.strip().lower() == "english":
            result = (True, content)
        else:
            translation = get_translation(content)
            # print("Translation result:", translation)
            if translation.strip().lower() == "none":
                raise ValueError("Translation error")
            if not isinstance(translation, str):
                raise ValueError("Expected a string from get_translation")
            # if get_language(translation).strip().lower() != "english":
            #     raise ValueError("Non English text")
            result = (False, translation)

    except Exception as e:
        # Log the error, uncomment for debugging
        print(f"Error processing post: '{content}'. Error: {e}")
        # Fallback: assume the post is English and return the original post.
        result = (True, content)

    # Final format check
    if not (isinstance(result, tuple) and len(result) == 2 and isinstance(result[0], bool) and isinstance(result[1], str)):
        result = (True, content)
    return result

translate_content("这是一条中文消息")