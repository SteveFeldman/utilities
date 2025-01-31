# Developer Tools Utilities 🚀

![GitHub Repo stars](https://img.shields.io/github/stars/SteveFeldman/utilities?style=social)
![GitHub forks](https://img.shields.io/github/forks/SteveFeldman/utilities?style=social)
![GitHub license](https://img.shields.io/github/license/SteveFeldman/utilities)
![GitHub issues](https://img.shields.io/github/issues/SteveFeldman/utilities)

## 📌 Overview

This repository contains a collection of Python scripts designed to analyze **developer workflows**, including pull request analysis, story point weighting, and cycle time calculations. These utilities help engineering teams gain actionable insights into their development processes.

## 📂 Available Scripts

### 1️⃣ [`getPRs.py`](https://github.com/SteveFeldman/utilities/blob/main/getPRs.py)
Extracts pull request (PR) data from GitHub, providing insights into review times, approvals, and contributor activity.

### 2️⃣ [`story_points_with_weights.py`](https://github.com/SteveFeldman/utilities/blob/main/story_points_with_weights.py)
Calculates weighted story points for sprint or backlog analysis, factoring in custom weightings.

### 3️⃣ [`cycle_time_jira.py`](https://github.com/SteveFeldman/utilities/blob/main/cycle_time_jira.py)
Analyzes cycle time for Jira issues by calculating the time between different workflow transitions.

### 4️⃣ [`cycle_time_jira_2file.py`](https://github.com/SteveFeldman/utilities/blob/main/cycle_time_jira_2file.py)
A variation of `cycle_time_jira.py` that processes Jira cycle time data from two input files.

---

## 🔧 Installation

Ensure you have **Python 3.8+** installed. Then, follow these steps:

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/SteveFeldman/utilities.git
cd utilities
```

### 2️⃣ Create a Virtual Environment (Optional but Recommended)
```sh
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate   # Windows
```

### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

---

## 🚀 Usage Instructions

### 1️⃣ Extract Pull Request Data (`getPRs.py`)

#### 🔹 **Description**
Fetches PR details from GitHub for further analysis.

#### 🛠️ **Configuration**
Edit the script to change the following parameters:
```python
REPO_OWNER = "your-org-or-username"
REPO_NAME = "your-repository"
GITHUB_TOKEN = "your-personal-access-token"
```

#### ▶️ **Run the Script**
```sh
python getPRs.py
```

---

### 2️⃣ Calculate Weighted Story Points (`story_points_with_weights.py`)

#### 🔹 **Description**
Processes story points and assigns custom weightings based on complexity.

#### 🛠️ **Configuration**
Modify the weighting logic in the script:
```python
WEIGHT_MAPPING = {
    "low": 1,
    "medium": 2,
    "high": 3
}
```

#### ▶️ **Run the Script**
```sh
python story_points_with_weights.py
```

---

### 3️⃣ Analyze Jira Cycle Time (`cycle_time_jira.py`)

#### 🔹 **Description**
Computes cycle time from Jira data to assess development efficiency.

#### 🛠️ **Configuration**
Edit the script to point to your **Jira data CSV file**:
```python
JIRA_DATA_FILE = "path/to/your-jira-data.csv"
```

#### ▶️ **Run the Script**
```sh
python cycle_time_jira.py
```

---

### 4️⃣ Process Jira Cycle Time from Two Files (`cycle_time_jira_2file.py`)

#### 🔹 **Description**
Similar to `cycle_time_jira.py` but processes data from two separate CSV files.

#### 🛠️ **Configuration**
Update file paths in the script:
```python
FILE_1 = "path/to/file1.csv"
FILE_2 = "path/to/file2.csv"
```

#### ▶️ **Run the Script**
```sh
python cycle_time_jira_2file.py
```

---

## 📈 Example Output

Sample JSON output for **`getPRs.py`**:
```json
{
    "PR_ID": 1234,
    "author": "johndoe",
    "review_time": "2 days",
    "approvals": 3,
    "status": "merged"
}
```

Sample weighted story point calculation:
```json
{
    "task": "Implement login API",
    "original_story_points": 5,
    "adjusted_story_points": 10
}
```

---

## 🏗️ Contributing

Contributions are welcome! Follow these steps to contribute:

1. **Fork the repository** 📌
2. **Create a feature branch** (`git checkout -b feature-xyz`) 🌱
3. **Commit your changes** (`git commit -m "Add feature XYZ"`) ✨
4. **Push the branch** (`git push origin feature-xyz`) 🚀
5. **Open a Pull Request** 📩

---

## 📜 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

## 📬 Contact & Support

- **GitHub Issues**: [Report a Bug](https://github.com/SteveFeldman/utilities/issues)
- **Email**: perfforensics@gmail.com

---

🌟 If you find this project useful, please **star the repository** and consider contributing! 🚀✨
