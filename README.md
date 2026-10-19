# 🎵 YouTube Downloader Music

Descarga y convierte música de YouTube y YouTube Music desde la línea de comandos, con barra de progreso, descarga por lotes y conversión entre formatos de audio.

---

## ✅ Requisitos previos

| Herramienta | Versión mínima | Descarga |
|---|---|---|
| Python | 3.10+ | https://www.python.org/downloads/ |
| FFmpeg | Cualquier versión reciente | https://ffmpeg.org/download.html |

> **Importante:** tanto `python` como `ffmpeg` deben estar en el `PATH` del sistema.

---

## 🪟 Instalación paso a paso en Windows

### Paso 1 — Instalar Python

1. Ve a https://www.python.org/downloads/ y descarga la versión más reciente.
2. Abre el instalador.
3. **Marca la casilla "Add Python to PATH"** antes de hacer clic en *Install Now*.
4. Completa la instalación.
5. Verifica abriendo el **Símbolo del sistema** (`Win + R` → escribe `cmd` → Enter):

```
python --version
```

Deberías ver algo como `Python 3.12.x`.

---

### Paso 2 — Instalar FFmpeg

FFmpeg es necesario para convertir el audio descargado a MP3.

1. Ve a https://github.com/BtbN/FFmpeg-Builds/releases
2. Descarga `ffmpeg-master-latest-win64-gpl.zip`.
3. Extrae el ZIP (por ejemplo en `C:\ffmpeg`).
4. Agrega FFmpeg al PATH del sistema:
   - Abre **Inicio** → busca *"Variables de entorno"* → **Editar las variables de entorno del sistema**.
   - En la ventana que aparece haz clic en **Variables de entorno...**.
   - En *Variables del sistema*, selecciona `Path` y haz clic en **Editar**.
   - Haz clic en **Nuevo** y escribe la ruta a la carpeta `bin` de FFmpeg, por ejemplo: `C:\ffmpeg\bin`
   - Acepta todas las ventanas con **Aceptar**.
5. Cierra y vuelve a abrir el Símbolo del sistema y verifica:

```
ffmpeg -version
```

---

### Paso 3 — Descargar el proyecto

**Opción A — Con Git:**
```cmd
git clone https://github.com/tu-usuario/youtube-downloader-music.git
cd youtube-downloader-music
```

**Opción B — Sin Git:**
1. Descarga el ZIP del repositorio.
2. Extráelo en la carpeta que prefieras (ej. `C:\youtube-downloader-music`).
3. Abre el Símbolo del sistema y navega a esa carpeta:

```cmd
cd C:\youtube-downloader-music
```

---

### Paso 4 — Crear un entorno virtual (recomendado)

```cmd
python -m venv venv
venv\Scripts\activate
```

Verás `(venv)` al inicio de la línea cuando esté activo.

---

### Paso 5 — Instalar las dependencias

```cmd
pip install -r requirements.txt
```

---

### Paso 6 — Ejecutar el programa

```cmd
python main.py
```

Aparecerá el menú principal:

```
  ╔══════════════════════════════════════════════════╗
  ║   🎵  YouTube Downloader Music  🎵               ║
  ║   Descarga y convierte música fácilmente         ║
  ╚══════════════════════════════════════════════════╝

  ── Menú Principal ──

  [1] Descargar música
  [2] Descargar lista de músicas desde archivo
  [3] Convertir archivos a otro formato
  [4] Configuración
  [5] Salir
```

---

## 📖 Uso de cada funcionalidad

### [1] Descargar música

1. Elige la opción `1`.
2. Pega el enlace de YouTube o YouTube Music.
3. El programa descarga automáticamente en la mejor calidad disponible y convierte a **MP3** con el bitrate configurado (por defecto **320 kbps**).
4. La canción se guarda en el directorio configurado en **Configuración** (por defecto: `C:\Users\TuUsuario\Music\Downloads`).

---

### [2] Descargar lista desde archivo

1. Crea un archivo de texto (o edita `canciones_lista.txt`).
2. Escribe una URL por línea. Las líneas que empiezan con `#` son comentarios.

```
# Mi lista de música
https://www.youtube.com/watch?v=XXXXXXXXXXX
https://music.youtube.com/watch?v=XXXXXXXXXXX
```

3. Elige la opción `2` e indica la ruta del archivo.
4. El programa descarga todas las canciones una por una mostrando el progreso. Si alguna falla, avisa y continúa con las demás.

---

### [3] Convertir archivos a otro formato

1. Elige la opción `3`.
2. Indica el directorio de origen (o presiona Enter para usar el configurado).
3. Indica el directorio destino donde se guardarán los archivos convertidos.
4. Elige el formato de salida: `mp3`, `flac`, `wav`, `ogg`, `aac`, `m4a`, `alac`, `opus`.
5. Indica si deseas eliminar los archivos originales (por defecto: **No**).
6. El programa convierte todos los archivos de audio encontrados. Si alguno falla, hace **rollback** (elimina el archivo parcial) y muestra cuáles fallaron.

---

### [4] Configuración

Permite personalizar:

- **Directorio de descargas** — dónde se guardan las canciones descargadas.
- **Directorio de conversiones** — dónde se guardan los archivos convertidos.
- **Formato de descarga** — formato de salida al descargar (por defecto: `mp3`).
- **Bitrate** — calidad del audio: `128k`, `192k`, `256k`, `320k` (por defecto: `320k`).

La configuración se guarda en `C:\Users\TuUsuario\.ytdl_music_config.json`.

---

## 🗂️ Estructura del proyecto

```
youtube-downloader-music/
├── main.py                      # Punto de entrada
├── requirements.txt             # Dependencias
├── canciones_lista.txt          # Ejemplo de lista de canciones
├── README.md
│
├── core/                        # Lógica central
│   ├── config_manager.py        # Gestión de configuración (SRP)
│   └── menu.py                  # Menú principal (OCP)
│
├── features/                    # Funcionalidades del menú
│   ├── downloader.py            # Opción 1: descarga individual
│   ├── batch_downloader.py      # Opción 2: descarga por lotes
│   ├── converter.py             # Opción 3: conversión de formatos
│   └── configurator.py          # Opción 4: configuración
│
└── utils/                       # Utilidades transversales
    ├── ui.py                    # Colores y presentación en consola
    └── ytdlp_wrapper.py         # Wrapper de yt-dlp con barra de progreso
```

---

## 🔧 Actualizar yt-dlp

YouTube actualiza su plataforma frecuentemente. Si las descargas fallan con errores de JavaScript, actualiza yt-dlp:

```cmd
pip install -U yt-dlp
```

---

## ❓ Preguntas frecuentes

**¿El programa descarga listas de reproducción completas?**
La opción 1 acepta URLs de listas de reproducción de YouTube. yt-dlp las detecta automáticamente y descarga todas las canciones.

**¿Por qué dice "FFmpeg no encontrado"?**
FFmpeg no está en el PATH. Revisa el Paso 2 de la instalación.

**¿La calidad de audio es buena?**
Sí. El programa descarga el mejor audio disponible (generalmente 128–320 kbps según la fuente) y lo convierte a MP3 con el bitrate que configures (mínimo 128 kbps por defecto 320 kbps).

**¿Funciona con YouTube Music?**
Sí. Acepta URLs de `music.youtube.com` y `youtube.com` indistintamente.

---

## 📄 Licencia

MIT License — libre para uso personal y educativo.
