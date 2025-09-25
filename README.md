# ✈️ AI-Based Flight Delay Cost & Emission Estimator  

## 📌 Overview  
This project is a **FinTech + Aviation AI application** that predicts **flight delays**, estimates the **financial cost of delays**, and calculates the **environmental impact (CO₂ emissions)** for Indian Airlines.  

The application is built with **Streamlit** and provides:  
- Flight delay prediction using a trained ML model  
- Cost estimation of delays for airlines & passengers  
- Environmental impact calculation (CO₂ emissions)  
- Interactive filtering by Airline, Origin, Destination  
- Visualization dashboards (charts, KPIs, tables)  
- Exportable results in CSV  

---

## 🚀 Features  
- **Upload Flight Data** in CSV format  
- **AI-powered Delay Prediction** (using `delay_model.pkl`)  
- **Cost Estimation**: financial + carbon cost  
- **Filters**: airline, departure, destination  
- **KPIs Dashboard**: average delay, cost, carbon cost  
- **Visualization**: airline-wise cost distribution, delay histograms  
- **Download Results** as CSV  

---

## 🛠️ Tech Stack  
- **Frontend**: Streamlit  
- **Backend/ML**: scikit-learn, pandas, joblib  
- **Visualization**: Matplotlib, Streamlit charts  

---

## 📂 Project Structure  

```
AIBF-Project/
│── app.py                  # Main Streamlit application
│── requirements.txt        # Python dependencies
│── delay_model.pkl         # Trained ML model
│── data_preprocessing.py   # Preprocessing utilities
│── cost_estimation.py      # Cost calculation logic
│── README.md               # Project documentation
│── dataset/                # Sample flight datasets
│── docs/                   # Report / Documentation
```

---

## ⚡ Installation & Setup  

### 1️⃣ Clone the repository  
```bash
git clone https://github.com/your-username/AIBF-project.git
cd AIBF-project
```

### 2️⃣ Create virtual environment (optional but recommended)  
```bash
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
```

### 3️⃣ Install dependencies  
```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Streamlit app  
```bash
streamlit run app.py
```

---

## 🌍 Deployment (Streamlit Cloud)  
1. Push your repo to GitHub.  
2. Go to [Streamlit Cloud](https://share.streamlit.io).  
3. Select your repo → branch `main` → file path `app.py`.  
4. Deploy 🚀 and get your public link.  

---

## 📊 Example Screenshot  

*(Add your app screenshot here after deployment)*  

---

## 👨‍💻 Developed By  
**Atharv Kulkarni**  
ATC-AI FinTech Project | 2025  
