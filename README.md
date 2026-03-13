# Cyber Y2K Personal Digital Space

## 📌 Project Overview
이 프로젝트는 2000년대 초반 Y2K 감성(싸이월드 미니홈피, 개인 HTML 홈페이지 등)과 크롬(Chrome) 텍스처를 테마로 한 개인 블로그 웹 서비스입니다. 
Flask를 기반으로 구축되었으며, 향후 개인 포트폴리오 아카이빙 목적으로 확장할 예정입니다.

## 🚀 Key Features (Pages)
본 미니 프로젝트는 요구사항에 맞춰 최소 3가지 이상의 기능(엔드포인트)을 포함하고 있습니다.
1. **Home (`/`, `/home`)**: 블로그 대문 역할. 방문자 카운터 감성과 최근 작성된 로그(글) 목록을 확인할 수 있는 메인 피드입니다.
2. **Write (`/write`)**: 해커/사이버 감성의 터미널 스타일 폼에서 새로운 글(제목, 내용)을 서버로 전송하는 글쓰기 페이지입니다.
3. **Guestbook (`/guestbook`)**: 2000년대 미니홈피 스타일의 방명록. 방문자가 이름과 짧은 메시지(일촌평)를 남길 수 있는 소통 공간입니다.

## 🛠 Tech Stack
* **Backend**: Python, Flask (v3.1.2)
* **Frontend**: HTML5, CSS3 (Inline)
* **VCS**: Git & GitHub

## ⚙️ How to Run
로컬 환경에서 이 프로젝트를 실행하기 위한 방법입니다.

1. **종속성 설치**
   ```bash
   pip install -r requirements.txt