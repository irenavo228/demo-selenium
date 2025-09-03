# 1. (Optional) Activate your venv
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
.\.venv\Scripts\activate         # Windows PowerShell

# 2. Download drivers
chrome: https://googlechromelabs.github.io/chrome-for-testing/
firefox: https://github.com/mozilla/geckodriver/releases/ 
Note: Must be same version with Chrome and Firefox browser on PC.

# 2. Install libs
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
npm install -g allure-commandline

# 3. Run test
pytest --browser=chrome --env=local --mode=headed tests/test_login.py -v
python gen_report.py

# 4. Build image on Docker:
docker buildx build -t demo-selenium:latest ../demo-selenium
