import streamlit as st
import pandas as pd
import requests

# =============================
# PAGE CONFIG
# =============================

st.set_page_config(
    page_title="Website NPSN",
    layout="wide"
)

# =============================
# 🔥 CUSTOM CSS ANIMASI
# =============================

st.markdown("""
<style>
.main-title {
    font-size:40px;
    font-weight:bold;
    text-align:center;
    animation: fadeIn 1.5s ease-in-out;
}
@keyframes fadeIn {
    from {opacity:0; transform: translateY(20px);}
    to {opacity:1; transform: translateY(0);}
}
.block-container {
    padding-top:1rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🔎 Pencarian Data Sekolah (NPSN)</p>', unsafe_allow_html=True)

# =============================
# 🎬 VIDEO PLAYLIST YOUTUBE
# =============================

st.subheader("🎧 Playlist Video")

playlist_url = st.text_input(
    "Masukkan link Playlist YouTube",
    placeholder="https://www.youtube.com/embed/videoseries?list=XXXX"
)

if playlist_url:
    st.video(playlist_url)

# =============================
# INPUT LINK SPREADSHEET
# =============================

st.subheader("📄 Data Spreadsheet")

sheet_url = st.text_input(
    "Masukkan link Spreadsheet (Google Sheet / Excel / CSV)"
)

# =============================
# LOAD DATA FUNCTION
# =============================

@st.cache_data
def load_data(url):

    if "docs.google.com" in url:
        url = url.replace("/edit?usp=sharing", "/export?format=csv")
        df = pd.read_csv(url)
    elif url.endswith(".csv"):
        df = pd.read_csv(url)
    else:
        df = pd.read_excel(url)

    # 🔥 Cleaning anti error
    df.columns = df.columns.astype(str).str.lower().str.strip()
    df = df.loc[:, ~df.columns.duplicated()]
    df = df.reset_index(drop=True)

    return df

# =============================
# LOAD DATA
# =============================

if sheet_url:

    try:
        df = load_data(sheet_url)

        st.success(f"Data berhasil dimuat — {len(df)} baris")

        # =============================
        # 🔎 SEARCH NPSN
        # =============================

        npsn = st.text_input("Masukkan NPSN")

        if npsn:

            if "npsn" not in df.columns:
                st.error("Kolom npsn tidak ada di data")
            else:
                hasil = df[df["npsn"].astype(str) == str(npsn)]

                if len(hasil) > 0:
                    st.subheader("✅ Data Ditemukan")
                    st.dataframe(hasil, use_container_width=True)
                else:
                    st.warning("NPSN tidak ditemukan")

        # =============================
        # PREVIEW DATA
        # =============================

        with st.expander("Preview Semua Data"):
            st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error(f"Error load data: {e}")

else:
    st.info("Masukkan link spreadsheet dulu.")
    
