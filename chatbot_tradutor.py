import streamlit as st
import openai

# Use o segredo se estiver no Streamlit Cloud
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Chatbot Tradutor", layout="centered")
st.title("Chatbot Tradutor Literal")

st.write("Cole um trecho do artigo científico em inglês e receba a tradução literal.")

user_input = st.text_area("Texto em inglês:", height=150)

if st.button("Traduzir"):
    if user_input.strip() != "":
        prompt = f"Traduza literalmente, sem interpretar ou reescrever: {user_input}"

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        translated_text = response.choices[0].message.content
        st.markdown("**Tradução:**")
        st.success(translated_text)
    else:
        st.warning("Insira um trecho em inglês antes de clicar em traduzir.")
