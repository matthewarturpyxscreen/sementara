import streamlit as st
import pandas as pd
import time

# ===================================
# CONFIG
# ===================================
st.set_page_config(page_title="Portal NPSN Anti Lag", layout="wide")

# ===================================
# 🎨 CSS
# ===================================
st.markdown("""
<style>
.stApp{background:#f4f7fb;}
.navbar{
    position:sticky;top:0;z-index:999;background:white;
    padding:18px 25px;border-radius:14px;
    box-shadow:0 6px 25px rgba(0,0,0,0.06);
    margin-bottom:25px;
}
.big-title{
    text-align:center;font-size:40px;font-weight:700;
    color:#0f172a;margin-top:30px;
}
.search-area{
    background:white;padding:35px;border-radius:16px;
    box-shadow:0 10px 40px rgba(0,0,0,0.07);
    max-width:900px;margin:auto;margin-top:20px;
}
.result-area{
    background:white;padding:20px;border-radius:14px;
    box-shadow:0 8px 30px rgba(0,0,0,0.05);
    margin-top:25px;
}
.player-full{
    background:white;padding:20px;border-radius:18px;
    box-shadow:0 15px 45px rgba(0,0,0,0.15);
    margin-top:25px;
}
</style>
""", unsafe_allow_html=True)

# ===================================
# NAVBAR
# ===================================
st.markdown("""
<div class="navbar">
<h3 style='margin:0;color:#0f172a;'>🎓 Portal Data Sekolah — ANTI LAG TOTAL</h3>
</div>
""", unsafe_allow_html=True)

# ===================================
# 📸 FOTO DEKORASI (DARI GAMBAR YANG KAMU UPLOAD)
# ===================================
colA, colB, colC, colD = st.columns(4)

with colA:
    st.image("/mnt/data/ca1e04de-46d5-47c2-8020-5adcc2fffd59.jpg", use_container_width=True)

with colB:
    st.image("/mnt/data/f243533f-6a13-4d54-9955-e3803d49df9f.jpg", use_container_width=True)

with colC:
    st.image("/mnt/data/d5f2ba3e-40e6-4f63-8282-344a8905b0e7.jpg", use_container_width=True)

with colD:
    st.image("/mnt/data/e96ef8d1-278e-439b-93f1-2e282a8aa2b5.jpg", use_container_width=True)

# ===================================
# 🎧 PLAYER FLEXIBLE
# ===================================
media_link = st.text_input("Masukkan Link YouTube (Playlist atau Video)")

if media_link:

    embed_url = None

    if "list=" in media_link:
        playlist_id = media_link.split("list=")[-1].split("&")[0]
        embed_url = f"https://www.youtube.com/embed/videoseries?list={playlist_id}&autoplay=1&loop=1"

    elif "watch?v=" in media_link:
        video_id = media_link.split("watch?v=")[-1].split("&")[0]
        embed_url = f"https://www.youtube.com/embed/{video_id}?autoplay=1"

    elif "youtu.be/" in media_link:
        video_id = media_link.split("youtu.be/")[-1].split("?")[0]
        embed_url = f"https://www.youtube.com/embed/{video_id}?autoplay=1"

    if embed_url:
        st.markdown('<div class="player-full">', unsafe_allow_html=True)
        st.components.v1.iframe(embed_url, height=520)
        st.markdown('</div>', unsafe_allow_html=True)

# ===================================
# TITLE
# ===================================
st.markdown('<p class="big-title">Cari Data Sekolah Berdasarkan NPSN</p>', unsafe_allow_html=True)

# ===================================
# SEARCH AREA
# ===================================
st.markdown('<div class="search-area">', unsafe_allow_html=True)

sheet_url = st.text_input("Masukkan Link Spreadsheet")

sheet_filter_input = st.text_input(
    "Filter Sheet (pisahkan dengan koma)",
    placeholder="Contoh: 18/2/2026, PAKE DATA INI UDAH KE UPDATE!!!"
)

npsn = st.text_input("Masukkan NPSN")

st.markdown('</div>', unsafe_allow_html=True)

# ===================================
# 🧠 LOAD DATA SEKALI SAJA (ANTI LAG TOTAL)
# ===================================
@st.cache_data(show_spinner=False)
def load_data(url, sheet_filters):

    if "docs.google.com" in url:
        url = url.replace("/edit?usp=sharing", "/export?format=xlsx")

    excel = pd.ExcelFile(url)

    selected_sheets = []

    if sheet_filters:
        for name in sheet_filters:
            if name in excel.sheet_names:
                selected_sheets.append(name)
    else:
        selected_sheets = excel.sheet_names

    all_df = []

    for sheet_name in selected_sheets:

        raw = pd.read_excel(excel, sheet_name=sheet_name, header=None)

        header_row = None
        for i in range(min(10, len(raw))):
            row_values = raw.iloc[i].astype(str).str.lower().tolist()
            if any("npsn" in v for v in row_values):
                header_row = i
                break

        if header_row is not None:
            df = raw.iloc[header_row+1:].copy()
            df.columns = raw.iloc[header_row].astype(str).str.lower().str.strip()
        else:
            df = raw.copy()
            df.columns = [f"kolom_{i}" for i in range(len(df.columns))]

        df["source_sheet"] = sheet_name
        df = df.loc[:, ~df.columns.duplicated()]
        all_df.append(df)

    final_df = pd.concat(all_df, ignore_index=True, sort=False)
    return final_df.reset_index(drop=True)

# ===================================
# RESULT SUPER CEPAT
# ===================================
if sheet_url:

    filters = [s.strip() for s in sheet_filter_input.split(",")] if sheet_filter_input else []

    # ⚡ LOAD SEKALI
    if "cached_df" not in st.session_state:
        st.session_state.cached_df = load_data(sheet_url, filters)

    df = st.session_state.cached_df

    if npsn:

        if "npsn" not in df.columns:
            st.warning("Kolom NPSN tidak ditemukan")
        else:
            hasil = df[df["npsn"].astype(str) == str(npsn)]

            if len(hasil) > 0:
                st.markdown('<div class="result-area">', unsafe_allow_html=True)
                st.dataframe(hasil, use_container_width=True, hide_index=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning("Data tidak ditemukan")
