![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Plataforma-Windows-0078D4?logo=windows&logoColor=white)
![License](https://img.shields.io/badge/Licencia-MIT-2ea44f)

# YouTube Downloader Music

Aplicación de consola para descargar audio de enlaces de YouTube y YouTube
Music, organizar canciones y colecciones, y convertir archivos de audio entre
formatos. El proyecto está escrito en Python y utiliza `yt-dlp` para la
extracción de audio y FFmpeg para la conversión y el procesamiento de medios.

> Utiliza la aplicación únicamente con contenido que tengas derecho a
> descargar. El usuario es responsable de respetar los derechos de autor y las
> condiciones de uso de las plataformas.

## ¿Qué ofrece?

- Descarga individual de audio a MP3, con bitrate configurable entre 128 y
  320 kbps.
- Descarga de varias URL desde un archivo de texto, con progreso por pista y
  reporte de errores sin detener el resto de la lista.
- Descarga de playlists y álbumes en una carpeta propia; también acepta enlaces
  que correspondan a una sola pista.
- Inserción de metadatos y portada cuando la información está disponible.
- Conversión por lotes a MP3, FLAC, WAV, OGG, AAC, M4A, ALAC u Opus.
- Configuración de carpetas, bitrate, tiempo de espera de red y número máximo
  de descargas simultáneas de fragmentos.
- Limpieza de archivos temporales cuando una descarga falla o se interrumpe.
- Descarga automática de FFmpeg en el primer inicio, sin tener que configurarlo
  en el `PATH`.
- Compilación como ejecutable de consola de un solo archivo para Windows.

La conversión a un bitrate determinado no puede recuperar calidad que no exista
en el audio original.

## Menú principal

| Opción | Función |
|---|---|
| 1 | Descargar una canción |
| 2 | Descargar URL desde un archivo de texto |
| 3 | Descargar playlist o álbum |
| 4 | Convertir archivos de audio |
| 5 | Configurar el programa |
| 6 | Salir |

## Requisitos

### Ejecutar desde el código fuente

- Windows 10 o posterior.
- Python 3.10 o posterior.
- Conexión a internet para descargar FFmpeg en el primer inicio y obtener
  contenido de las plataformas.

FFmpeg se descarga desde BtbN FFmpeg-Builds y se guarda en
`%APPDATA%\YDM-CLI\ffmpeg`. El programa comprueba que el ejecutable funcione y
reutiliza la copia local en los siguientes inicios. No es necesario instalar
FFmpeg manualmente.

### Ejecutar el `.exe`

El usuario final no necesita instalar Python ni FFmpeg. El primer inicio del
ejecutable requiere internet para descargar FFmpeg; las funciones que descargan
contenido requieren conexión a internet.

## Instalación y ejecución desde el código

Abre PowerShell o el Símbolo del sistema en la carpeta donde quieras guardar el
proyecto.

### 1. Obtener el código

Con Git:

```powershell
git clone https://github.com/LK-Ronald/downloader-music.git
cd downloader-music
```

También puedes descargar el ZIP del repositorio y extraerlo en una carpeta.

### 2. Crear y activar un entorno virtual (recomendado)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Si usas Símbolo del sistema, activa el entorno con:

```cmd
venv\Scripts\activate
```

### 3. Instalar dependencias

```powershell
python -m pip install -r requirements.txt
```

### 4. Iniciar la aplicación

```powershell
python main.py
```

En el primer inicio, FFmpeg se descargará automáticamente. Mantén abierta la
consola durante la descarga.

## Uso

### Descargar una canción

Selecciona `1` y pega una URL de YouTube o YouTube Music. El archivo se
descarga como MP3 en la carpeta configurada. Por defecto, el bitrate es
`320k`; puedes cambiarlo a `128k`, `192k` o `256k` en Configuración. Si el
proveedor ofrece una portada, el programa intenta recortarla a formato
cuadrado e incrustarla con sus metadatos.

### Descargar desde una lista de texto

Selecciona `2` e indica la ruta del archivo. También puedes usar el archivo
`canciones_lista.txt` incluido en el proyecto. Escribe una URL por línea; las
líneas vacías y las que empiezan con `#` se ignoran:

```text
# Lista de ejemplo
https://www.youtube.com/watch?v=ID_DE_VIDEO
https://music.youtube.com/watch?v=ID_DE_VIDEO
```

El programa procesa las URL en orden y continúa con las siguientes aunque una
descarga falle.

### Descargar una playlist o álbum

Selecciona `3` y pega el enlace de la colección. Las pistas disponibles se
guardan en una subcarpeta nombrada a partir del título de la playlist o álbum.
Si el enlace es de una sola canción, el programa la descarga como pista
individual.

### Convertir archivos

Selecciona `4`, indica la carpeta de origen y la de destino, y elige un formato:
`mp3`, `flac`, `wav`, `ogg`, `aac`, `m4a`, `alac` u `opus`. La eliminación de
los originales es opcional y está desactivada por defecto. Si una conversión
falla, se elimina el archivo parcial correspondiente y el resto del lote
continúa.

### Configurar opciones

Selecciona `5` para cambiar los directorios de descargas y conversiones, el
bitrate, el tiempo máximo de conexión o el número de descargas simultáneas de
fragmentos. La descarga genera MP3; el selector de formato de conversión está
en la opción `4`.

| Ajuste | Valor inicial | Rango / opciones |
|---|---:|---|
| Directorio de descargas | `~/Music/Downloads` | Ruta configurable |
| Directorio de conversiones | `~/Music/Converted` | Ruta configurable |
| Bitrate | `320k` | `128k`, `192k`, `256k`, `320k` |
| Tiempo de espera de conexión | 30 segundos | 5–120 segundos |
| Descargas simultáneas de fragmentos | 4 | 1–8 |

La configuración se guarda en `~/.ytdl_music_config.json` (en Windows,
normalmente dentro de la carpeta del perfil del usuario).

## Crear el ejecutable de Windows

Con Python y las dependencias del proyecto instaladas, instala PyInstaller y
ejecuta el script de compilación:

```powershell
python -m pip install pyinstaller
python build.py
```

El ejecutable de consola se genera en `dist\YDM-CLI.exe`. FFmpeg no se incluye
en el `.exe`; cada usuario lo descarga en su primer inicio.

### Recompilar automáticamente al cambiar el código

Para compilar una vez y volver a compilar cuando cambien archivos Python,
PowerShell o `requirements.txt`, ejecuta desde PowerShell en la carpeta del
proyecto:

```powershell
.\watch_build.ps1
```

El watcher compila al arrancar, espera dos segundos de estabilidad tras los
cambios y actualiza `dist\YDM-CLI.exe`. Ignora las carpetas generadas. Para
detenerlo, presiona `Ctrl+C`. Si la política de ejecución de PowerShell impide
iniciar el script, puedes usar:

```powershell
powershell -ExecutionPolicy Bypass -File .\watch_build.ps1
```

## Estructura del proyecto

```text
.
├── main.py
├── build.py
├── watch_build.ps1
├── requirements.txt
├── canciones_lista.txt
├── core/
│   ├── config_manager.py
│   └── menu.py
├── features/
│   ├── downloader.py
│   ├── batch_downloader.py
│   ├── playlist_downloader.py
│   ├── converter.py
│   └── configurator.py
├── utils/
│   ├── ffmpeg_manager.py
│   ├── ffmpeg_process.py
│   ├── ui.py
│   └── ytdlp_wrapper.py
└── tests/
    └── test_ffmpeg_manager.py
```

- `core/` contiene la configuración persistente y el menú de navegación.
- `features/` contiene las acciones que el usuario ejecuta desde el menú.
- `utils/` incluye la integración con `yt-dlp`, la gestión de FFmpeg y la
  interfaz de consola.
- `build.py` y `watch_build.ps1` permiten crear y actualizar el ejecutable.

## Solución de problemas

**No se puede descargar FFmpeg**

Comprueba la conexión a internet y que GitHub sea accesible. FFmpeg se guarda
en `%APPDATA%\YDM-CLI\ffmpeg`; no necesita añadirse al `PATH`.

**Falla una descarga de YouTube**

Actualiza `yt-dlp` en el entorno Python activo y vuelve a intentarlo:

```powershell
python -m pip install --upgrade yt-dlp
```

Las plataformas pueden cambiar y requerir una versión reciente de `yt-dlp`.
Algunos videos pueden no estar disponibles, ser privados o tener restricciones.

**No se puede convertir un archivo**

Verifica que FFmpeg se haya descargado correctamente, que el archivo de origen
sea compatible y que haya espacio y permisos de escritura en la carpeta destino.

## Dependencias y licencias

- [yt-dlp](https://github.com/yt-dlp/yt-dlp): extracción y descarga multimedia.
- [Mutagen](https://github.com/quodlibet/mutagen): trabajo con metadatos de
  audio.
- [Pillow](https://python-pillow.org/): soporte de imágenes.
- [FFmpeg](https://ffmpeg.org/): conversión y procesamiento de audio y portadas.
  Se descarga durante la ejecución y no se distribuye dentro del `.exe`.

El código de este proyecto se distribuye bajo la licencia MIT. Las dependencias
y FFmpeg conservan sus propias licencias; consulta sus proyectos oficiales para
conocer sus términos.
