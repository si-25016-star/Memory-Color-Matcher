
import random
import time
import streamlit as st
import streamlit.components.v1 as components

# ============================================================
# 1. PENGATURAN GAME
# ============================================================

DAFTAR_WARNA = ["Merah", "Hijau", "Kuning", "Biru"]

HEX_WARNA = {
    "Merah": "#FF4D4D",
    "Hijau": "#2ECC71",
    "Kuning": "#F1C40F",
    "Biru": "#3498DB"
}

EMOJI_WARNA = {
    "Merah": "🔴",
    "Hijau": "🟢",
    "Kuning": "🟡",
    "Biru": "🔵"
}

PANJANG_POLA = 4
POIN_BENAR = 10
DURASI_NORMAL = 5
DURASI_CEPAT = 3
BATAS_SKOR_CEPAT = 50


# ============================================================
# 2. TAMPILAN DAN SUARA
# ============================================================

st.set_page_config(
    page_title="Memory Color Matcher",
    page_icon="🎮",
    layout="centered"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #E3F2FD, #F3E5F5);
}
h1, h2, h3, p, label {
    color: #263238;
}
div.stButton > button {
    width: 100%;
    min-height: 48px;
    border-radius: 12px;
    font-weight: bold;
}
.game-card {
    background: white;
    padding: 22px;
    border-radius: 16px;
    text-align: center;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)



def suara_game(jenis="klik"):
    """Memainkan efek suara di browser."""

    daftar_nada = {
        "klik": [(500, 0.12)],
        "mulai": [(600, 0.15), (800, 0.20)],
        "benar": [(600, 0.16), (800, 0.16), (1100, 0.35)],
        "salah": [(300, 0.25), (180, 0.40)],
        "ronde": [(700, 0.12), (900, 0.12), (1200, 0.25)]
    }

    nada = daftar_nada.get(jenis, daftar_nada["klik"])
    daftar_js = ",".join(
        f"{{freq:{frekuensi}, dur:{durasi}}}"
        for frekuensi, durasi in nada
    )

    components.html(
        f"""
        <button id="play" style="display:none">Play</button>
        <script>
        (async () => {{
            try {{
                const ctx = new (
                    window.AudioContext ||
                    window.webkitAudioContext
                )();

                if (ctx.state === "suspended") {{
                    await ctx.resume();
                }}

                const notes = [{daftar_js}];
                let waktu = ctx.currentTime;

                notes.forEach(n => {{
                    const oscillator = ctx.createOscillator();
                    const gain = ctx.createGain();

                    oscillator.type = "sine";
                    oscillator.frequency.setValueAtTime(
                        n.freq, waktu
                    );

                    gain.gain.setValueAtTime(0.001, waktu);
                    gain.gain.linearRampToValueAtTime(
                        0.15, waktu + 0.02
                    );
                    gain.gain.exponentialRampToValueAtTime(
                        0.001, waktu + n.dur
                    );

                    oscillator.connect(gain);
                    gain.connect(ctx.destination);

                    oscillator.start(waktu);
                    oscillator.stop(waktu + n.dur);

                    waktu += n.dur;
                }});

                setTimeout(() => ctx.close(), 2000);
            }} catch (e) {{
                console.log("Audio tidak tersedia:", e);
            }}
        }})();
        </script>
        """,
        height=0
    )

# ============================================================
# 3. FUNGSI GAME
# ============================================================

def buat_pola():
    return [
        random.choice(DAFTAR_WARNA)
        for _ in range(PANJANG_POLA)
    ]


def siapkan_ronde():
    st.session_state.pola_target = buat_pola()
    st.session_state.input_pemain = []
    st.session_state.fase = "tampil_pola"


def mulai_game():
    st.session_state.skor = 0
    st.session_state.ronde = 1
    st.session_state.sudah_mulai = True
    siapkan_ronde()
    suara_game("mulai")


def ulangi_game():
    st.session_state.skor = 0
    st.session_state.ronde = 1
    st.session_state.sudah_mulai = False
    st.session_state.fase = "awal"
    st.session_state.input_pemain = []
    st.session_state.pola_target = []


# ============================================================
# 4. INISIALISASI SESSION
# ============================================================

nilai_awal = {
    "skor": 0,
    "best_skor": 0,
    "ronde": 1,
    "pola_target": [],
    "input_pemain": [],
    "fase": "awal",
    "sudah_mulai": False
}

for nama, nilai in nilai_awal.items():
    if nama not in st.session_state:
        st.session_state[nama] = nilai


# ============================================================
# 5. HEADER DAN INFORMASI SKOR
# ============================================================

st.markdown(
    "<h1 style='text-align:center;color:#5E35B1;'>"
    "🎮 MEMORY COLOR MATCHER</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center;'>"
    "Ingat urutan 4 warna yang muncul!</p>",
    unsafe_allow_html=True
)

kolom1, kolom2, kolom3 = st.columns(3)

with kolom1:
    st.metric("🎯 RONDE", st.session_state.ronde)

with kolom2:
    st.metric("⭐ SKOR", st.session_state.skor)

with kolom3:
    st.metric("🏆 BEST SCORE", st.session_state.best_skor)

durasi = (
    DURASI_CEPAT
    if st.session_state.skor >= BATAS_SKOR_CEPAT
    else DURASI_NORMAL
)


# ============================================================
# 6. HALAMAN AWAL
# ============================================================

if st.session_state.fase == "awal":
    st.markdown("""
    <div class="game-card">
        <h2>🧠 Siap Menguji Ingatan?</h2>
        <p>Perhatikan urutan warna, lalu tekan warna sesuai urutan.</p>
        <p>Jawaban benar mendapatkan 10 poin.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🎮 Mulai Game", type="primary"):
        mulai_game()
        st.rerun()


# ============================================================
# 7. MENAMPILKAN POLA WARNA
# ============================================================

elif st.session_state.fase == "tampil_pola":
    pola_str = "　".join(
        EMOJI_WARNA[w]
        for w in st.session_state.pola_target
    )

    if durasi == DURASI_CEPAT:
        st.warning("⚡ MODE CEPAT: Ingat pola dalam 3 detik!")
    else:
        st.info(f"🧠 INGAT POLA! Kamu punya {durasi} detik.")

    st.markdown(
        f"<div class='game-card'>"
        f"<h2>{pola_str}</h2>"
        f"<p>Perhatikan urutannya!</p>"
        f"</div>",
        unsafe_allow_html=True
    )

    st.progress(1.0, text=f"Waktu mengingat: {durasi} detik")

    # Beri kesempatan tampilan pola dikirim ke browser.
    time.sleep(durasi)

    st.session_state.fase = "pilihan"
    st.rerun()


# ============================================================
# 8. MEMILIH WARNA
# ============================================================

elif st.session_state.fase == "pilihan":
    st.warning("🙈 Pola disembunyikan! Pilih warna sesuai urutan.")
    st.markdown("### ❓ ❓ ❓ ❓")

    if st.session_state.input_pemain:
        jawaban_sementara = " → ".join(
            EMOJI_WARNA[w]
            for w in st.session_state.input_pemain
        )
        st.write("Pilihan kamu:", jawaban_sementara)

    st.write("Tekan warna satu per satu:")

    kolom_warna = st.columns(2)

    for i, warna in enumerate(DAFTAR_WARNA):
        with kolom_warna[i % 2]:
            if st.button(
                f"{EMOJI_WARNA[warna]} {warna}",
                key=f"warna_{warna}",
                use_container_width=True
            ):
                suara_game("klik")

                posisi = len(st.session_state.input_pemain)
                warna_benar = st.session_state.pola_target[posisi]

                if warna != warna_benar:
                    st.session_state.input_pemain.append(warna)
                    st.session_state.fase = "game_over"
                    suara_game("salah")
                else:
                    st.session_state.input_pemain.append(warna)

                    if len(st.session_state.input_pemain) == PANJANG_POLA:
                        st.session_state.skor += POIN_BENAR
                        st.session_state.best_skor = max(
                            st.session_state.best_skor,
                            st.session_state.skor
                        )
                        st.session_state.fase = "hasil_benar"
                        suara_game("benar")

                st.rerun()


# ============================================================
# 9. HASIL JAWABAN BENAR DAN LANJUT RONDE
# ============================================================

elif st.session_state.fase == "hasil_benar":
    st.success(f"🎉 BENAR! +{POIN_BENAR} poin")

    jawaban = " → ".join(
        f"{EMOJI_WARNA[w]} {w}"
        for w in st.session_state.pola_target
    )

    st.markdown(
        f"<div class='game-card'>"
        f"<h2 style='color:#2ECC71;'>🎉 JAWABAN BENAR!</h2>"
        f"<p>Jawaban: {jawaban}</p>"
        f"<h3>Skor kamu: {st.session_state.skor}</h3>"
        f"</div>",
        unsafe_allow_html=True
    )

    st.info("Ronde berikutnya akan dimulai otomatis...")

    time.sleep(1.5)

    st.session_state.ronde += 1
    suara_game("ronde")
    siapkan_ronde()
    st.rerun()


# ============================================================
# 10. GAME OVER
# ============================================================

elif st.session_state.fase == "game_over":
    st.error("💀 GAME OVER! Jawaban kamu salah.")

    jawaban = " → ".join(
        f"{EMOJI_WARNA[w]} {w}"
        for w in st.session_state.pola_target
    )

    st.markdown(
        f"<div class='game-card'>"
        f"<h2 style='color:#FF4D4D;'>💀 GAME OVER!</h2>"
        f"<p>Jawaban yang benar:</p>"
        f"<h3>{jawaban}</h3>"
        f"<h3>Skor akhir: {st.session_state.skor}</h3>"
        f"<p>🏆 Best score: {st.session_state.best_skor}</p>"
        f"<p>Terus berlatih!</p>"
        f"</div>",
        unsafe_allow_html=True
    )

    if st.button("🔄 Main Lagi", type="primary"):
        ulangi_game()
        st.rerun()
