# 🛡️ Sentinels-Automation-Hub

A professional-grade **Proof of Concept (POC)** for automated end-to-end testing. This framework is built using the **Python + Playwright** ecosystem, following the **Page Object Model (POM)** design pattern for maximum scalability and maintainability.

---

## 🚀 Tech Stack
* **Language:** Python 3.10+
* **Test Runner:** Pytest
* **Automation Library:** Playwright
* **Reporting:** Allure Framework
* **Pattern:** Page Object Model (POM)

---

## 🏗️ Architecture Features
* **Multi-Site Support:** Demonstrates cross-domain testing on both **SauceDemo** (E-commerce) and **OrangeHRM** (Enterprise ERP).
* **Data-Driven Testing:** Credentials and URLs are decoupled from code via `data/test_data.json`.
* **Centralized Configuration:** Managed through `pytest.ini` for consistent execution.
* **Failure Capture:** Automated screenshots and traces attached to Allure reports on failure.
* **CI/CD Ready:** Optimized for headless execution in GitHub Actions/Jenkins.

---

## 🛠️ Getting Started

### 1. Prerequisites
* Python 3.10 or higher
* (Optional) Allure CLI installed on your system

### 2. Installation
```bash
# Clone the repository
git clone [https://github.com/YOUR_USERNAME/Sentinels-Automation-Hub.git](https://github.com/YOUR_USERNAME/Sentinels-Automation-Hub.git)
cd Sentinels-Automation-Hub

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium