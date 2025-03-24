# TEG
python -m venv .venv
windows:
.venv\Scripts\activate
mac:
source ./.venv/bin/Activate

pip install -r requirements.txt

streamlit run frontend/app.py
python backend/app.py