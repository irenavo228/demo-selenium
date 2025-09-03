# 1. (Optional) Activate your venv
python -m venv .venv
(source .venv/bin/activate        # on macOS/Linux
.\.venv\Scripts\activate         # on Windows PowerShell)

# 2. Install libs
pip install -r requirements.txt
playwright install chromium firefox

# 3. Run test
pytest --browser=chromium --env=local --mode=headed tests/test_login.py -v

# 4. Build image on Docker:
docker buildx build -t demo-playwright-session:latest ../demo-playwright-session