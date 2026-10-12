# Level 2 영어 문장 연습

307개의 한글 예문을 한 번에 하나씩 무작위로 보여 주는 Streamlit 앱입니다. 한 라운드 안에서는 같은 문장이 다시 나오지 않습니다. `answer_key.csv`에 정답이 있는 문장은 제출 후 자동 채점하며, 현재 답지에서 확인된 정답은 229개입니다. 나머지 문장은 자동 채점하지 않고 다음으로 진행할 수 있습니다.

정답이면 **정답!**, 틀리면 **오답**과 정답 문장을 보여 줍니다. 답을 입력한 뒤 제출 버튼을 누르고, 결과를 확인한 다음 다음 문장으로 이동합니다.

## 로컬에서 실행하기

Python 3.10 이상을 설치한 뒤 저장소 폴더에서 실행합니다.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Streamlit Community Cloud로 배포하기

1. 저장소의 `app.py`, `sentences.csv`, `answer_key.csv`, `requirements.txt`를 GitHub의 기본 브랜치에 올립니다.
2. [share.streamlit.io](https://share.streamlit.io/)에 GitHub 계정으로 로그인합니다.
3. **Create app**을 누르고 저장소 `PassionChicken-Leesuin/Culcum_Level2_Practice`, 브랜치 `main`, 진입 파일 `app.py`를 선택합니다.
4. **Deploy**를 누릅니다. 배포가 끝나면 생성된 `*.streamlit.app` 주소로 접속할 수 있습니다.

Community Cloud 무료 앱은 **12시간 동안 트래픽이 없으면 잠들며**, 다음 방문자가 앱 화면의 깨우기 버튼을 눌러 다시 시작할 수 있습니다. 이 동작을 없애려면 Streamlit Community Cloud 대신 유료 상시 실행 서비스를 사용해야 합니다.

현재 배포 주소: [level2-sentence-practice.streamlit.app](https://level2-sentence-practice.streamlit.app/)

## 깨우기 대기 없이 운영하기

같은 `app.py`를 Render 같은 서비스의 **유료 Web Service**로 배포하면 됩니다. 저장소를 연결하고 다음 값을 설정합니다.

- Runtime: Python
- Build command: `pip install -r requirements.txt`
- Start command: `streamlit run app.py --server.address 0.0.0.0 --server.port $PORT`
- Instance: 유료 인스턴스

Render의 무료 Web Service도 일정 시간 유휴 후 중지되므로, 상시 실행이 목적이면 무료 인스턴스를 선택하지 마세요. Render 설정과 요금은 배포 시점에 대시보드에서 확인하세요.

## GitHub에 올리는 기본 명령

로컬에서 변경 사항을 확인한 다음 아래 명령으로 저장소에 올립니다.

```powershell
git add app.py sentences.csv answer_key.csv requirements.txt README.md
git commit -m "Add answer checking to sentence practice"
git push -u origin main
```
