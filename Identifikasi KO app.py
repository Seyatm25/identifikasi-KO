# ------------------------------------------------------------------------------
# POST TEST (Desain Baru & Fix Syntax Error)
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
                # Membuat layout Logbook
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
            badge_placeholder.markdown(
                f"<div class='badge-pereaksi'>🧪 Pereaksi: {pereaksi}</div>", 
                unsafe_allow_html=True
            )
            
            tube_placeholder.markdown(
                render_tube("30%", "#f1f5f9", "none"), 
                unsafe_allow_html=True
            )
            time.sleep(0.8)
            
            warna_reagen = reagen_colors[pereaksi]
            tube_placeholder.markdown(
                render_tube("65%", warna_reagen, "none"), 
                unsafe_allow_html=True
            )
            time.sleep(1.2)
            
            res = database_reaksi[senyawa][pereaksi]
            w_endapan = res.get("warna_endapan", None)
            
            tube_placeholder.markdown(
                render_tube("65%", res["warna_akhir"], res["efek"], warna_endapan=w_endapan), 
                unsafe_allow_html=True
            )
            time.sleep(1.0)
            
            st.session_state.log_history.append({
                "step": st.session_state.current_step + 1,
                "pereaksi": pereaksi,
                "hasil": res["hasil"],
                "reaksi": res["reaksi"],
                "alasan": res["alasan"]
            })
            
            st.session_state.current_step += 1
            st.session_state.trigger_animation = False
            force_rerun()

        elif not st.session_state.trigger_animation:
            if st.session_state.current_step > 0:
                last_pereaksi = urutan[st.session_state.current_step - 1]
                res = database_reaksi[senyawa][last_pereaksi]
                
                badge_placeholder.markdown(
                    f"<div class='badge-pereaksi'>🧪 Pereaksi: {last_pereaksi}</div>", 
                    unsafe_allow_html=True
                )
                
                tube_placeholder.markdown(
                    render_tube("65%", res["warna_akhir"], res["efek"], res.get("warna_endapan", None)), 
                    unsafe_allow_html=True
                )
