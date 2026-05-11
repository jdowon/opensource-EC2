import streamlit as st
import json

# 1. 첫 화면 조건 (학번, 이름 표시)
st.set_page_config(page_title="Streamlit 퀴즈 배포 실습", page_icon="💻")
st.title("💻 오픈소스 전공 상식 퀴즈: Streamlit 편")
st.subheader("학번: 2025404003 / 이름: 정도원")
st.markdown("---")

# 세션 상태 초기화
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'current_user' not in st.session_state:
    st.session_state['current_user'] = ""

# 2. 로그인 화면
if not st.session_state['logged_in']:
    st.write("퀴즈를 시작하려면 로그인이 필요합니다.")
    st.info("💡 테스트 계정 - 아이디: admin / 비밀번호: 1234") 
    
    user_id = st.text_input("아이디")
    user_pw = st.text_input("비밀번호", type="password")
    
    if st.button("로그인"):
        # [로그 추가] 로그인 시도 시 터미널에 표시
        print(f"🚀 [시스템 로그] 로그인 시도 아이디: {user_id}")
        
        if user_id == "admin" and user_pw == "1234":
            st.session_state['logged_in'] = True
            st.session_state['current_user'] = user_id
            print(f"✅ [시스템 로그] '{user_id}' 계정 로그인 성공") # [로그 추가]
            st.rerun()
        else:
            st.error("아이디 또는 비밀번호가 틀렸습니다.")
            print(f"❌ [시스템 로그] '{user_id}' 계정 로그인 실패") # [로그 추가]

# 3. 로그인 성공 시 화면
if st.session_state['logged_in']:
    
    st.success(f"🎉 로그인 성공! 현재 **'{st.session_state['current_user']}'** 계정으로 접속 중입니다.")
    
    if st.button("로그아웃"):
        print(f"🚪 [시스템 로그] '{st.session_state['current_user']}' 계정 로그아웃") # [로그 추가]
        st.session_state['logged_in'] = False
        st.session_state['current_user'] = ""
        st.rerun()
        
    st.markdown("---")

    # 4. 캐싱 기능 (파일 읽기)
    @st.cache_data
    def load_questions():
        # 이 로그는 캐싱 덕분에 '최초 1회'만 터미널에 찍힙니다.
        print("📂 [시스템 로그] questions.json 파일을 새로 읽어왔습니다 (Cache Miss)") 
        with open('questions.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    
    try:
        questions = load_questions()
    except FileNotFoundError:
        st.error("questions.json 파일이 없습니다.")
        st.stop()

    # 5. 퀴즈 폼
    with st.form(key='quiz_form'):
        for q in questions:
            st.write(f"**Q{q['id']}. {q['question']}**")
            # 세션 스테이트를 이용해 정답 저장
            st.radio("정답을 선택하세요:", q['options'], key=f"q_{q['id']}")
            st.write("---")
        
        submit_button = st.form_submit_button(label='채점하기')

    # 6. 채점 로직
    if submit_button:
        score = 0
        total_questions = len(questions)

        for q in questions:
            user_answer = st.session_state.get(f"q_{q['id']}")
            if user_answer == q['answer']:
                score += 1

        # [로그 추가] 과제의 핵심! 채점 시 터미널에 점수 출력
        print(f"📊 [시스템 로그] '{st.session_state['current_user']}' 님이 채점을 요청함. 점수: {score}/{total_questions}")

        st.subheader("📝 퀴즈 결과")
        st.write(f"총 {total_questions}문제 중 **{score}문제**를 맞히셨습니다!")

        if score == total_questions:
            st.balloons()
            st.success("🎉 만점입니다! 완벽해요!")
        elif score > 0:
            st.info("👍 아쉽지만 잘 하셨습니다!")
        else:
            st.error("😭 다시 공부가 필요할 것 같아요!")