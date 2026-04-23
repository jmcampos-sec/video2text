"""
================================================================================
video_to_text.py
================================================================================
Descripción : Script interactivo que descarga un vídeo desde una URL,
              extrae el audio y lo transcribe a texto usando OpenAI Whisper.
Autor       : jmcampos-sec (https://github.com/jmcampos-sec)
Versión     : 2.0.0
Licencia    : MIT
================================================================================

Dependencias (instalar con: pip install -r requirements.txt):
    - yt-dlp
    - openai-whisper
    - tqdm

Requisito del sistema (instalar manualmente):
    - FFmpeg  →  https://ffmpeg.org/download.html
================================================================================
"""

import os
import sys
import subprocess
import platform
from datetime import datetime
from pathlib import Path

# Carpeta base donde se guardarán todas las transcripciones
CARPETA_BASE = "transcripciones"

# Archivo de historial global (dentro de la carpeta base)
ARCHIVO_HISTORIAL = os.path.join(CARPETA_BASE, "historial.txt")


# ──────────────────────────────────────────────────────────────────────────────
# UTILIDADES GENERALES
# ──────────────────────────────────────────────────────────────────────────────

def separador():
    """Imprime una línea separadora visual en la terminal."""
    print("─" * 60)


def carpeta_hoy() -> str:
    """
    Devuelve la ruta de la carpeta correspondiente al día actual.
    La crea si no existe.

    Returns:
        str: Ruta de la carpeta del día (ej: transcripciones/2025-04-23/)
    """
    fecha = datetime.now().strftime("%Y-%m-%d")
    ruta = os.path.join(CARPETA_BASE, fecha)
    os.makedirs(ruta, exist_ok=True)
    return ruta


def guardar_historial(url: str, nombre_archivo: str):
    """
    Añade una entrada al historial de transcripciones.

    Args:
        url            : URL del vídeo descargado.
        nombre_archivo : Nombre del archivo de transcripción generado.
    """
    # Crear la carpeta base si no existe
    os.makedirs(CARPETA_BASE, exist_ok=True)

    # Formatear la línea de historial con fecha, hora, URL y nombre de archivo
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    linea = f"{timestamp} | URL: {url} | Archivo: {nombre_archivo}\n"

    # Añadir la línea al historial (modo append para no sobreescribir)
    with open(ARCHIVO_HISTORIAL, "a", encoding="utf-8") as f:
        f.write(linea)

    print(f"📝  Historial actualizado: {ARCHIVO_HISTORIAL}")


def abrir_archivo(ruta: str):
    """
    Abre el archivo de transcripción con el programa predeterminado del sistema.

    Args:
        ruta: Ruta completa del archivo a abrir.
    """
    sistema = platform.system()

    if sistema == "Windows":
        os.startfile(ruta)
    elif sistema == "Darwin":
        # macOS
        subprocess.run(["open", ruta])
    else:
        # Linux
        subprocess.run(["xdg-open", ruta])


# ──────────────────────────────────────────────────────────────────────────────
# INTERACCIÓN CON EL USUARIO
# ──────────────────────────────────────────────────────────────────────────────

def pedir_url() -> str:
    """
    Solicita al usuario la URL del vídeo a procesar.

    Returns:
        str: URL introducida por el usuario.
    """
    separador()
    print("🎬  VIDEO2TEXT — Transcriptor automático de vídeos")
    separador()
    url = input("\n🔗  Introduce la URL del vídeo: ").strip()

    # Validar que no esté vacía
    if not url:
        print("❌  La URL no puede estar vacía.")
        sys.exit(1)

    return url


def detectar_titulo(url: str) -> str:
    """
    Usa yt-dlp para obtener el título del vídeo sin descargarlo.

    Args:
        url: URL del vídeo.

    Returns:
        str: Título del vídeo limpio para usar como nombre de archivo,
             o cadena vacía si no se pudo detectar.
    """
    print("\n🔍  Detectando título del vídeo...")

    resultado = subprocess.run(
        ["yt-dlp", "--no-playlist", "--print", "title", url],
        capture_output=True,
        text=True
    )

    if resultado.returncode != 0 or not resultado.stdout.strip():
        # Si no se puede detectar el título, devolvemos cadena vacía
        return ""

    # Limpiar el título para usarlo como nombre de archivo
    # Reemplazar caracteres problemáticos por guiones bajos
    titulo = resultado.stdout.strip()
    for caracter in r'<>:"/\|?* ':
        titulo = titulo.replace(caracter, "_")

    return titulo


def pedir_nombre(titulo_detectado: str) -> str:
    """
    Muestra el título detectado y permite al usuario aceptarlo o cambiarlo.

    Args:
        titulo_detectado: Título obtenido automáticamente del vídeo.

    Returns:
        str: Nombre final elegido para el archivo de transcripción.
    """
    if titulo_detectado:
        print(f"📌  Título detectado: {titulo_detectado}")
        nombre = input("✏️   ¿Quieres usar este nombre o prefieres otro? (Enter para aceptar): ").strip()

        # Si el usuario no escribe nada, usar el título detectado
        if not nombre:
            return titulo_detectado
        return nombre
    else:
        # Si no se detectó título, pedir nombre obligatoriamente
        print("⚠️   No se pudo detectar el título automáticamente.")
        nombre = input("✏️   Introduce un nombre para el archivo: ").strip()

        if not nombre:
            # Usar fecha y hora como nombre por defecto
            nombre = datetime.now().strftime("transcripcion_%Y%m%d_%H%M%S")

        return nombre


def pedir_modelo() -> str:
    """
    Solicita al usuario el modelo de Whisper a utilizar.
    Si pulsa Enter sin escribir nada, usa 'base' por defecto.

    Returns:
        str: Nombre del modelo elegido.
    """
    modelos_validos = ["tiny", "base", "small", "medium", "large"]

    print("\n🤖  Modelos disponibles: tiny | base | small | medium | large")
    modelo = input("⚙️   Modelo Whisper (Enter para 'base'): ").strip().lower()

    # Usar 'base' si el usuario no escribe nada
    if not modelo:
        return "base"

    # Validar que el modelo introducido sea válido
    if modelo not in modelos_validos:
        print(f"⚠️   Modelo no reconocido. Se usará 'base' por defecto.")
        return "base"

    return modelo


# ──────────────────────────────────────────────────────────────────────────────
# DESCARGA DEL VÍDEO
# ──────────────────────────────────────────────────────────────────────────────

def descargar_video(url: str, carpeta_salida: str) -> str:
    """
    Descarga el vídeo de la URL usando yt-dlp en la mejor calidad disponible.

    Args:
        url           : URL del vídeo a descargar.
        carpeta_salida: Carpeta donde guardar el vídeo descargado.

    Returns:
        str: Ruta completa del archivo de vídeo descargado.
    """
    separador()
    print(f"\n📥  Descargando vídeo...")

    # Plantilla de nombre de salida para yt-dlp
    plantilla_salida = os.path.join(carpeta_salida, "%(title)s.%(ext)s")

    resultado = subprocess.run(
        [
            "yt-dlp",
            "--no-playlist",                        # Solo el vídeo indicado
            "-f", "bestvideo+bestaudio/best",       # Mejor calidad disponible
            "--merge-output-format", "mp4",         # Formato de salida MP4
            "-o", plantilla_salida,
            "--print", "after_move:filepath",       # Imprimir ruta final
            url,
        ],
        capture_output=True,
        text=True
    )

    if resultado.returncode != 0:
        print("❌  Error al descargar el vídeo:")
        print(resultado.stderr)
        sys.exit(1)

    # Obtener la ruta del archivo descargado (última línea del output)
    ruta_video = resultado.stdout.strip().splitlines()[-1]
    print(f"✅  Vídeo descargado correctamente.")
    return ruta_video


# ──────────────────────────────────────────────────────────────────────────────
# EXTRACCIÓN DEL AUDIO
# ──────────────────────────────────────────────────────────────────────────────

def extraer_audio(ruta_video: str, carpeta_salida: str) -> str:
    """
    Extrae el audio del vídeo usando FFmpeg.
    Genera un archivo WAV a 16kHz mono, formato óptimo para Whisper.

    Args:
        ruta_video    : Ruta del archivo de vídeo.
        carpeta_salida: Carpeta donde guardar el audio extraído.

    Returns:
        str: Ruta completa del archivo de audio generado.
    """
    separador()
    print("\n🎵  Extrayendo audio...")

    # Construir la ruta del archivo de audio
    ruta_audio = os.path.join(
        carpeta_salida,
        Path(ruta_video).stem + ".wav"
    )

    resultado = subprocess.run(
        [
            "ffmpeg",
            "-y",                   # Sobreescribir si ya existe
            "-i", ruta_video,       # Archivo de entrada
            "-vn",                  # Sin pista de vídeo
            "-acodec", "pcm_s16le", # Codec de audio PCM 16 bits
            "-ar", "16000",         # Frecuencia de muestreo 16kHz (óptimo para Whisper)
            "-ac", "1",             # Canal mono
            ruta_audio,
        ],
        capture_output=True,
        text=True
    )

    if resultado.returncode != 0:
        print("❌  Error al extraer el audio:")
        print(resultado.stderr)
        sys.exit(1)

    print(f"✅  Audio extraído correctamente.")
    return ruta_audio


# ──────────────────────────────────────────────────────────────────────────────
# TRANSCRIPCIÓN DEL AUDIO
# ──────────────────────────────────────────────────────────────────────────────

def transcribir_audio(ruta_audio: str, modelo: str) -> str:
    """
    Transcribe el audio a texto usando OpenAI Whisper de forma local.

    Args:
        ruta_audio: Ruta del archivo de audio WAV.
        modelo    : Nombre del modelo Whisper a usar (tiny/base/small/medium/large).

    Returns:
        str: Texto completo de la transcripción.
    """
    # Verificar que Whisper está instalado
    try:
        import whisper
    except ImportError:
        print("❌  Whisper no está instalado. Ejecuta: pip install openai-whisper")
        sys.exit(1)

    separador()
    print(f"\n🤖  Cargando modelo Whisper '{modelo}'...")
    print("⏳  Esto puede tardar unos segundos la primera vez...\n")

    # Cargar el modelo (se descarga automáticamente la primera vez)
    model = whisper.load_model(modelo)

    print("📝  Transcribiendo audio...")
    print("⚠️   Este proceso puede tardar varios minutos según la duración del vídeo.\n")

    # Realizar la transcripción
    # verbose=True muestra progreso interno de Whisper
    resultado = model.transcribe(ruta_audio, verbose=False)
    print("✅  Transcripción completada.")

    return resultado["text"]


# ──────────────────────────────────────────────────────────────────────────────
# GUARDAR Y MOSTRAR RESULTADOS
# ──────────────────────────────────────────────────────────────────────────────

def guardar_transcripcion(texto: str, nombre: str, carpeta: str) -> str:
    """
    Guarda el texto de la transcripción en un archivo .txt.

    Args:
        texto  : Texto completo de la transcripción.
        nombre : Nombre base del archivo (sin extensión).
        carpeta: Carpeta donde guardar el archivo.

    Returns:
        str: Ruta completa del archivo guardado.
    """
    ruta_txt = os.path.join(carpeta, nombre + "_transcripcion.txt")

    with open(ruta_txt, "w", encoding="utf-8") as f:
        f.write(texto)

    return ruta_txt


def mostrar_preview(texto: str, num_caracteres: int = 500):
    """
    Muestra una vista previa de las primeras líneas de la transcripción.

    Args:
        texto         : Texto completo de la transcripción.
        num_caracteres: Número de caracteres a mostrar como preview.
    """
    separador()
    print("\n👁️   Vista previa de la transcripción:\n")
    preview = texto[:num_caracteres].strip()
    print(preview)

    # Indicar si hay más contenido
    if len(texto) > num_caracteres:
        print("\n[... continúa en el archivo ...]")

    print()


# ──────────────────────────────────────────────────────────────────────────────
# PROGRAMA PRINCIPAL
# ──────────────────────────────────────────────────────────────────────────────

def main():
    """
    Función principal que orquesta todo el proceso:
    1. Pedir URL al usuario
    2. Detectar y confirmar nombre del archivo
    3. Pedir modelo Whisper
    4. Descargar vídeo
    5. Extraer audio
    6. Transcribir
    7. Guardar resultados
    8. Actualizar historial
    9. Mostrar preview y abrir archivo
    """

    # ── Paso 1: Obtener URL ──────────────────────────────────────
    url = pedir_url()

    # ── Paso 2: Detectar título y confirmar nombre ───────────────
    titulo = detectar_titulo(url)
    nombre = pedir_nombre(titulo)

    # ── Paso 3: Elegir modelo Whisper ────────────────────────────
    modelo = pedir_modelo()

    # ── Preparar carpeta de salida organizada por fecha ──────────
    carpeta_salida = carpeta_hoy()

    # ── Paso 4: Descargar vídeo ──────────────────────────────────
    ruta_video = descargar_video(url, carpeta_salida)

    # ── Paso 5: Extraer audio ────────────────────────────────────
    ruta_audio = extraer_audio(ruta_video, carpeta_salida)

    # ── Paso 6: Transcribir ──────────────────────────────────────
    transcripcion = transcribir_audio(ruta_audio, modelo)

    # ── Paso 7: Guardar transcripción ────────────────────────────
    separador()
    ruta_txt = guardar_transcripcion(transcripcion, nombre, carpeta_salida)
    print(f"\n✅  ¡Transcripción completada!")
    print(f"📄  Guardada en: {ruta_txt}")

    # ── Paso 8: Actualizar historial ─────────────────────────────
    guardar_historial(url, os.path.basename(ruta_txt))

    # ── Limpieza: eliminar vídeo y audio temporales ───────────────
    os.remove(ruta_video)
    os.remove(ruta_audio)
    print("🗑️   Archivos temporales eliminados.")

    # ── Paso 9: Vista previa y apertura automática ────────────────
    mostrar_preview(transcripcion)

    separador()
    print("🎉  ¡Proceso completado con éxito!")
    separador()

    # Abrir el archivo automáticamente con el programa predeterminado
    abrir_archivo(ruta_txt)


# Punto de entrada del script
if __name__ == "__main__":
    main()
