import streamlit as st
import pandas as pd

# 1. Konfigurasi Halaman Website
st.set_page_config(page_title="Cek DPS Pilkades", page_icon="🗳️", layout="centered")

st.title("🗳️ Posko Digital Cek DPT Pilkades")
st.write("""Silakan masukkan NIK atau Nama Lengkap Anda untuk mengecek status daftar pemilih dan lokasi TPS.""")

# 2. Membaca Data Excel
@st.cache_data
def load_data():
    df = pd.read_excel("data_dpt.xlsx", dtype={"NIK": str})
    # Membersihkan nama kolom dari spasi tidak sengaja
    df.columns = df.columns.str.strip()
    # Memastikan kolom NIK dan Nama dibersihkan dari spasi awal/akhir
    if 'NIK' in df.columns:
        df['NIK'] = df['NIK'].astype(str).str.strip()
    if 'Nama' in df.columns:
        df['Nama'] = df['Nama'].astype(str).str.strip()
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
                # Proses pencarian data NIK
                hasil = data_dpt[data_dpt['NIK'] == input_nik.strip()]
                
                if not hasil.empty:
                    st.success("✅ DATA DITEMUKAN! Anda terdaftar sebagai pemilih.")
                    nik_sensor = input_nik[:6] + "**********"
                    
                    # Mengambil baris pertama sebagai dictionary agar anti-KeyError
                    data_orang = hasil.to_dict(orient='records')[0]
                    
                    # Menampilkan data secara dinamis berdasarkan kolom yang tersedia di Excel
                    st.info(f"""
                    * **NIK:** {nik_sensor}
                    * **Nama Pemilih:** {data_orang.get('Nama', '-')}
                    * **Jenis Kelamin:** {data_orang.get('JK', '-')}
                    * **RT:** {data_orang.get('RT', '-')}
                    * **RW:** {data_orang.get('RW', '-')}
                    * **Lokasi TPS:** TPS {data_orang.get('TPS', '-')}
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
                # Mencari nama yang mengandung kata kunci
                hasil = data_dpt[data_dpt['Nama'].str.contains(input_nama.strip(), case=False, na=False)]
                
                if not hasil.empty:
                    st.success(f"✅ Ditemukan {len(hasil)} data yang cocok:")
                    tampilan_hasil = hasil.copy()
                    
                    # Menyensor NIK di tabel nama
                    tampilan_hasil['NIK'] = tampilan_hasil['NIK'].apply(lambda x: str(x)[:6] + "**********" if pd.notnull(x) else "**********")
                    
                    # Menampilkan kolom yang ada secara otomatis
                    kolom_tampil = [k for k in ['Nama', 'JK', 'RT', 'RW', 'TPS'] if k in tampilan_hasil.columns]
                    st.dataframe(tampilan_hasil[kolom_tampil], use_container_width=True)
                else:
                    st.error("""❌ Nama tidak ditemukan. Silakan pastikan ejaan nama sudah benar.""")

except FileNotFoundError:
    st.error("📁 File 'data_dpt.xlsx' tidak ditemukan. Pastikan file Excel diletakkan satu folder dengan kode ini.")
except Exception as e:
    st.error(f"⚠️ Terjadi kesalahan pembacaan data: {e}. Periksa kembali format file Excel Anda.")
