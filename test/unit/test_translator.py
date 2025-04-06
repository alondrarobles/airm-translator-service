from src.translator import translate_content


def test_chinese():
    is_english, translated_content = translate_content("这是一条中文消息")
    assert is_english == False
    assert "Chinese" in translated_content
    assert "message" in translated_content

def test_llm_normal_response():
    is_english, translated_content = translate_content("This is a normal English message")
    assert is_english == True
    assert translated_content == "This is a normal English message"

def test_llm_gibberish_response():
    is_english, translated_content = translate_content("shsohdohsohdohsodh")
    assert is_english == True
    assert translated_content == "shsohdohsohdohsodh"