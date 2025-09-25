import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from data_preprocessing import preprocess_data
from cost_estimation import calculate_cost

# -------------------
# Page Config
# -------------------
st.set_page_config(
    page_title="AI Flight Delay Cost Estimator",
    page_icon="✈️",
    layout="wide"
)

# -------------------
# Custom CSS
# -------------------
st.markdown("""
    <style>
    /* Global Background */
    .stApp {
        background-color: #F8FAFC;
        font-family: 'Segoe UI', Tahoma, sans-serif;
    }

    /* Header */
    .custom-header {
        background: linear-gradient(90deg, #1E3A8A, #2563EB);
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .custom-header h1 {
        color: white;
        font-size: 34px;
        font-weight: bold;
        margin-bottom: 8px;
    }
    .custom-header p {
        color: #E0E7FF;
        font-size: 15px;
        margin: 0;
    }

    /* Upload Box */
    .upload-box {
        border: 2px dashed #2563EB;
        padding: 25px;
        border-radius: 12px;
        background: #FFFFFF;
        text-align: center;
        box-shadow: 0 3px 10px rgba(0,0,0,0.05);
        margin-bottom: 25px;
    }

    /* KPI Metric Cards */
    .metric-card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 3px 10px rgba(0,0,0,0.08);
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-3px);
    }
    .metric-card h3 {
        font-size: 16px;
        color: #475569;
        margin-bottom: 6px;
    }
    .metric-card p {
        font-size: 22px;
        font-weight: bold;
        color: #2563EB;
        margin: 0;
    }

    /* Section Titles */
    .section-title {
        font-size: 20px;
        font-weight: 600;
        color: #1E40AF;
        margin-top: 30px;
        margin-bottom: 10px;
    }

    /* Footer */
    .footer {
        text-align: center;
        margin-top: 40px;
        padding: 12px;
        color: gray;
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------
# Header
# -------------------
st.markdown("""
<div class="custom-header">
    <h1>AI-Based Flight Delay Cost & Emission Estimator</h1>
    <p>Predict delays, estimate financial losses, and calculate environmental impact for Indian Airlines</p>
</div>
""", unsafe_allow_html=True)

# -------------------
# Load Model
# -------------------
try:
    model = joblib.load("delay_model.pkl")
except:
    st.error("⚠️ Model not found. Please train the model first using `model_training.py`.")
    st.stop()

# -------------------
# Layout
# -------------------
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("<div class='upload-box'>📂 <b>Upload Flight Dataset (CSV)</b></div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["csv"])
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.success("File uploaded successfully!")
            st.write("### Preview of Uploaded Data", df.head())
        except Exception as e:
            st.warning("⚠️ Could not read the uploaded file as a CSV. Showing raw file preview not available.")
            st.stop()

with col2:
    st.info("🌍 Every minute of flight delay adds ~50 kg CO₂ emissions and ₹1,000+ in financial loss")

# -------------------
# Main App Logic
# -------------------
if uploaded_file:
    # Validate required columns first
    required_cols = ["Airline", "Origin", "Destination"]
    missing_cols = [c for c in required_cols if c not in df.columns]

    if missing_cols:
        # If user uploaded wrong dataset: show friendly warning and raw dataset only (no further processing)
        st.warning(f"⚠️ Uploaded dataset does not match the required format. Missing columns: {', '.join(missing_cols)}.")
        st.dataframe(df, use_container_width=True)

    else:
        # Try full pipeline; if anything fails, fall back to showing raw dataset (no crash)
        try:
            # Preprocess
            df_encoded = preprocess_data(df)

            # Predict Delay
            X = df_encoded.drop(columns=["DelayMinutes", "FlightID", "ScheduledDeparture"], errors="ignore")
            predictions = model.predict(X)
            df["PredictedDelay"] = predictions

            # Calculate Costs
            df["EstimatedCost"] = df["PredictedDelay"].apply(lambda x: calculate_cost(x)["TotalCost"])
            df["CarbonCost"] = df["PredictedDelay"] * 50 * 20  # 50 kg CO₂ per min * ₹20/kg

            # Filters & Search
            st.markdown("<div class='section-title'>🔎 Search & Filter Flights</div>", unsafe_allow_html=True)
            search_airline = st.text_input("✈️ Search by Airline", "").strip().lower()
            departure_filter = st.selectbox("🛫 Departure Airport", ["All"] + sorted(df["Origin"].unique().tolist()))
            destination_filter = st.selectbox("🛬 Destination Airport", ["All"] + sorted(df["Destination"].unique().tolist()))

            filtered_df = df.copy()
            if search_airline:
                filtered_df = filtered_df[filtered_df["Airline"].str.lower().str.contains(search_airline)]
            if departure_filter != "All":
                filtered_df = filtered_df[filtered_df["Origin"] == departure_filter]
            if destination_filter != "All":
                filtered_df = filtered_df[filtered_df["Destination"] == destination_filter]

            # Show Results
            st.subheader("Results with Cost Estimation")
            st.dataframe(filtered_df[["FlightID", "Airline", "Origin", "Destination", "PredictedDelay", "EstimatedCost", "CarbonCost"]])

            # KPIs
            st.subheader("Key Insights")
            kpi1, kpi2, kpi3 = st.columns(3)
            kpi1.metric("Avg Predicted Delay (mins)", f"{filtered_df['PredictedDelay'].mean():.1f}")
            kpi2.metric("Avg Estimated Cost (₹)", f"{filtered_df['EstimatedCost'].mean():,.0f}")
            kpi3.metric("Total Carbon Cost (₹)", f"{filtered_df['CarbonCost'].sum():,.0f}")

            # Charts
            st.subheader("Airline-wise Average Delay Cost")
            if not filtered_df.empty:
                chart_data = filtered_df.groupby("Airline")["EstimatedCost"].mean().sort_values()
                st.bar_chart(chart_data)

            st.subheader("Delay Distribution")
            if not filtered_df.empty:
                fig, ax = plt.subplots()
                filtered_df["PredictedDelay"].hist(bins=20, ax=ax, color="skyblue", edgecolor="black")
                ax.set_title("Predicted Delay Distribution")
                ax.set_xlabel("Minutes")
                ax.set_ylabel("Flights")
                st.pyplot(fig)

            # Download
            st.download_button("⬇ Download Results as CSV", filtered_df.to_csv(index=False), "results.csv", "text/csv")

        except Exception:
            # If any error occurs during processing/prediction, don't crash — show raw dataset and a warning.
            st.warning("⚠️ Uploaded dataset is incompatible with the prediction pipeline or an internal error occurred. Showing raw dataset only.")
            st.dataframe(df, use_container_width=True)

# -------------------
# Footer
# -------------------
st.markdown("<div class='footer'><span style='font-weight:bold; font-size:20px'>Developed by</span> <span style='font-weight:bold; font-size:20px'>Atharv Kulkarni</span> </div>", unsafe_allow_html=True)