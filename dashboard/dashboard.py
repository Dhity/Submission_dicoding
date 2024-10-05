import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Load the CSV file
day_df = pd.read_csv('all_day.csv')

# Preprocessing the data
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
day_df['year'] = day_df['dteday'].dt.year
day_df['month'] = day_df['dteday'].dt.month_name().str[:3]  # Ambil singkatan bulan
day_df['weekday'] = day_df['weekday'].replace({
    0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'
})
day_df['season'] = day_df['season'].replace({
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
})
day_df['weathersit'] = day_df['weathersit'].replace({
    1: 'Clear', 2: 'Mist', 3: 'Light Snow', 4: 'Heavy Rain'
})

# Set up the Streamlit page
st.set_page_config(page_title="Dashboard Penyewaan Sepeda")

# Dashboard title
st.title("Dashboard Analisis Penyewaan Sepeda")

# 1. Trend Sewa Sepeda per Bulan dan Tahun
st.subheader("Trend Sewa Sepeda per Bulan dan Tahun")

# Konversi 'mnth' menjadi kategori yang terurut
day_df['mnth'] = pd.Categorical(day_df['month'], categories=[
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    ordered=True)

# Menghitung total 'cnt' per bulan dan tahun
monthly_counts = day_df.groupby(["mnth", "year"])["cnt"].sum().reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(
    data=monthly_counts,
    x="mnth",  
    y="cnt",   
    hue="year",  
    palette=["yellow", "brown"]
)

# Memberikan judul dan penyesuaian pada plot
ax.set_title("Trend Sewa Sepeda", fontsize=14)
ax.set_xlabel("Bulan", fontsize=12)
ax.set_ylabel("Total Sewa", fontsize=12)
ax.legend(title="Tahun", loc="upper right")
plt.tight_layout()  
st.pyplot(fig)

# 2. Jumlah Pengguna Sepeda berdasarkan Musim
st.subheader("Jumlah Pengguna Sepeda berdasarkan Musim")

# Menghitung jumlah pengguna sepeda per musim
byseason_df = day_df.groupby(by="season").cnt.sum().reset_index()

# Mengganti nama kolom untuk memudahkan interpretasi
byseason_df.rename(columns={"cnt": "total_count"}, inplace=True)

plt.figure(figsize=(10, 5))
sns.barplot(
    y="total_count", 
    x="season",
    data=byseason_df.sort_values(by="total_count", ascending=False),
    palette=["brown", "yellow", "yellow", "yellow"]
)

# Menambahkan judul dan penyesuaian pada plot
plt.title("Jumlah Pengguna Sepeda berdasarkan Musim", loc="center", fontsize=15)
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis='x', labelsize=12)
plt.tight_layout()
st.pyplot(plt)

# 3. Jumlah Pengguna Sepeda berdasarkan Kondisi Cuaca
st.subheader("Jumlah Pengguna Sepeda berdasarkan Kondisi Cuaca")

# Menghitung jumlah pengguna sepeda per kondisi cuaca
byweathersit_df = day_df.groupby(by="weathersit").cnt.sum().reset_index()

# Mengganti nama kolom untuk memudahkan interpretasi
byweathersit_df.rename(columns={"cnt": "total_count"}, inplace=True)

plt.figure(figsize=(10, 5))
sns.barplot(
    y="total_count", 
    x="weathersit",
    data=byweathersit_df.sort_values(by="total_count", ascending=False),
    palette=["brown", "yellow", "yellow"]
)

# Menambahkan judul dan penyesuaian pada plot
plt.title("Jumlah Pengguna Sepeda berdasarkan Kondisi Cuaca", loc="center", fontsize=15)
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis='x', labelsize=12)
plt.tight_layout()
st.pyplot(plt)

# 4. Perbandingan Penyewa Sepeda: Working Day vs Holiday
st.subheader("Perbandingan Penyewa Sepeda: Working Day vs Holiday")

# Menghitung jumlah pengguna sepeda berdasarkan working day dan holiday
byworkingday_df = day_df.groupby(by="workingday").cnt.sum().reset_index()

# Mengganti nama kolom untuk memudahkan interpretasi
byworkingday_df.rename(columns={"cnt": "total_count"}, inplace=True)

plt.figure(figsize=(10, 6))
sns.barplot(
    x='workingday',  
    y='total_count',         
    data=byworkingday_df,    
    palette=["yellow", "brown"]
)

# Menambahkan judul dan penyesuaian pada plot
plt.title('Perbandingan Penyewa Sepeda: Working Day vs Holiday', fontsize=14)
plt.xlabel(None)  
plt.ylabel('Jumlah Pengguna Sepeda', fontsize=12) 
plt.xticks(ticks=[0, 1], labels=['Holiday', 'Working Day']) 
plt.tight_layout()
st.pyplot(plt)

# 5. Perbandingan Penyewa Sepeda Setiap Hari
st.subheader("Perbandingan Penyewa Sepeda Setiap Hari")

# Menghitung jumlah pengguna sepeda berdasarkan hari dalam seminggu
byweekday_df = day_df.groupby(by="weekday").cnt.sum().reset_index()

# Mengganti nama kolom untuk memudahkan interpretasi
byweekday_df.rename(columns={"cnt": "total_count"}, inplace=True)

plt.figure(figsize=(10, 6))
sns.barplot(
    x='weekday',  
    y='total_count',      
    data=byweekday_df,  
    order=['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],  
    palette=["yellow", "yellow", "yellow", "yellow", "yellow", "brown", "yellow"]
)

# Menambahkan judul dan penyesuaian pada plot
plt.title('Perbandingan Penyewa Sepeda Setiap Hari', fontsize=14)
plt.xlabel(None)  
plt.ylabel('Jumlah Pengguna Sepeda', fontsize=12)
plt.tight_layout()
st.pyplot(plt)
