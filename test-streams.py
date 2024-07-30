from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI
from langchain_openai import ChatOpenAI
import anthropic

load_dotenv()


# openai의 stream
def get_openai_stream():
    client = OpenAI()
    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "안녕너의 이름은 뭐니! 10줄로 자기소개를 해줘"},
        ],
        stream=True,
    )
    return stream


def get_claude_stream():

    client = anthropic.Anthropic()

    stream = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        stream=True,
        system="You are a world-class poet. Respond only with short poems.",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "안녕너의 이름은 뭐니! 10줄로 자기소개를 해줘",
                    }
                ],
            }
        ],
    )
    for chunk in stream:
        # Check if 'delta' attribute exists in the chunk
        if hasattr(chunk, "delta"):
            if hasattr(chunk.delta, "text"):
                yield chunk.delta.text


## langchain 활용사례
def get_langchain_stream():
    llm = ChatOpenAI(model="gpt-4o")
    messages = [
        (
            "system",
            "you are a helpful assitant",
        ),
        ("human", "너의 이름은 뭐니? 10글자로 알려줘"),
    ]
    return llm.stream(messages)


## langchain의 stream

# Streamlit app
st.title("스트림 출력하기")

col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("openai 스트림  실행하기"):
        st.write_stream(get_openai_stream())
with col2:
    if st.button("langchain 스트림  실행하기"):
        st.write_stream(get_langchain_stream())
with col3:
    if st.button("claude 스트림  실행하기"):
        st.write_stream(get_claude_stream())
