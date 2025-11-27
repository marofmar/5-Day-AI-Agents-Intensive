import streamlit as st
import requests  # API를 호출하기 위해 requests 라이브러리가 필요합니다

# ------------------------------------------------
# 기본 설정
# ------------------------------------------------
st.set_page_config(
    page_title="ADK 블로그 포스트 생성기",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 Google ADK 블로그 포스트 생성기")
st.write("FastAPI 백엔드에서 실행 중인 Google ADK 에이전트를 호출합니다.")

# ------------------------------------------------
# API 엔드포인트
# ------------------------------------------------
# FastAPI 서버가 실행 중인 주소입니다.
API_BASE_URL = "http://127.0.0.1:8000"

# ------------------------------------------------
# 메인 UI
# ------------------------------------------------

# 1. 사용자로부터 '주제' 입력받기
topic_input = st.text_input(
    label="블로그 포스트 주제를 입력하세요:",
    placeholder="예: 인공지능이 바꿀 미래의 직업"
)

# 2. '생성' 버튼
if st.button("🚀 포스트 생성하기"):
    if topic_input:
        # 3. 로딩 스피너 표시
        with st.spinner("에이전트가 Google을 검색하고 블로그 글을 작성 중입니다... ✍️"):
            try:
                # 4. FastAPI 백엔드 API 호출
                response = requests.get(
                    f"{API_BASE_URL}/generate-blog-post",
                    params={"topic": topic_input} # 쿼리 파라미터로 'topic' 전달
                )

                # 5. 응답 처리
                if response.ok:
                    data = response.json()
                    blog_post_content = data.get("blog_post")
                    
                    st.success("🎉 생성이 완료되었습니다!")
                    # 6. 결과물을 마크다운 형식으로 예쁘게 표시
                    st.markdown("---")
                    st.subheader(f"'{topic_input}'에 대한 포스트:")
                    st.markdown(blog_post_content)  # 줄바꿈 처리
                else:
                    st.error(f"API 호출 실패: {response.status_code} - {response.text}")

            except requests.exceptions.ConnectionError:
                st.error("백엔드 서버(FastAPI)에 연결할 수 없습니다. 😥")
                st.info("FastAPI 서버가 켜져 있는지(uvicorn main_api:app --reload) 확인해주세요.")
            except Exception as e:
                st.error(f"예상치 못한 오류가 발생했습니다: {e}")
    else:
        st.warning("주제를 입력해주세요!")