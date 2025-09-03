# 1. (Optional) Activate your venv
python -m venv .venv
(source .venv/bin/activate        # on macOS/Linux
.\.venv\Scripts\activate         # on Windows PowerShell)

# 2. Install libs
pip install playwright beautifulsoup4 pytest pytest-rerunfailures pytest-order allure-pytest docker
playwright install

# 3. Install hết lib từ file requirements
pip install -r requirements.txt


Tạo sẵn image trên Docker:
docker buildx build -t demo-playwright-session:latest ../demo-playwright-session


