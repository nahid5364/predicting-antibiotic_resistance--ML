import pandas as pd
import random

# Generate the dummy dataset
def generate_dummy_dataset():
    random.seed(42)  # For reproducibility
    
    num_entries = 2000
    data = {
       "Age": [random.randint(18, 90) for _ in range(num_entries)],
        "Gender": [random.choice(["Male", "Female", "Other"]) for _ in range(num_entries)],
        "Admission_Department": [random.choice(["Outpatient", "Inpatient"]) for _ in range(num_entries)],
        "Hospitalization_Duration": [random.choice(["Less than 5 days", "More than 5 days"]) for _ in range(num_entries)],
        "Last_Antibiotic_Exposure": [random.choice(["30 days or less", "More than 30 days"]) for _ in range(num_entries)],
        "Region": [random.choice(["Pakistan", "Saudi Arabia", "United Kingdom", "United States of America"]) for _ in range(num_entries)],
        "Ciprofloxacin": [random.choice([1, 0]) for _ in range(num_entries)],  # 1 = used, 0 = not used
        "Resistance_in_Urine": [random.choice([1, 0]) for _ in range(num_entries)],  # 1 = resistant, 0 = not resistant
        "Previous_Resistance_to_Antibiotics": [random.choice([1, 0]) for _ in range(num_entries)],  # 1 = resistant, 0 = not resistant
        "Diabetes": [random.choice([1, 0]) for _ in range(num_entries)],  # Comorbidity
        "Hypertension": [random.choice([1, 0]) for _ in range(num_entries)],  # Comorbidity
        "Chronic_Lung_Disease": [random.choice([1, 0]) for _ in range(num_entries)],  # Comorbidity
        "Cardiovascular_Disease": [random.choice([1, 0]) for _ in range(num_entries)],  # Comorbidity
        "Previous_Visits": [random.randint(0, 10) for _ in range(num_entries)],  # Number of previous visits
        "Resistance": [random.choices([1, 0], weights=[65, 35], k=1)[0] for _ in range(num_entries)]  # 65% resistant
    }
    
    df = pd.DataFrame(data)
    return df

# Generate and save the dataset
dummy_dataset = generate_dummy_dataset()
dummy_dataset.to_csv("antibiotic_resistance_dummy_dataset.csv", index=False)
print("Dataset saved as 'antibiotic_resistance_dummy_dataset.csv'")
