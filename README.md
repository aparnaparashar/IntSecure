# IntSecure - Your AI-powered watchdog for shady transactions.

**IntSecure** is a machine learning-based fraud detection system designed to identify potentially fraudulent transactions in real time. It provides a clean web interface where users can input transaction details and receive instant feedback on whether the transaction is likely to be fraudulent.

### System Architecture

┌────────────────────┐ ┌───────────────────────┐ ┌────────────────────────┐
│ User Interface │ ─────▶ │ Flask Backend │ ─────▶ │ ML Model (pkl files) │
│ (HTML, Tailwind) │ ◀───── │ (app.py handles form) │ ◀───── │ fraud_model + scaler │
└────────────────────┘ └───────────────────────┘ └────────────────────────┘

User submits transaction         Backend receives and         Model predicts fraud or not,
   details via form              scales inputs                sends response back to user

### Features

* Real-time fraud detection based on transaction metadata
* Trained logistic regression model using a public fraud dataset
* Scalable and modular architecture using Flask
* Clean, responsive interface with Tailwind CSS
* Ready for deployment on cloud platforms like Render or Heroku

### Tech Stack

| Layer         | Tools Used                      |
| ------------- | ------------------------------- |
| Frontend      | HTML, Tailwind CSS              |
| Backend       | Python, Flask                   |
| ML Framework  | scikit-learn, pandas, joblib    |
| Model Outputs | `fraud_model.pkl`, `scaler.pkl` |


### Dataset Information

* **Name**: `payment_fraud.csv`
* **Fields Used for Prediction**:

  * Transaction Amount
  * Account Balance Before
  * Account Balance After
  * Receiver Balance Before
  * Receiver Balance After
  * Hour of Day
* **Target Variable**: `label` (`1` for fraud, `0` for legitimate)

### Model Details

* **Algorithm**: Logistic Regression
* **Preprocessing**: Numeric scaling via `StandardScaler`
* **Saved Files**:

  * `fraud_model.pkl`: trained classifier
  * `scaler.pkl`: fitted scaler used for preprocessing
* **Training Environment**: `model.ipynb`

### Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/intsecure.git
cd intsecure
```

2. **(Optional) Create a virtual environment**

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Train the model**

* Open `model.ipynb` in Jupyter Notebook
* Run the notebook to train and save:

  * `fraud_model.pkl`
  * `scaler.pkl`

5. **Run the Flask app**

```bash
python app.py
```

Sure, Aparna! Here's your cleaned-up and **perfectly separated** section of the `README.md` including:

* Proper spacing
* Bullet formatting
* Indented folder structure
* Consistent markdown styling

---

### App Access

When running locally, access the application at:

```
http://127.0.0.1:5000
```

---

### Folder Structure

```
intsecure/
├── app.py
├── model.ipynb
├── payment_fraud.csv
├── fraud_model.pkl
├── scaler.pkl
├── requirements.txt
├── templates/
│   └── index.html
├── static/
│   └── style.css
└── README.md
```

---

###  Deployment (Render or Other Platforms)

To deploy this app using Render:

1. Push your project to GitHub
2. Go to [https://render.com](https://render.com)
3. Create a new **Web Service** and connect your GitHub repo
4. Configure the service:

   * **Build Command**:

     ```
     pip install -r requirements.txt
     ```
   * **Start Command**:

     ```
     python app.py
     ```
5. Ensure the following files are present in the root of your repo:

   * `fraud_model.pkl`
   * `scaler.pkl`
   * `payment_fraud.csv`

---

###  Author

**Aparna Parashar**
© 2025 **IntSecure**. All rights reserved.



