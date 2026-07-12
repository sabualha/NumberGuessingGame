import random
import streamlit as st

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@700&display=swap');

    [data-testid="stMarkdownContainer"] h1 {
        font-family: 'Baloo 2', cursive !important;
        text-align: center;
        font-size: 60px !important;
    }

    div[data-testid="stTextInput"] input {
        border-radius: 12px;
        border: 2px solid #d63384;
        padding: 10px 14px;
        font-size: 18px;
        text-align: center;
        background-color: white;
        color: #d63384;
    }

    div[data-testid="stTextInput"] input:focus {
        border-color: #ff69b4;
        box-shadow: 0 0 8px rgba(255, 105, 180, 0.5);
        outline: none;
    }
    </style>
""", unsafe_allow_html=True)

lowest_num = 1
highest_num = 100

if "answer" not in st.session_state:
    st.session_state.answer = random.randint(lowest_num, highest_num)
if "guesses" not in st.session_state:
    st.session_state.guesses = 0
if "hints_used" not in st.session_state:
    st.session_state.hints_used = 0
if "history" not in st.session_state:
    st.session_state.history = []
if "player_name" not in st.session_state:
    st.session_state.player_name = ""

st.title("Number Guessing Game! 🎯🎯🎯")

if not st.session_state.player_name:
    name_input = st.text_input("What's your name?")
    if st.button("Start Game"):
        if name_input:
            st.session_state.player_name = name_input
            st.rerun()
else:
    st.write(f"Hi {st.session_state.player_name}! 👋")

    st.markdown(
        f"<p style='text-align: center; font-size: 24px;'>Select a number between {lowest_num} and {highest_num}.</p>",
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            "<p style='text-align: center; font-size: 18px;'>Enter your guess:</p>",
            unsafe_allow_html=True
        )
        guess = st.text_input("Enter your guess:", label_visibility="collapsed")
        submitted = st.button("Submit Guess", use_container_width=True)
        hint_clicked = st.button("💡 Get a Hint", use_container_width=True)

    if submitted:
        if guess.isdigit():
            guess = int(guess)
            st.session_state.guesses += 1
            st.session_state.history.append(guess)

            if guess < lowest_num or guess > highest_num:
                st.write(f"Please enter a number between {lowest_num} and {highest_num}.")
            elif guess < st.session_state.answer:
                st.error("🥶 Too low! Try again.")
            elif guess > st.session_state.answer:
                st.error("🔥 Too high! Try again.")
            else:
                st.success(f"🎉 Correct! The answer was {st.session_state.answer}. You guessed it in {st.session_state.guesses} guesses!")
                st.balloons()
        else:
            st.write("Please enter a valid number.")

    if hint_clicked:
        st.session_state.hints_used += 1
        answer = st.session_state.answer

        if st.session_state.hints_used == 1:
            st.info(f"💡 Hint: the number is {'even' if answer % 2 == 0 else 'odd'}.")
        elif st.session_state.hints_used == 2:
            tens = (answer // 10) * 10
            st.info(f"💡 Hint: it's between {tens} and {tens + 10}.")
        elif st.session_state.hints_used == 3:
            st.info(f"💡 Hint: the sum of its digits is {sum(int(d) for d in str(answer))}.")
        else:
            st.info("🕵️ No more hints — you're on your own now!")

    if st.session_state.history:
        st.write("**Your guesses so far:**")
        history_display = []
        for g in st.session_state.history:
            if g == st.session_state.answer:
                history_display.append(f"{g} ✅")
            else:
                history_display.append(str(g))
        st.write(" → ".join(history_display))