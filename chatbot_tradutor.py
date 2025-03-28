import streamlit as st
import openai

# Inicializa cliente OpenAI com a chave secreta
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Chatbot Tradutor", layout="centered")
st.title("Chatbot Tradutor")

# Inicializa estados
if "traduzido" not in st.session_state:
    st.session_state.traduzido = False
if "encerrar" not in st.session_state:
    st.session_state.encerrar = False
if "input" not in st.session_state:
    st.session_state.input = ""

# Interface encerrada
if st.session_state.encerrar:
    st.success("Sessão encerrada. Obrigado por usar o tradutor!")
    st.stop()

# Primeira tela: entrada de texto + botões
if not st.session_state.traduzido:
    st.write("""
    Cole um trecho do artigo científico em inglês e clique em **Traduzir**.  
    Quando quiser encerrar, clique em **Encerrar**.
    """)

    user_input = st.text_area("Texto em inglês:", key="input", height=150)

    col1, col2 = st.columns(2)
    with col1:
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
                st.session_state.translated_text = translated_text.strip()
                st.session_state.traduzido = True
                st.rerun()
            else:
                st.warning("Insira um trecho em inglês antes de clicar em Traduzir.")
    with col2:
        if st.button("Encerrar"):
            st.session_state.encerrar = True
            st.rerun()

# Tela de resultado da tradução
else:
    st.markdown("**Tradução:**")
    st.success(st.session_state.translated_text)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Traduzir novo texto"):
            st.session_state.traduzido = False
            st.session_state.input = ""
            st.rerun()
    with col2:
        if st.button("Encerrar"):
            st.session_state.encerrar = True
            st.rerun()
