import streamlit as st
import time

# ==============================================================================
# 1. KONFIGURASI HALAMAN & CSS
# ==============================================================================
st.set_page_config(
    page_title="OrganicChem | Edu-Lab Platform",
    page_icon="🧪",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f8fafc, #f1f5f9);
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f766e, #14b8a6);
}
[data-testid="stSidebar"] * {
    color: white !important;
}
.banner-utama {
    background: linear-gradient(135deg, #06b6d4, #3b82f6);
    padding: 35px;
    border-radius: 15px;
    color: white;
    margin-bottom: 30px;
    box-shadow: 0 6px 20px rgba(59,130,246,0.25);
}
/* Styling Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
}
.stTabs [data-baseweb="tab"] {
    height: 50px;
    background-color: #e2e8f0;
    border-radius: 8px 8px 0px 0px;
    padding: 10px 20px;
    font-weight: 600;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #0f766e, #14b8a6);
    color: white !important;
}
/* Styling Tube & Animasi */
.tube-wrap {
    display: flex;
    justify-content: center;
    height: 350px;
    padding-top: 10px;
}
.tube-glass {
    width: 80px;
    height: 300px;
    border: 4px solid #94a3b8;
    border-top: none;
    border-radius: 0 0 40px 40px;
    position: relative;
    overflow: hidden;
    background: rgba(15, 23, 42, 0.08);
    box-shadow: inset 0 0 15px rgba(0,0,0,0.1);
}
.tube-liquid {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    transition: height 1.2s ease-in-out, background 1.2s ease-in-out;
}
.precipitate-layer {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 60px;
    box-shadow: inset 0 2px 5px rgba(0,0,0,0.2);
}
.cloudy-layer {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    background: linear-gradient(to bottom, rgba(255,255,255,0.85), rgba(241,245,249,0.95));
}
.bubble-fx {
    position: absolute;
    background: rgba(0,0,0,0.15);
    border-radius: 50%;
    width: 8px;
    height: 8px;
    animation: floatUp 1.8s infinite ease-in;
}
@keyframes floatUp {
    0% { bottom: 0px; opacity: 1; }
    100% { bottom: 250px; opacity: 0; }
}
/* Badge Info Pereaksi */
.badge-pereaksi {
    background-color: #e2e8f0;
    padding: 12px;
    border-radius: 8px;
    text-align: center;
    font-weight: 600;
    color: #1e293b;
    margin-bottom: 20px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. FUNGSI HELPER & DATABASE
# ==============================================================================
def force_rerun():
    if hasattr(st, 'rerun'):
        st.rerun()
    elif hasattr(st, 'experimental_rerun'):
        st.experimental_rerun()

def render_tube(tinggi, warna_larutan, efek, warna_endapan=None):
    e_html = ""
    if efek == "precipitate":
        bg_endapan = warna_endapan if warna_endapan else warna_larutan
        e_html = f"<div class='precipitate-layer' style='background: {bg_endapan}; border-top: 3.5px solid rgba(0, 0, 0, 0.25);'></div>"
    elif efek == "cloudy":
        e_html = "<div class='cloudy-layer'></div>"
    elif efek == "bubbles":
        e_html = "<div class='bubble-fx' style='left:20px;'></div><div class='bubble-fx' style='left:50px; animation-delay:0.5s;'></div>"
    return f"<div class='tube-wrap'><div class='tube-glass'><div class='tube-liquid' style='height:{tinggi}; background:{warna_larutan};'>{e_html}</div></div></div>"

# Database Reaksi dan Warna (Dipadatkan untuk efisiensi ruang)
reagen_colors = {
    "Uji Golongan Alkohol": "#f97316", "Uji Oksidasi Alkohol": "#f97316", "Uji Golongan Alkohol Tersier": "#f8fafc", 
    "Uji Golongan Alkohol Sekunder": "#f8fafc", "Uji Golongan Alkanal/Aldehida (Bisulfit)": "#f8fafc", 
    "Uji Reduksi Golongan Alkanal (Fehling)": "#3b82f6", "Uji Spesifik Golongan Alkanal (Schiff)": "#f8fafc",
    "Uji Golongan Metil Keton / Metil Karbinol": "#f8fafc", "Uji Golongan Ester": "#f8fafc", "Uji Golongan Asam Karboksilat": "#f8fafc"
}

flowchart_paths = {
    "Alkohol Primer": ["Uji Golongan Alkohol", "Uji Oksidasi Alkohol", "Uji Golongan Alkohol Sekunder"],
    "Alkohol Sekunder": ["Uji Golongan Alkohol", "Uji Oksidasi Alkohol", "Uji Golongan Alkohol Sekunder", "Uji Golongan Metil Keton / Metil Karbinol"],
    "Alkohol Tersier": ["Uji Golongan Alkohol", "Uji Oksidasi Alkohol", "Uji Golongan Alkohol Tersier"],
    "Aldehida (Alkanal)": ["Uji Golongan Alkohol", "Uji Golongan Alkanal/Aldehida (Bisulfit)", "Uji Reduksi Golongan Alkanal (Fehling)", "Uji Spesifik Golongan Alkanal (Schiff)"],
    "Keton (Alkanon)": ["Uji Golongan Alkohol", "Uji Golongan Alkanal/Aldehida (Bisulfit)", "Uji Reduksi Golongan Alkanal (Fehling)", "Uji Golongan Metil Keton / Metil Karbinol"],
    "Ester (Alkil Alkanoat)": ["Uji Golongan Alkohol", "Uji Golongan Alkanal/Aldehida (Bisulfit)", "Uji Golongan Ester"],
    "Asam Karboksilat": ["Uji Golongan Alkohol", "Uji Golongan Alkanal/Aldehida (Bisulfit)", "Uji Golongan Ester", "Uji Golongan Asam Karboksilat"],
    "Alkana / Hidrokarbon Jenuh": ["Uji Golongan Alkohol", "Uji Golongan Alkanal/Aldehida (Bisulfit)", "Uji Golongan Ester", "Uji Golongan Asam Karboksilat"]
}

database_reaksi = {
    "Alkohol Primer": {
        "Uji Golongan Alkohol": {"hasil": "(+) Merah Ceri", "reaksi": r"R-OH + [Ce(NO_3)_6]^{2-} \rightarrow [Ce(OR)(NO_3)_5]^{2-} + HNO_3", "alasan": "Gugus -OH bebas bereaksi menggantikan ligan nitrat pada ion Cerium(IV) membentuk senyawa kompleks koordinasi berwarna merah ceri.", "warna_akhir": "#ef4444", "efek": "none"},
        "Uji Oksidasi Alkohol": {"hasil": "(+) Hijau", "reaksi": r"3\ R-CH_2OH + 2\ CrO_3 + 3\ H_2SO_4 \rightarrow 3\ R-CHO + Cr_2(SO_4)_3 + 6\ H_2O", "alasan": "Dioksidasi menjadi aldehida, kromium(VI) tereduksi menjadi kromium(III).", "warna_akhir": "#10b981", "efek": "none"},
        "Uji Golongan Alkohol Sekunder": {"hasil": "(-) Tetap Jingga", "reaksi": r"R-CH_2OH + HCl \xrightarrow{ZnCl_2} \text{Tidak ada reaksi}", "alasan": "Karbokation primer sangat tidak stabil.", "warna_akhir": "#f97316", "efek": "none"}
    },
    "Alkohol Sekunder": {
        "Uji Golongan Alkohol": {"hasil": "(+) Merah Ceri", "reaksi": r"R-OH + [Ce(NO_3)_6]^{2-} \rightarrow [Ce(OR)(NO_3)_5]^{2-} + HNO_3", "alasan": "Ikatan koordinasi terbentuk dengan logam Cerium.", "warna_akhir": "#ef4444", "efek": "none"},
        "Uji Oksidasi Alkohol": {"hasil": "(+) Hijau", "reaksi": r"3\ R_2CH-OH + 2\ CrO_3 + 3\ H_2SO_4 \rightarrow 3\ R_2C=O + Cr_2(SO_4)_3 + 6\ H_2O", "alasan": "Dioksidasi menjadi keton.", "warna_akhir": "#10b981", "efek": "none"},
        "Uji Golongan Alkohol Sekunder": {"hasil": "(+) Emulsi Putih", "reaksi": r"R_2CH-OH + HCl \xrightarrow{ZnCl_2} R_2CH-Cl \downarrow + H_2O", "alasan": "Karbokation sekunder menghasilkan alkil klorida (lambat).", "warna_akhir": "#e2e8f0", "efek": "cloudy"},
        "Uji Golongan Metil Keton / Metil Karbinol": {"hasil": "(+) Endapan Kuning", "reaksi": r"R-CH(OH)-CH_3 + 4\ I_2 + 6\ NaOH \rightarrow CHI_3 \downarrow + R-COONa + 5\ NaI + 5\ H_2O", "alasan": "Membentuk endapan iodoform kuning.", "warna_akhir": "#fef08a", "efek": "precipitate", "warna_endapan": "#facc15"}
    },
    "Alkohol Tersier": {
        "Uji Golongan Alkohol": {"hasil": "(+) Merah Ceri", "reaksi": r"R-OH + [Ce(NO_3)_6]^{2-} \rightarrow [Ce(OR)(NO_3)_5]^{2-} + HNO_3", "alasan": "Membentuk kompleks koordinasi berwarna merah.", "warna_akhir": "#ef4444", "efek": "none"},
        "Uji Oksidasi Alkohol": {"hasil": "(-) Tetap Jingga", "reaksi": r"R_3C-OH + CrO_3 \rightarrow \text{Tidak bereaksi}", "alasan": "Tidak memiliki hidrogen alfa.", "warna_akhir": "#f97316", "efek": "none"},
        "Uji Golongan Alkohol Tersier": {"hasil": "(+) Emulsi Putih", "reaksi": r"R_3C-OH + HCl \xrightarrow{ZnCl_2} R_3C-Cl \downarrow + H_2O", "alasan": "Karbokation tersier sangat stabil, bereaksi instan.", "warna_akhir": "#94a3b8", "efek": "cloudy"}
    },
    "Aldehida (Alkanal)": {
        "Uji Golongan Alkohol": {"hasil": "(-) Tetap Jingga", "reaksi": r"R-CHO + [Ce(NO_3)_6]^{2-} \rightarrow \text{Tidak bereaksi}", "alasan": "Tidak memiliki gugus hidroksil bebas.", "warna_akhir": "#f97316", "efek": "none"},
        "Uji Golongan Alkanal/Aldehida (Bisulfit)": {"hasil": "(+) Endapan Putih", "reaksi": r"R-CHO + NaHSO_3 \rightarrow R-CH(OH)SO_3Na \downarrow", "alasan": "Adisi nukleofilik membentuk kristal.", "warna_akhir": "#cbd5e1", "efek": "precipitate", "warna_endapan": "#ffffff"},
        "Uji Reduksi Golongan Alkanal (Fehling)": {"hasil": "(+) Merah Bata", "reaksi": r"R-CHO + 2\ Cu^{2+} + 5\ OH^- \rightarrow R-COO^- + Cu_2O \downarrow + 3\ H_2O", "alasan": "Aldehida mereduksi kupri oksida.", "warna_akhir": "#3b82f6", "efek": "precipitate", "warna_endapan": "#b91c1c"},
        "Uji Spesifik Golongan Alkanal (Schiff)": {"hasil": "(+) Ungu", "reaksi": r"\text{Aldehida} + \text{Pereaksi Schiff} \rightarrow \text{Kompleks Magenta}", "alasan": "Menghasilkan warna ungu kemerahan.", "warna_akhir": "#d946ef", "efek": "none"}
    },
    "Keton (Alkanon)": {
        "Uji Golongan Alkohol": {"hasil": "(-) Tetap Jingga", "reaksi": r"\text{Keton} + [Ce(NO_3)_6]^{2-} \rightarrow \text{Tidak bereaksi}", "alasan": "Tidak memiliki gugus hidroksil.", "warna_akhir": "#f97316", "efek": "none"},
        "Uji Golongan Alkanal/Aldehida (Bisulfit)": {"hasil": "(+) Endapan Putih", "reaksi": r"CH_3-CO-CH_3 + NaHSO_3 \rightarrow (CH_3)_2C(OH)SO_3Na \downarrow", "alasan": "Keton suku rendah diadisi bisulfit.", "warna_akhir": "#cbd5e1", "efek": "precipitate", "warna_endapan": "#ffffff"},
        "Uji Reduksi Golongan Alkanal (Fehling)": {"hasil": "(-) Tetap Biru", "reaksi": r"\text{Keton} + Cu^{2+} \rightarrow \text{Tidak bereaksi}", "alasan": "Keton tidak bersifat reduktor.", "warna_akhir": "#3b82f6", "efek": "none"},
        "Uji Golongan Metil Keton / Metil Karbinol": {"hasil": "(+) Endapan Kuning", "reaksi": r"R-CO-CH_3 + 3\ I_2 + 4\ NaOH \rightarrow CHI_3 \downarrow + R-COONa + 3\ NaI + 3\ H_2O", "alasan": "Membentuk endapan iodoform.", "warna_akhir": "#fef08a", "efek": "precipitate", "warna_endapan": "#facc15"}
    },
    "Ester (Alkil Alkanoat)": {
        "Uji Golongan Alkohol": {"hasil": "(-) Tetap Jingga", "reaksi": r"\text{Ester} + [Ce(NO_3)_6]^{2-} \rightarrow \text{Tidak bereaksi}", "alasan": "Tidak memiliki gugus OH bebas.", "warna_akhir": "#f97316", "efek": "none"},
        "Uji Golongan Alkanal/Aldehida (Bisulfit)": {"hasil": "(-) Bening", "reaksi": r"\text{Ester} + NaHSO_3 \rightarrow \text{Tidak bereaksi}", "alasan": "Gugus ester stabil akibat resonansi.", "warna_akhir": "#f8fafc", "efek": "none"},
        "Uji Golongan Ester": {"hasil": "(+) Merah Violet", "reaksi": r"3\ R-CONHOH + FeCl_3 \rightarrow Fe(R-CONHO)_3 + 3\ HCl", "alasan": "Membentuk kompleks violet.", "warna_akhir": "#c026d3", "efek": "none"}
    },
    "Asam Karboksilat": {
        "Uji Golongan Alkohol": {"hasil": "(-) Tetap Jingga", "reaksi": r"R-COOH + [Ce(NO_3)_6]^{2-} \rightarrow \text{Tidak bereaksi}", "alasan": "Sifat nukleofil ditarik resonansi.", "warna_akhir": "#f97316", "efek": "none"},
        "Uji Golongan Alkanal/Aldehida (Bisulfit)": {"hasil": "(-) Bening", "reaksi": r"R-COOH + NaHSO_3 \rightarrow \text{Tidak bereaksi}", "alasan": "Tidak mengandung gugus karbonil aldehida/keton.", "warna_akhir": "#f8fafc", "efek": "none"},
        "Uji Golongan Ester": {"hasil": "(-) Bening", "reaksi": r"R-COOH + NH_2OH + FeCl_3 \rightarrow \text{Tidak bereaksi}", "alasan": "Bukan derivat ester.", "warna_akhir": "#f8fafc", "efek": "none"},
        "Uji Golongan Asam Karboksilat": {"hasil": "(+) Gelembung & Keruh", "reaksi": r"CO_2 + Ba(OH)_2 \rightarrow BaCO_3 \downarrow + H_2O", "alasan": "CO2 yang dihasilkan mengeruhkan air barit.", "warna_akhir": "#f8fafc", "efek": "bubbles"}
    },
    "Alkana / Hidrokarbon Jenuh": {
        "Uji Golongan Alkohol": {"hasil": "(-) Tetap Jingga", "reaksi": r"\text{Alkana} + [Ce(NO_3)_6]^{2-} \rightarrow \text{Tidak bereaksi}", "alasan": "Senyawa inert.", "warna_akhir": "#f97316", "efek": "none"},
        "Uji Golongan Alkanal/Aldehida (Bisulfit)": {"hasil": "(-) Bening", "reaksi": r"\text{Alkana} + NaHSO_3 \rightarrow \text{Tidak bereaksi}", "alasan": "Inert.", "warna_akhir": "#f8fafc", "efek": "none"},
        "Uji Golongan Ester": {"hasil": "(-) Bening", "reaksi": r"\text{Alkana} + NH_2OH \rightarrow \text{Tidak bereaksi}", "alasan": "Inert.", "warna_akhir": "#f8fafc", "efek": "none"},
        "Uji Golongan Asam Karboksilat": {"hasil": "(-) Bening", "reaksi": r"\text{Alkana} + NaNaHCO_3 \rightarrow \text{Tidak bereaksi}", "alasan": "Senyawa sangat stabil dan nonpolar.", "warna_akhir": "#f8fafc", "efek": "none"}
    }
}

if "test_started" not in st.session_state:
    st.session_state.test_started = False
if "current_step" not in st.session_state:
    st.session_state.current_step = 0
if "log_history" not in st.session_state:
    st.session_state.log_history = []
if "trigger_animation" not in st.session_state:
    st.session_state.trigger_animation = False

# ==============================================================================
# 3. SIDEBAR NAVIGASI
# ==============================================================================
with st.sidebar:
    st.title("🧪 OrganicChem")
    st.write("*Virtual Lab Simulator*")
    st.markdown("---")
    pilihan_halaman = st.sidebar.radio("Navigasi:", ["🏠 HALAMAN UTAMA", "📘 BAB I", "📙 BAB II", "📗 BAB III", "📕 BAB IV", "🔬 POST TEST"])
    st.markdown("---")

# ==============================================================================
# 4. LOGIKA KONTEN TIAP HALAMAN
# ==============================================================================

if pilihan_halaman == "🏠 HALAMAN UTAMA":
    st.markdown("<div class='banner-utama'><h2>Selamat Datang di Lab Virtual!</h2><p>Pilih menu navigasi di samping untuk mulai.</p></div>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# BAB I - IV (Dengan Perbaikan Fitur 2D Anti-Error)
# ------------------------------------------------------------------------------
elif pilihan_halaman in ["📘 BAB I", "📙 BAB II", "📗 BAB III", "📕 BAB IV"]:
    st.title(pilihan_halaman)
    tab_teori, tab_reaksi, tab_visual = st.tabs(["📖 Referensi Standar & Sifat", "📊 Analisis Parameter Reaksi", "📈 Visualisasi 2D"])
    
    with tab_teori:
        st.write("Silakan baca modul untuk memahami dasar-dasar sifat fisik dan kimia golongan ini.")
    
    with tab_reaksi:
        st.write("Daftar persamaan stoikiometri dan reaksi kimia.")
        
    with tab_visual:
        st.subheader("Ilustrasi 2D Mekanisme Reaksi")
        st.info("💡 **Petunjuk Pengembang:** Ganti baris kode `st.info(...)` ini dengan `st.image('nama_file_lokal.png')` yang di-render dari ChemDraw agar aman dan tidak diblokir internet.")
        
        col1, col2, col3 = st.columns([2, 1, 2])
        with col1:
            # Contoh penggunaan placeholder aman (Bebas error URL)
            st.markdown("""
            <div style="border: 2px dashed #94a3b8; padding: 30px; text-align: center; border-radius: 10px; background: white;">
                🖼️ <b>[Gambar Pereaksi.png]</b><br>
                <span style="font-size:12px; color:gray;">(Masukkan file lokal)</span>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("<h1 style='text-align: center; color: #14b8a6; margin-top: 20px;'>➔</h1>", unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div style="border: 2px dashed #94a3b8; padding: 30px; text-align: center; border-radius: 10px; background: white;">
                🖼️ <b>[Gambar Produk.png]</b><br>
                <span style="font-size:12px; color:gray;">(Masukkan file lokal)</span>
            </div>
            """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# POST TEST (Desain Baru Sesuai Tangkapan Layar)
# ------------------------------------------------------------------------------
elif pilihan_halaman == "🔬 POST TEST":
    if not st.session_state.test_started:
        st.title("🔬 Mulai Analisis Sampel")
        senyawa = st.selectbox("Pilih Sampel:", ["-- Pilih --"] + list(flowchart_paths.keys()))
        if st.button("Mulai Identifikasi 🚀"):
            if senyawa != "-- Pilih --":
                st.session_state.test_started = True
                st.session_state.senyawa_uji = senyawa
                st.session_state.current_step = 0
                st.session_state.log_history = []
                st.session_state.trigger_animation = True
                force_rerun()
    else:
        senyawa = st.session_state.senyawa_uji
        urutan = flowchart_paths[senyawa]

        col_visual, col_space, col_log = st.columns([1.2, 0.2, 2.5])
        
        with col_visual:
            st.markdown("<h3 style='text-align: center; color: #1e293b; font-weight: 600;'>Visual Lab</h3>", unsafe_allow_html=True)
            
            # Placeholder untuk Badge Pereaksi yang rapi
            badge_placeholder = st.empty()
            
            # Tabung Reaksi
            tube_placeholder = st.empty() 
            status_placeholder = st.empty()
            
            st.write("")
            if st.button("⏹️ Reset Uji", use_container_width=True):
                st.session_state.test_started = False
                force_rerun()
            
        with col_log:
            st.markdown("<h3 style='color: #1e293b; font-weight: 600;'>📑 Logbook & Analisis Teoritis</h3>", unsafe_allow_html=True)
            log_container = st.container()

        # Render Riwayat Logbook
        with log_container:
            for log in st.session_state.log_history:
                # Membuat layout Logbook yang persis seperti screenshot
                if "(+)" in log["hasil"]:
                    st.success(f"Tahap {log['step']}: {log['pereaksi']} ➔ {log['hasil']}")
                else:
                    st.error(f"Tahap {log['step']}: {log['pereaksi']} ➔ {log['hasil']}")
                
                # Persamaan rata tengah
                st.latex(log['reaksi'])
                
                # Pembahasan
                st.markdown(f"**Pembahasan:** {log['alasan']}")
                st.markdown("<br>", unsafe_allow_html=True)

        # Logika Animasi & Transisi Tahapan
        if st.session_state.trigger_animation and st.session_state.current_step < len(urutan):
            pereaksi = urutan[st.session_state.current_step]
            
            # Tampilkan Badge Nama Pereaksi
            badge_placeholder.markdown(f"<div class='badge-pereaksi'>🧪 Pereaksi: {pereaksi}</div>", unsafe_allow_html=True)
            
            tube_placeholder.markdown(
