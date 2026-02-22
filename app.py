import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Pencarian Data NPSN",
    layout="wide"
)

st.title("🔎 Pencarian Data Berdasarkan NPSN")

# ==============================
# INPUT LINK SPREADSHEET
# ==============================

sheet_url = st.text_input(
    "Masukkan link Spreadsheet (Excel / CSV / Google Sheet export link)"
)

# ==============================
# FUNCTION LOAD DATA
# ==============================

@st.cache_data
def load_data(url):
    try:
        if "docs.google.com" in url:
            # convert google sheet ke CSV
            url = url.replace("/edit?usp=sharing", "/export?format=csv")
            df = pd.read_csv(url)
        elif url.endswith(".csv"):
            df = pd.read_csv(url)
        else:
            df = pd.read_excel(url)

        # normalisasi nama kolom
        df.columns = df.columns.str.lower()

        return df
    except Exception as e:
        st.error(f"Gagal load data: {e}")
        return None


# ==============================
# LOAD DATA
# ==============================

if sheet_url:

    df = load_data(sheet_url)

    if df is not None:

        st.success(f"Data berhasil dimuat. Total baris: {len(df)}")

        # ==============================
        # INPUT NPSN
        # ==============================

        npsn = st.text_input("Masukkan NPSN")

        if npsn:

            if "npsn" not in df.columns:
                st.error("Kolom 'npsn' tidak ditemukan di spreadsheet")
            else:
                hasil = df[df["npsn"].astype(str) == str(npsn)]

                if len(hasil) > 0:
                    st.subheader("✅ Data Ditemukan")
                    st.dataframe(hasil, use_container_width=True)
                else:
                    st.warning("NPSN tidak ditemukan")

        # ==============================
        # PREVIEW DATA
        # ==============================

        with st.expander("Lihat semua data"):
            st.dataframe(df, use_container_width=True)

else:
    st.info("Masukkan link spreadsheet terlebih dahulu.")
