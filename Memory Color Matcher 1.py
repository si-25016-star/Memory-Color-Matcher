
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Memory Color Matcher",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

html_game = r"""
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    padding: 12px;
    font-family: Arial, sans-serif;
    background: #DCEEFF;
    color: #263238;
}

.game-container {
    max-width: 720px;
    margin: 0 auto;
}

.game-header {
    background: #BBDDFB;
    padding: 20px;
    border-radius: 18px;
    text-align: center;
}

.game-title {
    margin: 0 0 20px;
    color: #673AB7;
    font-size: 27px;
}

.score-container {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
}

.score-card {
    background: white;
    padding: 14px 5px;
    border-radius: 12px;
    min-height: 78px;
}

.score-label {
    font-size: 13px;
}

.score-number {
    margin-top: 8px;
    font-size: 24px;
    font-weight: bold;
    color: #00A152;
}

.round-number {
    color: #673AB7;
}

.best-number {
    color: #F4B400;
}

.pattern-card {
    background: white;
    padding: 22px 10px;
    margin-top: 16px;
    border-radius: 14px;
    text-align: center;
}

.pattern-title {
    font-size: 17px;
    font-weight: bold;
    color: #673AB7;
    margin-bottom: 18px;
}

.pattern-display {
    font-size: 34px;
    letter-spacing: 5px;
    min-height: 45px;
    overflow-wrap: anywhere;
}

.instruction {
    margin: 18px 0 10px;
    text-align: center;
    font-weight: bold;
    line-height: 1.5;
}

.status {
    min-height: 25px;
    text-align: center;
    font-size: 14px;
    font-weight: bold;
    margin: 10px 0;
}

.timer-container {
    width: 100%;
    height: 8px;
    background: #E0E0E0;
    border-radius: 10px;
    overflow: hidden;
    margin-top: 15px;
}

.timer-bar {
    width: 100%;
    height: 100%;
    background: #673AB7;
}

.color-container {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 12px;
    margin-top: 15px;
}

.color-tile {
    width: 100%;
    height: 78px;
    border: 3px solid rgba(255,255,255,0.8);
    border-radius: 13px;
    font-size: 17px;
    font-weight: bold;
    color: #17202A;
    cursor: pointer;
    box-shadow: 0 3px 7px rgba(0,0,0,0.12);
    transition: transform 0.12s, filter 0.12s;
}

.color-tile:hover:not(:disabled) {
    filter: brightness(0.93);
    transform: translateY(-2px);
}

.color-tile:active:not(:disabled) {
    transform: scale(0.96);
}

.color-tile:disabled {
    cursor: not-allowed;
    opacity: 0.65;
}

.red {
    background: #FF4D4D;
}

.green {
    background: #2ECC71;
}

.yellow {
    background: #F1C40F;
}

.blue {
    background: #3498DB;
}

.main-button {
    display: block;
    width: 100%;
    margin: 18px auto 0;
    padding: 15px 20px;
    background: #673AB7;
    color: white;
    font-size: 16px;
    font-weight: bold;
    border: none;
    border-radius: 11px;
    cursor: pointer;
}

.main-button:hover {
    background: #512DA8;
}

.main-button:disabled {
    opacity: 0.65;
    cursor: not-allowed;
}

.hidden {
    display: none !important;
}

.result-card {
    background: white;
    border-radius: 14px;
    padding: 20px;
    margin-top: 16px;
    text-align: center;
    line-height: 1.8;
}

.result-title {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 10px;
}

@media (max-width: 450px) {
    body {
        padding: 5px;
    }

    .game-title {
        font-size: 21px;
    }

    .game-header {
        padding: 14px 10px;
    }

    .score-container {
        gap: 5px;
    }

    .score-label {
        font-size: 10px;
    }

    .score-number {
        font-size: 20px;
    }

    .color-tile {
        height: 68px;
        font-size: 14px;
    }

    .pattern-display {
        font-size: 29px;
        letter-spacing: 2px;
    }
}
</style>
</head>

<body>

<div class="game-container">

    <div class="game-header">

        <h1 class="game-title">🎮 MEMORY COLOR MATCHER</h1>

        <div class="score-container">

            <div class="score-card">
                <div class="score-label">🎯 RONDE</div>
                <div class="score-number round-number" id="round">1</div>
            </div>

            <div class="score-card">
                <div class="score-label">⭐ SKOR</div>
                <div class="score-number" id="score">0</div>
            </div>

            <div class="score-card">
                <div class="score-label">🏆 BEST SCORE</div>
                <div class="score-number best-number" id="best">0</div>
            </div>

        </div>

        <div class="pattern-card">

            <div class="pattern-title" id="patternTitle">
                🧠 INGAT URUTAN WARNA!
            </div>

            <div class="pattern-display" id="patternDisplay">
                🔴 🟢 🟡 🔵
            </div>

            <div class="timer-container hidden" id="timerContainer">
                <div class="timer-bar" id="timerBar"></div>
            </div>

        </div>
    </div>

    <div class="instruction" id="instruction">
        Tekan tombol Mulai Game untuk bermain!
    </div>

    <div class="status" id="status">
        Siap menguji ingatanmu?
    </div>

    <div class="color-container">

        <button type="button" class="color-tile red"
                onclick="pilihWarna('Merah')" disabled>
            🔴 Merah
        </button>

        <button type="button" class="color-tile green"
                onclick="pilihWarna('Hijau')" disabled>
            🟢 Hijau
        </button>

        <button type="button" class="color-tile yellow"
                onclick="pilihWarna('Kuning')" disabled>
            🟡 Kuning
        </button>

        <button type="button" class="color-tile blue"
                onclick="pilihWarna('Biru')" disabled>
            🔵 Biru
        </button>

    </div>

    <button type="button" class="main-button"
            id="startButton" onclick="mulaiGame()">
        🎮 Mulai Game
    </button>

    <div class="result-card hidden" id="resultCard">

        <div class="result-title" id="resultTitle"></div>

        <div id="resultText"></div>

        <button type="button" class="main-button"
                onclick="mulaiGame()">
            🔄 Main Lagi
        </button>

    </div>

</div>

<script>
"use strict";

// ============================================================
// 1. PENGATURAN GAME
// ============================================================

const WARNA = ["Merah", "Hijau", "Kuning", "Biru"];

const EMOJI = {
    Merah: "🔴",
    Hijau: "🟢",
    Kuning: "🟡",
    Biru: "🔵"
};

const PANJANG_POLA = 4;
const POIN_BENAR = 10;
const DURASI_NORMAL = 5000;
const DURASI_CEPAT = 3000;
const BATAS_SKOR_CEPAT = 50;

// ============================================================
// 2. VARIABEL GAME
// ============================================================

let skor = 0;
let ronde = 1;
let bestScore = 0;

let polaTarget = [];
let posisiPemain = 0;

let gameAktif = false;
let sedangMenampilkanPola = false;

let timerInterval = null;
let timeoutPola = null;
let timeoutRonde = null;

let audioContext = null;

// ============================================================
// 3. MEMBACA BEST SCORE
// ============================================================

try {
    bestScore = Number(
        localStorage.getItem("memoryColorMatcherBest") || 0
    );
} catch (error) {
    bestScore = 0;
}

// ============================================================
// 4. SISTEM SUARA
// ============================================================

function siapkanAudio() {
    try {
        if (!audioContext) {
            const AudioClass =
                window.AudioContext ||
                window.webkitAudioContext;

            if (!AudioClass) {
                return;
            }

            audioContext = new AudioClass();
        }

        if (audioContext.state === "suspended") {
            audioContext.resume();
        }
    } catch (error) {
        console.log("Audio tidak tersedia:", error);
    }
}

function bunyikanNada(frekuensi, durasi, bentuk = "sine") {
    try {
        if (!audioContext || audioContext.state !== "running") {
            return;
        }

        const oscillator = audioContext.createOscillator();
        const gain = audioContext.createGain();
        const sekarang = audioContext.currentTime;

        oscillator.type = bentuk;
        oscillator.frequency.setValueAtTime(
            frekuensi, sekarang
        );

        gain.gain.setValueAtTime(0.001, sekarang);
        gain.gain.linearRampToValueAtTime(
            0.12, sekarang + 0.02
        );
        gain.gain.exponentialRampToValueAtTime(
            0.001, sekarang + durasi
        );

        oscillator.connect(gain);
        gain.connect(audioContext.destination);

        oscillator.start(sekarang);
        oscillator.stop(sekarang + durasi);
    } catch (error) {
        console.log("Suara gagal dimainkan:", error);
    }
}

function suaraKlik(warna) {
    const nada = {
        Merah: 440,
        Hijau: 554,
        Kuning: 659,
        Biru: 784
    };

    bunyikanNada(nada[warna], 0.15);
}

function suaraMulai() {
    bunyikanNada(600, 0.15);

    setTimeout(function () {
        bunyikanNada(800, 0.20);
    }, 160);
}

function suaraBenar() {
    bunyikanNada(600, 0.15);

    setTimeout(function () {
        bunyikanNada(800, 0.15);
    }, 150);

    setTimeout(function () {
        bunyikanNada(1000, 0.25);
    }, 300);
}

function suaraSalah() {
    bunyikanNada(300, 0.25, "triangle");

    setTimeout(function () {
        bunyikanNada(180, 0.30, "triangle");
    }, 220);
}

function suaraRonde() {
    bunyikanNada(700, 0.12);

    setTimeout(function () {
        bunyikanNada(900, 0.12);
    }, 140);

    setTimeout(function () {
        bunyikanNada(1100, 0.20);
    }, 280);
}

// ============================================================
// 5. FUNGSI TAMPILAN
// ============================================================

function perbaruiSkor() {
    document.getElementById("round").textContent = ronde;
    document.getElementById("score").textContent = skor;
    document.getElementById("best").textContent = bestScore;
}

function aturTombolWarna(aktif) {
    document.querySelectorAll(".color-tile").forEach(
        function (tombol) {
            tombol.disabled = !aktif;
        }
    );
}

function tampilkanStatus(pesan, warna = "#263238") {
    const elemen = document.getElementById("status");
    elemen.textContent = pesan;
    elemen.style.color = warna;
}

function buatPola() {
    const hasil = [];

    for (let i = 0; i < PANJANG_POLA; i++) {
        const indeks = Math.floor(
            Math.random() * WARNA.length
        );

        hasil.push(WARNA[indeks]);
    }

    return hasil;
}

function durasiMengingat() {
    return skor >= BATAS_SKOR_CEPAT
        ? DURASI_CEPAT
        : DURASI_NORMAL;
}

function bersihkanTimer() {
    if (timerInterval !== null) {
        clearInterval(timerInterval);
        timerInterval = null;
    }

    if (timeoutPola !== null) {
        clearTimeout(timeoutPola);
        timeoutPola = null;
    }

    if (timeoutRonde !== null) {
        clearTimeout(timeoutRonde);
        timeoutRonde = null;
    }
}

// ============================================================
// 6. MEMULAI GAME
// ============================================================

function mulaiGame() {
    bersihkanTimer();
    siapkanAudio();

    skor = 0;
    ronde = 1;
    posisiPemain = 0;

    gameAktif = true;
    sedangMenampilkanPola = false;

    perbaruiSkor();

    document.getElementById("startButton").classList.add("hidden");
    document.getElementById("resultCard").classList.add("hidden");

    suaraMulai();
    mulaiRonde();
}

// ============================================================
// 7. MEMULAI RONDE
// ============================================================

function mulaiRonde() {
    bersihkanTimer();

    if (!gameAktif) {
        return;
    }

    polaTarget = buatPola();
    posisiPemain = 0;
    sedangMenampilkanPola = true;

    aturTombolWarna(false);

    const durasi = durasiMengingat();

    document.getElementById("patternTitle").textContent =
        durasi === DURASI_CEPAT
        ? "⚡ MODE CEPAT: INGAT POLA!"
        : "🧠 INGAT URUTAN WARNA!";

    document.getElementById("patternDisplay").textContent =
        polaTarget.map(function (warna) {
            return EMOJI[warna];
        }).join(" ");

    document.getElementById("instruction").textContent =
        "Perhatikan urutan warna dengan baik!";

    tampilkanStatus(
        "Ingat 4 warna selama " + (durasi / 1000) + " detik."
    );

    document.getElementById("timerContainer").classList.remove("hidden");

    const timerBar = document.getElementById("timerBar");

    timerBar.style.transition = "none";
    timerBar.style.width = "100%";

    // Memulai animasi timer setelah browser memperbarui tampilan.
    requestAnimationFrame(function () {
        requestAnimationFrame(function () {
            timerBar.style.transition =
                "width " + (durasi / 1000) + "s linear";

            timerBar.style.width = "0%";
        });
    });

    const waktuMulai = Date.now();

    timerInterval = setInterval(function () {
        const sisa = Math.max(
            0, durasi - (Date.now() - waktuMulai)
        );

        if (sisa <= 0 && timerInterval !== null) {
            clearInterval(timerInterval);
            timerInterval = null;
        }
    }, 100);

    timeoutPola = setTimeout(function () {
        timeoutPola = null;

        if (gameAktif) {
            tampilkanPilihan();
        }
    }, durasi);
}

// ============================================================
// 8. MENYEMBUNYIKAN POLA
// ============================================================

function tampilkanPilihan() {
    if (!gameAktif) {
        return;
    }

    if (timerInterval !== null) {
        clearInterval(timerInterval);
        timerInterval = null;
    }

    sedangMenampilkanPola = false;

    document.getElementById("patternTitle").textContent =
        "🙈 POLA SUDAH DISEMBUNYIKAN!";

    document.getElementById("patternDisplay").textContent =
        "❓  ❓  ❓  ❓";

    document.getElementById("timerContainer").classList.add("hidden");

    document.getElementById("instruction").textContent =
        "Pilih warna satu per satu sesuai urutan.";

    tampilkanStatus("Ayo, ingat urutan warnanya!");

    aturTombolWarna(true);
}

// ============================================================
// 9. MEMILIH WARNA
// ============================================================

function pilihWarna(warna) {
    if (!gameAktif || sedangMenampilkanPola) {
        return;
    }

    if (posisiPemain >= PANJANG_POLA) {
        return;
    }

    siapkanAudio();
    suaraKlik(warna);

    const warnaBenar = polaTarget[posisiPemain];

    if (warna !== warnaBenar) {
        gameOver();
        return;
    }

    posisiPemain++;

    const jawabanPemain = polaTarget
        .slice(0, posisiPemain)
        .map(function (w) {
            return EMOJI[w];
        })
        .join(" ");

    const sisa = PANJANG_POLA - posisiPemain;

    const tandaTanya = Array(sisa).fill("❓").join(" ");

    document.getElementById("patternDisplay").textContent =
        jawabanPemain + (sisa > 0 ? " " + tandaTanya : "");

    tampilkanStatus(
        "Benar! " + posisiPemain + " dari " +
        PANJANG_POLA + " warna.",
        "#00A152"
    );

    if (posisiPemain === PANJANG_POLA) {
        rondeBerhasil();
    }
}

// ============================================================
// 10. JAWABAN BENAR
// ============================================================

function rondeBerhasil() {
    gameAktif = false;
    sedangMenampilkanPola = false;

    aturTombolWarna(false);

    skor += POIN_BENAR;

    if (skor > bestScore) {
        bestScore = skor;

        try {
            localStorage.setItem(
                "memoryColorMatcherBest",
                String(bestScore)
            );
        } catch (error) {
            console.log("Best score tidak dapat disimpan.");
        }
    }

    perbaruiSkor();
    suaraBenar();

    document.getElementById("patternTitle").textContent =
        "🎉 HEBAT! SEMUA WARNA BENAR!";

    document.getElementById("patternDisplay").textContent =
        polaTarget.map(function (w) {
            return EMOJI[w];
        }).join(" ");

    document.getElementById("instruction").textContent =
        "Kamu berhasil menyelesaikan ronde " + ronde + "!";

    tampilkanStatus(
        "Jawaban benar! +" + POIN_BENAR + " poin.",
        "#00A152"
    );

    timeoutRonde = setTimeout(function () {
        timeoutRonde = null;

        ronde++;
        perbaruiSkor();

        suaraRonde();

        gameAktif = true;
        mulaiRonde();
    }, 1600);
}

// ============================================================
// 11. GAME OVER
// ============================================================

function gameOver() {
    gameAktif = false;
    sedangMenampilkanPola = false;

    bersihkanTimer();
    aturTombolWarna(false);
    suaraSalah();

    document.getElementById("timerContainer").classList.add("hidden");

    document.getElementById("patternTitle").textContent =
        "💀 GAME OVER!";

    document.getElementById("patternDisplay").textContent =
        polaTarget.map(function (w) {
            return EMOJI[w];
        }).join(" ");

    document.getElementById("instruction").textContent =
        "Urutan warna yang benar ditampilkan di atas.";

    tampilkanStatus(
        "Jawaban salah! Coba lagi, ya.",
        "#FF3333"
    );

    document.getElementById("resultTitle").textContent =
        "💀 GAME OVER!";

    document.getElementById("resultText").textContent =
        "Ronde terakhir: " + ronde +
        " | Skor akhir: " + skor +
        " | Best score: " + bestScore +
        ". Terus berlatih untuk meningkatkan ingatanmu!";

    document.getElementById("resultCard").classList.remove("hidden");
}

// ============================================================
// 12. PENGATURAN AWAL
// ============================================================

aturTombolWarna(false);
perbaruiSkor();

</script>

</body>
</html>
"""

# ============================================================
# 3. MENAMPILKAN GAME DI STREAMLIT
# ============================================================

components.html(
    html_game,
    height=850,
    scrolling=True
)
