import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set style seaborn
sns.set(style='dark')

# --- HELPER FUNCTIONS ---

def create_weather_rentals_df(df):
    weather_rentals_df = df.groupby("weather_label")["cnt"].sum().reset_index()
    weather_rentals_df = weather_rentals_df.sort_values(by="cnt", ascending=False)
    return weather_rentals_df

def create_hourly_rentals_df(df):
    # Menggunakan hour_df untuk tren jam
    hourly_rentals_df = df.groupby(["hr", "workingday"])["cnt"].mean().reset_index()
    return hourly_rentals_df

# --- LOAD DATA ---

# Memuat dataset
day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")

# Konversi dteday ke datetime
day_df["dteday"] = pd.to_datetime(day_df["dteday"])
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])

# Mapping Label (Cleaning)
weather_mapping = {
    1: "Clear/Partly Cloudy",
    2: "Mist/Cloudy",
    3: "Light Snow/Rain",
    4: "Severe Weather"
}

day_df["weather_label"] = day_df["weathersit"].map(weather_mapping)
hour_df["weather_label"] = hour_df["weathersit"].map(weather_mapping)

# --- SIDEBAR ---

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2972/2972185.png") # Icon sepeda
    
    # Menentukan rentang tanggal
    min_date = day_df["dteday"].min()
    max_date = day_df["dteday"].max()
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter dataframe utama berdasarkan tanggal
main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                 (day_df["dteday"] <= str(end_date))]

# Filter untuk data jam (disesuaikan dengan tanggal yang dipilih)
main_hour_df = hour_df[(hour_df["dteday"] >= str(start_date)) & 
                       (hour_df["dteday"] <= str(end_date))]

# Menyiapkan dataframe untuk visualisasi
weather_df = create_weather_rentals_df(main_df)
hourly_df = create_hourly_rentals_df(main_hour_df)

# --- MAIN PAGE ---

st.header('Bike Sharing Dashboard 🚲')

# Row 1: Dashboard Metrics
st.subheader('Daily Rentals Overview')
col1, col2, col3 = st.columns(3)

with col1:
    total_rentals = main_df.cnt.sum()
    st.metric("Total Rentals", value=f"{total_rentals:,}")

with col2:
    total_casual = main_df.casual.sum()
    st.metric("Casual Users", value=f"{total_casual:,}")

with col3:
    total_registered = main_df.registered.sum()
    st.metric("Registered Users", value=f"{total_registered:,}")

# Row 2: Pengaruh Musim & Cuaca
st.subheader("Faktor Lingkungan terhadap Penyewaan")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(20, 8))

# Plot Cuaca
sns.barplot(x="cnt", y="weather_label", data=weather_df, palette="magma", ax=ax[1])
ax[1].set_title("Penyewaan Berdasarkan Kondisi Cuaca", loc="center", fontsize=18)
ax[1].set_xlabel(None)
ax[1].set_ylabel(None)

st.pyplot(fig)

# Row 3: Tren Jam (Working Day vs Weekend)
st.subheader("Tren Jam Penyewaan: Hari Kerja vs Akhir Pekan")

fig, ax = plt.subplots(figsize=(16, 8))
sns.lineplot(
    x="hr", 
    y="cnt", 
    hue="workingday", 
    data=hourly_df, 
    marker="o", 
    palette=["#E64A19", "#1976D2"],
    ax=ax
)
ax.set_title("Rata-rata Penyewaan per Jam", loc="center", fontsize=20)
ax.set_xlabel("Jam (0-23)", fontsize=15)
ax.set_ylabel("Rata-rata Jumlah Sepeda", fontsize=15)
ax.set_xticks(range(0, 24))
ax.legend(title="Tipe Hari", labels=["Hari Libur", "Hari Kerja"], fontsize=12)
ax.grid(True, alpha=0.3)

st.pyplot(fig)

st.caption("Copyright © 2024 - Bike Sharing Analysis Project")