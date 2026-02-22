import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Pencarian NPSN",
    layout="wide"
)

st.title("🔎 Pencarian Data Sekolah Berdasarkan NPSN")

# =========================
# INPUT LINK
# =========================

sheet_url = st.text_input(
    "Masukkan link Spreadsheet (Google Sheet / Excel / CSV)"
)

# =========================
# LOAD DATA FUNCTION
# =========================

@st.cache_data
def load_data(url):

    if "docs.google.com" in url:
        url = url.replace("/edit?usp=sharing", "/export?format=csv")
        df = pd.read_csv(url)

    elif url.endswith(".csv"):
        df = pd.read_csv(url)

    else:
        df = pd.read_excel(url)

    # =========================
    # 🔥 CLEANING WAJIB (ANTI ERROR)
    # =========================

    # rapikan nama kolom
    df.columns = df.columns.astype(str).str.lower().str.strip()

    # hapus duplicate column (ini penyebab error kamu)
    df = df.loc[:, ~df.columns.duplicated()]

    # reset index biar rapi
    df = df.reset_index(drop=True)

    return df


# =========================
# LOAD DATA
# =========================

if sheet_url:

    try:
        df = load_data(sheet_url)

        st.success(f"Data berhasil dimuat — total {len(df)} baris")

        # =========================
        # SEARCH NPSN
        # =========================

        npsn = st.text_input("Masukkan NPSN")

        if npsn:

            if "npsn" not in df.columns:
                st.error("Kolom 'npsn' tidak ditemukan di data")
            else:
                hasil = df[df["npsn"].astype(str) == str(npsn)]

                if len(hasil) > 0:
                    st.subheader("✅ Data Ditemukan")
                    st.dataframe(hasil, use_container_width=True)
                else:
                    st.warning("NPSN tidak ditemukan")

        # =========================
        # PREVIEW DATA
        # =========================

        with st.expander("Preview Semua Data"):
            st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error(f"Terjadi error saat load data: {e}")

else:
    st.info("Masukkan link spreadsheet terlebih dahulu.")
