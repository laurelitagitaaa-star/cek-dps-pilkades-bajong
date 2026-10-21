import streamlit as st
import pandas as pd

# 1. Konfigurasi Halaman Website
st.set_page_config(page_title="Cek DPT Pilkades", page_icon="🗳️", layout="centered")

st.title("🗳️ Posko Digital Cek DPS Pilkades BAJONG")
st.write("""Silakan masukkan NIK atau Nama Lengkap Anda untuk mengecek status daftar pemilih dan lokasi TPS.""")

# 2. Membaca Data Excel
@st.cache_data
def load_data():
    df = pd.read_excel("data_dpt.xlsx", dtype={"NIK": str})
    return df

try:
    data_dpt = load_data()
    
    # 3. Pilihan Metode Pencarian
    metode = st.radio("Pilih Metode Pencarian:", ("Berdasarkan NIK", "Berdasarkan Nama"))
    
    if metode == "Berdasarkan NIK":
        input_nik = st.text_input("Masukkan 16 Digit NIK Anda:", max_chars=16)
        tombol_cari = st.button("Cari Data NIK")
        
        if tombol_cari:
            if len(input_nik) < 16:
                st.warning("⚠️ NIK harus 16 digit. Periksa kembali ketikan Anda.")
            else:
                hasil = data_dpt[data_dpt['NIK'] == input_nik.strip()]
                
                if not hasil.empty:
                    st.success("✅ DATA DITEMUKAN! Anda terdaftar sebagai pemilih.")
                    nik_sensor = input_nik[:6] + "**********"
                    
                    st.info(f"""
                    * **NIK:** {nik_sensor}
                    * **Nama Pemilih:** {hasil.iloc[0]['Nama']}
                    * **Jenis Kelamin:** {hasil.iloc[0]['JK']}
                    * **Alamat:** RT {hasil.iloc[0]['RT']} / RW {hasil.iloc[0]['RW']}
                    * **Lokasi TPS:** TPS {hasil.iloc[0]['TPS']}
                    """)
                else:
                    st.error("""❌ Data tidak ditemukan. Silakan hubungi Panitia Pilkades untuk konfirmasi lebih lanjut.""")
                    
    elif metode == "Berdasarkan Nama":
        input_nama = st.text_input("Masukkan Nama Lengkap / Sebagian Nama:")
        tombol_cari = st.button("Cari Data Nama")
        
        if tombol_cari:
            if input_nama.strip() == "":
                st.warning("⚠️ Silakan ketik nama terlebih dahulu.")
            else:
                hasil = data_dpt[data_dpt['Nama'].str.contains(input_nama, case=False, na=False)]
                
                if not hasil.empty:
                    st.success(f"✅ Ditemukan {len(hasil)} data yang cocok:")
                    tampilan_hasil = hasil.copy()
                    tampilan_hasil['NIK'] = tampilan_hasil['NIK'].apply(lambda x: str(x)[:6] + "**********" if pd.notnull(x) else x)
                    st.dataframe(tampilan_hasil[['Nama', 'JK', 'RT', 'RW', 'TPS']], use_container_width=True)
                else:
                    st.error("""❌ Nama tidak ditemukan. Silakan pastikan ejaan nama sudah benar.""")

except FileNotFoundError:
    st.error("📁 File 'data_dpt.xlsx' tidak ditemukan. Pastikan file Excel diletakkan satu folder dengan kode ini.")
