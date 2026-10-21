import streamlit as st
import pandas as pd
st.set_page_config(page_title="Cek DPT Pilkades", page_icon="■■", layout="centered")
st.title("■■ Sistem Cek DPT Online Pilkades")
st.write("Silakan masukkan NIK atau Nama Lengkap Anda untuk mengecek status daftar pemilih dan lokasi TPS.")
@st.cache_data
def load_data():
try:
    df = pd.read_excel("data_dpt.xlsx")
    df['NIK'] = df['NIK'].astype(str).str.strip()
    df['Nama Lengkap'] = df['Nama Lengkap'].astype(str).str.upper().str.strip()
    return df
except Exception as e:
    st.error(f"Gagal memuat database DPT: {e}")
    return None
df = load_data()
if df is not None:
search_option = st.radio("Metode Pencarian:", ("Berdasarkan NIK", "Berdasarkan Nama"))
if search_option == "Berdasarkan NIK":
nik_input = st.text_input("Masukkan 16 Digit NIK Anda:", max_chars=16)
tombol = st.button("Cari Data")
if tombol:
if len(nik_input) != 16 or not nik_input.isdigit():
st.warning("■■ NIK harus berjumlah 16 digit angka.")
else:
hasil = df[df['NIK'] == nik_input.strip()]
if not hasil.empty:
st.success("■ Data Ditemukan!")
for idx, row in hasil.iterrows():
st.markdown(f"""
- **Nama:** {row['Nama Lengkap']}
- **Jenis Kelamin:** {row['Jenis Kelamin']}
- **RT/RW:** {row['RT/RW']}
- **Lokasi Memilih:** :green[{row['TPS']}]
""" )
else:
st.error("■ Data tidak ditemukan. Silakan hubungi Panitia Pilkades untuk konfirmasi.")
else:
nama_input = st.text_input("Masukkan Nama Lengkap (Sesuai KTP):")
tombol = st.button("Cari Data")
if tombol:
if nama_input.strip() == "":
st.warning("■■ Silakan masukkan nama terlebih dahulu.")
else:
hasil = df[df['Nama Lengkap'].str.contains(nama_input.upper().strip(), na=False)]
if not hasil.empty:
st.success(f"■ Menampilkan {len(hasil)} data yang cocok:")
st.dataframe(hasil[['Nama Lengkap', 'Jenis Kelamin', 'RT/RW', 'TPS']], use_contai
ner_width=True)
else:
st.error("■ Nama tidak ditemukan atau belum terdaftar.")
