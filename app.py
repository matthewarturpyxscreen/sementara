import streamlit as st
import pandas as pd

# ===================================
# CONFIG
# ===================================
st.set_page_config(page_title="Portal NPSN Anti Lag", layout="wide")

# ===================================
# 🎨 CSS + STICKMAN ANIMATION
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

/* AREA ANIMASI */
.fight-area{
    display:flex;
    justify-content:center;
    gap:60px;
    margin-top:20px;
}

/* STICKMAN BODY */
.stickman{
    position:relative;
    width:120px;
    height:200px;
    animation: fight 1.2s infinite alternate ease-in-out;
}

/* FOTO JADI KEPALA BULAT */
.head{
    width:90px;
    height:90px;
    border-radius:50%;
    object-fit:cover;
    position:absolute;
    top:0;
    left:15px;
    border:4px solid white;
    box-shadow:0 6px 18px rgba(0,0,0,0.2);
}

/* BADAN */
.body{
    position:absolute;
    top:90px;
    left:58px;
    width:4px;
    height:70px;
    background:#111;
}

/* TANGAN */
.arm{
    position:absolute;
    width:60px;
    height:4px;
    background:#111;
    top:110px;
    left:30px;
    transform-origin:left;
}

/* KAKI */
.leg{
    position:absolute;
    width:60px;
    height:4px;
    background:#111;
    top:160px;
    left:30px;
    transform-origin:left;
}

/* ANIMASI BERANTEM */
@keyframes fight{
    0% { transform: rotate(-6deg) translateY(0px);}
    100% { transform: rotate(6deg) translateY(-8px);}
}

</style>
""", unsafe_allow_html=True)

# ===================================
# NAVBAR
# ===================================
st.markdown("""
<div class="navbar">
<h3>🎓 Portal Data Sekolah — ANTI LAG TOTAL</h3>
</div>
""", unsafe_allow_html=True)

# ===================================
# 🥊 STICKMAN FIGHT AREA
# ===================================
st.markdown("""
<div class="fight-area">

<div class="stickman">
<img src="foto1.jpg" class="head">
<div class="body"></div>
<div class="arm" style="transform:rotate(25deg);"></div>
<div class="leg" style="transform:rotate(-20deg);"></div>
</div>

<div class="stickman">
<img src="foto2.jpg" class="head">
<div class="body"></div>
<div class="arm" style="transform:rotate(-25deg);"></div>
<div class="leg" style="transform:rotate(20deg);"></div>
</div>

<div class="stickman">
<img src="foto3.jpg" class="head">
<div class="body"></div>
<div class="arm" style="transform:rotate(30deg);"></div>
<div class="leg" style="transform:rotate(-15deg);"></div>
</div>

<div class="stickman">
<img src="foto4.jpg" class="head">
<div class="body"></div>
<div class="arm" style="transform:rotate(-30deg);"></div>
<div class="leg" style="transform:rotate(15deg);"></div>
</div>

</div>
""", unsafe_allow_html=True)

# ===================================
# 🎧 PLAYER
# ===================================
st.markdown("### 🎧 Player")

media_link = st.text_input("Masukkan Link YouTube")

if media_link:

    embed_url=None

    if "list=" in media_link:
        playlist_id=media_link.split("list=")[-1].split("&")[0]
        embed_url=f"https://www.youtube.com/embed/videoseries?list={playlist_id}&autoplay=1&loop=1"

    elif "watch?v=" in media_link:
        video_id=media_link.split("watch?v=")[-1].split("&")[0]
        embed_url=f"https://www.youtube.com/embed/{video_id}?autoplay=1"

    elif "youtu.be/" in media_link:
        video_id=media_link.split("youtu.be/")[-1].split("?")[0]
        embed_url=f"https://www.youtube.com/embed/{video_id}?autoplay=1"

    if embed_url:
        st.components.v1.iframe(embed_url,height=520)

# ===================================
# 🔎 SEARCH
# ===================================
st.markdown("### 🔎 Pencarian")

c1,c2,c3=st.columns([1,2,1])

with c2:
    sheet_url=st.text_input("Masukkan Link Spreadsheet")
    sheet_filter_input=st.text_input("Filter Sheet (pisahkan koma)")
    npsn=st.text_input("Masukkan NPSN")

# ===================================
# LOAD DATA (ANTI LAG)
# ===================================
@st.cache_data(show_spinner=False)
def load_data(url,filters):

    if "docs.google.com" in url:
        url=url.replace("/edit?usp=sharing","/export?format=xlsx")

    excel=pd.ExcelFile(url)

    selected=[]
    if filters:
        for name in filters:
            if name in excel.sheet_names:
                selected.append(name)
    else:
        selected=excel.sheet_names

    all_df=[]

    for sheet_name in selected:

        raw=pd.read_excel(excel,sheet_name=sheet_name,header=None)

        header_row=None
        for i in range(min(10,len(raw))):
            row_values=raw.iloc[i].astype(str).str.lower().tolist()
            if any("npsn" in v for v in row_values):
                header_row=i
                break

        if header_row is not None:
            df=raw.iloc[header_row+1:].copy()
            df.columns=raw.iloc[header_row].astype(str).str.lower().str.strip()
        else:
            df=raw.copy()
            df.columns=[f"kolom_{i}" for i in range(len(df.columns))]

        df["source_sheet"]=sheet_name
        df=df.loc[:,~df.columns.duplicated()]
        all_df.append(df)

    final_df=pd.concat(all_df,ignore_index=True,sort=False)
    return final_df.reset_index(drop=True)

# ===================================
# RESULT SUPER CEPAT
# ===================================
if sheet_url:

    filters=[s.strip() for s in sheet_filter_input.split(",")] if sheet_filter_input else []

    if "cached_df" not in st.session_state:
        st.session_state.cached_df=load_data(sheet_url,filters)

    df=st.session_state.cached_df

    if npsn and "npsn" in df.columns:

        hasil=df[df["npsn"].astype(str)==str(npsn)]

        if len(hasil)>0:
            st.dataframe(hasil,use_container_width=True,hide_index=True)
        else:
            st.warning("Data tidak ditemukan")
