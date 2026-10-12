from __future__ import annotations

import csv
import random
import re
from pathlib import Path

import streamlit as st


DATA_PATH = Path(__file__).with_name("sentences.csv")
ANSWER_PATH = Path(__file__).with_name("answer_key.csv")


def load_sentences() -> list[str]:
    with DATA_PATH.open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        if not reader.fieldnames or "한글 예문" not in reader.fieldnames:
            raise ValueError("sentences.csv에 '한글 예문' 열이 없습니다.")
        values = [row["한글 예문"].strip() for row in reader if row.get("한글 예문", "").strip()]

    unique: list[str] = []
    seen: set[str] = set()
    for sentence in values:
        key = re.sub(r"\W+", "", sentence, flags=re.UNICODE)
        if key and key not in seen:
            seen.add(key)
            unique.append(sentence)
    return unique


def load_answer_key() -> dict[str, str]:
    if not ANSWER_PATH.exists():
        return {}
    with ANSWER_PATH.open("r", encoding="utf-8-sig", newline="") as csv_file:
        return {
            row["한글 예문"].strip(): row["영어 정답"].strip()
            for row in csv.DictReader(csv_file)
            if row.get("한글 예문", "").strip() and row.get("영어 정답", "").strip()
        }


def normalize_answer(answer: str) -> str:
    answer = answer.lower().replace("’", "'")
    return re.sub(r"[^a-z0-9]", "", answer)


def start_round() -> None:
    sentences = load_sentences()
    random.SystemRandom().shuffle(sentences)
    st.session_state.deck = sentences
    st.session_state.index = 0
    st.session_state.answers = []
    st.session_state.feedback = None


st.set_page_config(page_title="Level 2 영어 문장 연습", page_icon="✍️", layout="centered")

st.markdown(
    """
    <style>
      .stApp { background: #f7f8fc; }
      .block-container { max-width: 760px; padding-top: 3.2rem; }
      .eyebrow { color: #6558c8; font-size: .82rem; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; }
      .prompt-card { background: white; border: 1px solid #e8e9f2; border-radius: 22px; padding: 2rem 2.2rem; margin: 1.4rem 0 1.2rem; box-shadow: 0 12px 36px #24284d0b; }
      .prompt-card p { color: #24243a; font-size: 1.8rem; line-height: 1.65; font-weight: 650; margin: 0; }
      div.stButton > button, div.stFormSubmitButton > button { border-radius: 12px; min-height: 3rem; font-weight: 700; }
      @media (max-width: 640px) { .block-container { padding: 1.5rem 1rem; } .prompt-card { padding: 1.4rem; } .prompt-card p { font-size: 1.4rem; } }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Level 2 영어 문장 연습")
st.caption("한글 문장을 보고 영어로 써 보세요. 한 바퀴 동안 같은 문장은 다시 나오지 않습니다.")

if "deck" not in st.session_state:
    try:
        start_round()
    except (OSError, ValueError) as error:
        st.error(f"문장 파일을 읽지 못했습니다: {error}")
        st.stop()

deck: list[str] = st.session_state.deck
index: int = st.session_state.index
answers: list[dict[str, str]] = st.session_state.answers
answer_key = load_answer_key()

if index >= len(deck):
    st.success(f"한 바퀴 완료! {len(deck)}개 문장을 모두 연습했습니다.")
    st.markdown("### 이번 라운드 입력 기록")
    for number, item in enumerate(answers, 1):
        with st.container(border=True):
            st.caption(f"{number} / {len(answers)}")
            st.markdown(f"**한글**　{item['prompt']}")
            st.markdown(f"**내 답**　{item['answer']}")
            if item.get("result"):
                st.markdown(f"**결과**　{item['result']}")
                if item.get("correct_answer"):
                    st.markdown(f"**정답**　{item['correct_answer']}")
    if st.button("새 순서로 다시 시작", type="primary", use_container_width=True):
        start_round()
        st.rerun()
    st.stop()

st.progress(index / len(deck), text=f"{index + 1} / {len(deck)}")
st.markdown('<div class="eyebrow">영어로 번역해 보세요</div>', unsafe_allow_html=True)
st.markdown(f'<div class="prompt-card"><p>{deck[index]}</p></div>', unsafe_allow_html=True)
prompt = deck[index]
feedback = st.session_state.feedback
if feedback and feedback["prompt"] == prompt:
    if feedback["result"] == "correct":
        st.success("정답!")
    elif feedback["result"] == "incorrect":
        st.error("오답입니다.")
        st.markdown(f"**정답:** {feedback['correct_answer']}")
    else:
        st.info("이 문장은 답지에서 확인되지 않아 자동 채점하지 않았습니다.")

    with st.form(f"next_form_{index}"):
        st.text_input(
            "다음 문장으로",
            placeholder="Enter를 눌러 다음 문장으로 이동하세요.",
            label_visibility="collapsed",
            key=f"advance_input_{index}",
        )
        next_clicked = st.form_submit_button("다음 문장 →", type="primary", use_container_width=True)
    if next_clicked:
        item = {"prompt": prompt, "answer": feedback["answer"]}
        if feedback.get("result") in {"correct", "incorrect"}:
            item["result"] = "정답" if feedback["result"] == "correct" else "오답"
            item["correct_answer"] = feedback.get("correct_answer", "")
        answers.append(item)
        st.session_state.answers = answers
        st.session_state.index = index + 1
        st.session_state.feedback = None
        st.rerun()

else:
    st.caption("영어 답을 입력하고 Enter 또는 버튼을 누르세요. 답지에 있는 문장은 즉시 채점합니다.")
    with st.form(f"answer_form_{index}"):
        st.text_input(
            "영어 답",
            placeholder="Type your English translation…",
            label_visibility="collapsed",
            key=f"answer_input_{index}",
        )
        submitted = st.form_submit_button("답 제출", type="primary", use_container_width=True)
    if submitted:
        answer = st.session_state[f"answer_input_{index}"].strip()
        if not answer:
            st.warning("영어 답을 입력해 주세요.")
        else:
            correct_answer = answer_key.get(prompt)
            if correct_answer is None:
                result = "unavailable"
            elif normalize_answer(answer) == normalize_answer(correct_answer):
                result = "correct"
            else:
                result = "incorrect"
            st.session_state.feedback = {
                "prompt": prompt,
                "answer": answer,
                "correct_answer": correct_answer or "",
                "result": result,
            }
            st.rerun()

with st.expander("사용 방법"):
    st.write(
        "문장을 한 번씩 무작위 순서로 풀고, 답을 입력하고 Enter 또는 제출 버튼을 누르면 정답 여부를 확인합니다. 채점 후 다음 화면의 입력란에서 Enter 또는 다음 버튼을 누르면 이동합니다. "
        f"현재 답지에서 확인된 문장은 {len(answer_key)}개입니다. "
        "답지에서 찾지 못한 문장은 자동 채점하지 않습니다. "
        "입력 기록은 이 브라우저 세션에서 라운드가 끝날 때까지 볼 수 있습니다."
    )
