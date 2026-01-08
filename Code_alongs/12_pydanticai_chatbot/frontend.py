import streamlit as st
from chat import JokeBot

# session_state använd hela tiden för att sidan ska "komma ihåg" historiken och inte tömma messageslsitan vid varje input

def init_session_states():
    # initisera historik
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "bot" not in st.session_state:
        st.session_state.bot = JokeBot()


def display_chat_messages():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def handle_user_input():
    # := tar värdet användaren skrivit och sparar det i prompt direkt
    if prompt := st.chat_input("Talk to the JokeBot"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        bot_response = st.session_state.bot.chat(prompt).get("bot")

        response = f"Ro Båt: {bot_response}"

        with st.chat_message(name ="user"):
            st.markdown(prompt)
        with st.chat_message(name = "ai"):
            st.markdown(response)

        st.session_state.messages.append({"role": "agent", "content": response})


def layout():
    st.markdown("# Chat with Ro Båt")
    st.write(
        "RO BÅT is a funny robot that can help you out with programming tasks. However he doesn't directly answer your question, usually he asks another question back."
    )

    display_chat_messages()
    handle_user_input()


if __name__ == "__main__":
    init_session_states()
    layout()