import streamlit as st
import time
import uuid
import json

from yt_rag.agent import get_answer


def print_log(message):
    print(message, flush=True)


def main():
    print_log("Starting the Course Assistant application")
    st.title("YT Assistant")

    # Session state initialization
    if "conversation_id" not in st.session_state:
        st.session_state.conversation_id = str(uuid.uuid4())
        print_log(
            f"New conversation started with ID: {st.session_state.conversation_id}"
        )

    # User input
    user_input = st.text_input("Enter your question:")

    if st.button("Ask"):
        print_log(f"User asked: '{user_input}'")
        with st.spinner("Processing..."):
            print_log(f"Getting answer from assistant")
            start_time = time.time()
            answer_data = get_answer(user_input)
            end_time = time.time()
            print_log(f"Answer received in {end_time - start_time:.2f} seconds")
            st.success("Completed!")
            st.write(json.dumps(answer_data, indent=2))


print_log("Streamlit app loop completed")


if __name__ == "__main__":
    print_log("YT Culinary Assistant application started")
    main()
