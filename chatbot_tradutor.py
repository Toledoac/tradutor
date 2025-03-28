import streamlit as st
import openai

client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Chatbot Tradutor", layout="centered")
st.title("Chatbot Tradutor Literal")

# Inicializa estados
if "traduzido" not in st.session_state:
    st.session_state.traduzido = False
if "encerrar" not in st.session_state:
    st.session_state.encerrar = False
if "input" not in st.session_state:
    st.session_state.input = ""

# Mensagem inicial
if not st.session_state.traduzido and not st.session_state.encerrar:
    st.write("""
    Cole um trecho do artigo científico em inglês para traduzir.  
    Quando quiser encerrar, clique em **Encerrar** após a tradução.
    """)

    user_input = st.text_area("Texto em inglês:", key="input", height=150)

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
            st.session_state.traduzido = True
            st.session_state.translated_text = translated_text.strip()
        else:
            st.warning("Insira um trecho em inglês antes de clicar em traduzir.")

# Exibe a tradução e os botões de decisão
elif st.session_state.traduzido and not st.session_state.encerrar:
    st.markdown("**Tradução:**")
    st.success(st.session_state.translated_text)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Traduzir novo texto"):
            st.session_state.traduzido = False
            st.session_state.input = ""
    with col2:
        if st.button("Encerrar"):
            st.session_state.encerrar = True

# Exibe mensagem final
elif st.session_state.encerrar:
    st.success("Sessão encerrada. Obrigado por usar o tradutor!")
