# 🎬 video2text

> Descarga vídeos desde cualquier URL, extrae el audio y genera una transcripción en texto de forma automática.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Whisper](https://img.shields.io/badge/OpenAI-Whisper-412991?logo=openai&logoColor=white)
![yt-dlp](https://img.shields.io/badge/yt--dlp-latest-red)
![FFmpeg](https://img.shields.io/badge/FFmpeg-required-green?logo=ffmpeg&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📋 Índice

- [¿Qué hace?](#-qué-hace)
- [Características](#-características)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Modelos Whisper](#-modelos-whisper)
- [Estructura del proyecto](#-estructura-del-proyecto)
- [English version](#-english-version)

---

## ¿Qué hace?

`video2text` es un script interactivo en Python que realiza tres pasos de forma automática:

1. **Descarga** el vídeo desde la URL indicada (compatible con YouTube, Vimeo, Twitter/X y más de 1000 sitios).
2. **Extrae** el audio en formato WAV optimizado para transcripción.
3. **Transcribe** el audio a texto usando OpenAI Whisper, completamente en local y sin coste.

---

## ✨ Características

- 🖥️ **Interfaz interactiva** — sin necesidad de recordar comandos largos
- 🔍 **Detección automática del título** — sugiere el nombre del archivo y permite modificarlo
- 📁 **Organización por fecha** — cada transcripción se guarda en su carpeta del día
- 📊 **Barra de progreso** — información en tiempo real durante la transcripción
- 📖 **Vista previa inmediata** — muestra las primeras líneas al terminar
- 📝 **Historial de descargas** — registro de URLs, nombres y fechas
- 🚀 **Apertura automática** — abre el .txt al finalizar
- 🌍 **Multiidioma** — Whisper soporta más de 99 idiomas

---

## 📦 Requisitos

- Python 3.8 o superior
- [FFmpeg](https://ffmpeg.org/download.html) — instalado en el sistema y en el PATH *(no se instala con pip)*
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — descarga de vídeos
- [openai-whisper](https://github.com/openai/whisper) — transcripción de audio
- [tqdm](https://github.com/tqdm/tqdm) — barra de progreso

---

## 🔧 Instalación

### 1. Clona el repositorio

```bash
git clone https://github.com/jmcampos-sec/video2text.git
cd video2text
```

### 2. Instala las dependencias Python

```bash
pip install -r requirements.txt
```

### 3. Instala FFmpeg

FFmpeg es necesario para extraer el audio del vídeo. No se instala con pip, hay que instalarlo en el sistema:

| Sistema | Comando / Descarga |
|---------|--------------------|
| Windows | Descarga desde [ffmpeg.org](https://ffmpeg.org/download.html) y añade la carpeta `bin` al PATH |
| Linux | `sudo apt install ffmpeg` |
| macOS | `brew install ffmpeg` |

Verifica la instalación:

```bash
ffmpeg -version
```

---

## 🚀 Uso

Ejecuta el script y sigue las instrucciones interactivas:

```bash
python video_to_text.py
```

El flujo es el siguiente:

```
Introduce la URL del vídeo: https://...
Detectando título del vídeo...
Título detectado: Clase_LogicaDifusa_20250423
¿Quieres usar este nombre o prefieres otro? (Enter para aceptar): 
Modelo Whisper [tiny/base/small/medium/large] (Enter para 'base'): 

📥 Descargando vídeo...
🎵 Extrayendo audio...
📝 Transcribiendo... [████████████████████] 100%

✅ Transcripción completada!
📄 Guardada en: transcripciones/2025-04-23/Clase_LogicaDifusa_20250423.txt
```

---

## 🤖 Modelos Whisper

| Modelo | Velocidad | Precisión | RAM |
|--------|-----------|-----------|-----|
| `tiny` | ⚡⚡⚡ | ★★☆☆☆ | ~1 GB |
| `base` | ⚡⚡ | ★★★☆☆ | ~1 GB |
| `small` | ⚡ | ★★★★☆ | ~2 GB |
| `medium` | 🐢 | ★★★★★ | ~5 GB |
| `large` | 🐢🐢 | ★★★★★ | ~10 GB |

> 💡 Recomendación: empieza con `base`. Si necesitas más precisión en términos técnicos, prueba `small` o `medium`.

---

## 📁 Estructura del proyecto

```
video2text/
│
├── video_to_text.py        # Script principal
├── requirements.txt        # Dependencias del proyecto
├── README.md               # Este archivo
├── LICENSE                 # Licencia MIT
│
└── transcripciones/        # Generada automáticamente
    └── 2025-04-23/
        ├── Clase_LogicaDifusa.txt
        └── historial.txt
```

---

## ⚠️ Aviso legal

Este proyecto es para uso personal y educativo. Respeta los términos de servicio de las plataformas y los derechos de autor del contenido que descargues.

---

---

# 🌐 English version

> Download videos from any URL, extract the audio and automatically generate a text transcription.

---

## What does it do?

`video2text` is an interactive Python script that automatically performs three steps:

1. **Downloads** the video from the given URL (compatible with YouTube, Vimeo, Twitter/X and 1000+ sites).
2. **Extracts** the audio in WAV format optimized for transcription.
3. **Transcribes** the audio to text using OpenAI Whisper, fully locally and at no cost.

---

## ✨ Features

- 🖥️ **Interactive interface** — no need to remember long commands
- 🔍 **Automatic title detection** — suggests the filename and allows modification
- 📁 **Date-based organization** — each transcription is saved in its daily folder
- 📊 **Progress bar** — real-time information during transcription
- 📖 **Instant preview** — shows the first lines when finished
- 📝 **Download history** — log of URLs, names and dates
- 🚀 **Auto-open** — opens the .txt file when done
- 🌍 **Multilingual** — Whisper supports 99+ languages

---

## 📦 Requirements

- Python 3.8 or higher
- [FFmpeg](https://ffmpeg.org/download.html) — installed at system level and added to PATH *(not installed via pip)*
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — video downloading
- [openai-whisper](https://github.com/openai/whisper) — audio transcription
- [tqdm](https://github.com/tqdm/tqdm) — progress bar

---

## 🔧 Installation

### 1. Clone the repository

```bash
git clone https://github.com/jmcampos-sec/video2text.git
cd video2text
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Install FFmpeg

FFmpeg is required to extract audio from video. It is not installed via pip — it must be installed at the system level:

| OS | Command / Download |
|----|--------------------|
| Windows | Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add the `bin` folder to PATH |
| Linux | `sudo apt install ffmpeg` |
| macOS | `brew install ffmpeg` |

Verify installation:

```bash
ffmpeg -version
```

---

## 🚀 Usage

Run the script and follow the interactive prompts:

```bash
python video_to_text.py
```

---

## 🤖 Whisper Models

| Model | Speed | Accuracy | RAM |
|-------|-------|----------|-----|
| `tiny` | ⚡⚡⚡ | ★★☆☆☆ | ~1 GB |
| `base` | ⚡⚡ | ★★★☆☆ | ~1 GB |
| `small` | ⚡ | ★★★★☆ | ~2 GB |
| `medium` | 🐢 | ★★★★★ | ~5 GB |
| `large` | 🐢🐢 | ★★★★★ | ~10 GB |

---

## ⚠️ Legal disclaimer

This project is for personal and educational use only. Please respect the terms of service of the platforms and the copyright of the content you download.

---

## 📜 License

MIT License — see [LICENSE](LICENSE) for details.

---

*Developed with the assistance of AI — idea, design and testing by [jmcampos-sec](https://github.com/jmcampos-sec)*
