import streamlit as st


from openai import OpenAI


def get_openai_stream():
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "자기소개를 10줄로 해줘"},
        ],
        stream=True,
    )

    for chunk in completion:
        if chunk.choices[0].delta.content:
            yield (chunk.choices[0].delta.content)


if st.button("stream 실행하기"):
    st.write_stream(get_openai_stream())
