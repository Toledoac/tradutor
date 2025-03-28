import streamlit as st
import openai

client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Chatbot Tradutor", layout="centered")
st.title("Chatbot Tradutor")

# Inicializa variáveis de sessão
if "encerrar" not in st.session_state:
    st.session_state.encerrar = False
if "historico" not in st.session_state:
    st.session_state.historico = []

st.write("""
Cole um trecho do artigo científico em inglês e clique em Traduzir.
Quando quiser encerrar, **escreva 'Fim' e clique em Traduzir**.
""")

# Verifica se o usuário decidiu encerrar
if st.session_state.encerrar:
    st.success("Sessão encerrada. Obrigado por usar o tradutor!")
    if st.session_state.historico:
        st.subheader("📜 Histórico de traduções:")
        for idx, item in enumerate(st.session_state.historico, 1):
            st.markdown(f"**{idx}. Texto original:** {item['original']}")
            st.markdown(f"**   Tradução:** {item['traducao']}")
    st.stop()

# Caixa de entrada
user_input = st.text_area("Texto em inglês:", key="input", height=150)

if st.button("Traduzir"):
    if user_input.strip().lower() in ["fim", "fim."]:
        st.session_state.encerrar = True
        st.experimental_rerun()

    elif user_input.strip() != "":
        prompt = f"Traduza literalmente, sem interpretar ou reescrever: {user_input}"

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        translated_text = response.choices[0].message.content

        # Adiciona ao histórico
        st.session_state.historico.append({
            "original": user_input.strip(),
            "traducao": translated_text.strip()
        })

        st.markdown("**Tradução:**")
        st.success(translated_text)

        # Limpa o campo de entrada
        st.experimental_rerun()
    else:
        st.warning("Insira um trecho em inglês antes de clicar em traduzir.")

# Mostra histórico (em tempo real, mesmo antes do fim)
if st.session_state.historico:
    st.subheader("📜 Histórico de traduções:")
    for idx, item in enumerate(st.session_state.historico, 1):
        st.markdown(f"**{idx}. Texto original:** {item['original']}")
        st.markdown(f"**   Tradução:** {item['traducao']}")
