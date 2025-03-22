Title:
Clinical Decision Support System (CDSS) for Predicting Ciprofloxacin Resistance in UTI Patients using Machine Learning

Overview:

This project is part of my MSc Computing Dissertation. It aims to tackle the rising challenge of antibiotic resistance, focusing specifically on predicting ciprofloxacin resistance in Escherichia coli for urinary tract infections (UTIs).

The solution is a lightweight Clinical Decision Support System (CDSS) powered by a logistic regression model, allowing clinicians to make data-driven decisions about antibiotic prescriptions.


🎯 Key Features
🧠 Logistic Regression-based predictor for resistance
📝 Form-based input system for patient data
📊 SHAP-based feature importance visualization
🗃️ Local SQLite database logging patient entries
📈 Use Case: Supports Clinicians, GPs, and Researchers
🔒 Focus on data security and integrity (developer role in system)

🛠️ Tech Stack
Frontend: HTML (CDSS form)
Backend: Python (Flask)
ML: scikit-learn (Logistic Regression), SHAP
Database: SQLite
Other: Pandas, NumPy, Matplotlib, Seaborn, SMOTE


Use Case:
To aid the combat against AMR by providing clinicians a low- cost efficient tool that can predict antibiotic resistance in UTI patients.

🚀 How to Run the Project Locally
1. Clone the repository
bash
Copy
Edit
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>

2. Set up virtual environment
bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

3. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt

4. Run the Flask App
bash
Copy
Edit
python app.py



🧑‍💻 Author
Nahidur Rahman
MSc Computing Dissertation | Cardiff University