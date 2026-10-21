# Tutorial: descargar música con YDM-CLI

Guía paso a paso para descargar el programa desde GitHub y empezar a
descargar música. Está escrita para **Windows 10/11** y asume que no tienes
Python ni FFmpeg instalados: no los necesitas, el ejecutable los gestiona
por su cuenta.

Los pasos de esta guía fueron probados con el ejecutable real de la release
`v2.0.0-alpha`.

---

## 1. Qué necesitas

- Windows 10 o posterior.
- Conexión a internet (para descargar FFmpeg la primera vez y para obtener
  el contenido de YouTube / YouTube Music).
- Nada más. No hay que instalar Python, `yt-dlp` ni FFmpeg.

> Usa el programa solo con contenido que tengas derecho a descargar. El
> usuario es responsable de respetar los derechos de autor y las condiciones
> de uso de las plataformas.

---

## 2. Descargar el programa desde GitHub

1. Abre la página de la release:

   https://github.com/LK-Ronald/YDM-CLI/releases/tag/v2.0.0-alpha

2. Baja hasta la sección **Assets** (archivos adjuntos) de esa página.

3. Descarga el archivo **`YDM-CLI.exe`** (unos 30 MB). Es un ejecutable de
   consola de un solo archivo: no hay que instalar nada, se guarda donde
   quieras y se abre con doble clic.

### Comprobar que el archivo está completo (opcional pero recomendado)

El `YDM-CLI.exe` de esa release tiene este tamaño y suma SHA-256:

```text
Tamaño:  31.801.401 bytes
SHA-256: 8ef7fe76ba484e53e13acc7c105ade1b8ff2396d2b1ee228f4812445a204f7ad
```

En PowerShell, dentro de la carpeta donde lo descargaste:

```powershell
Get-FileHash .\YDM-CLI.exe -Algorithm SHA256
```

El valor impreso debe coincidir con el de arriba (en mayúsculas).

> **Aviso sobre `YDM.exe.sha256`**: esa release incluye también un archivo
> `YDM.exe.sha256`. Su contenido **no corresponde** al `YDM-CLI.exe` que se
> publica junto a él (menciona `YDM.exe` y una suma distinta). No lo uses
> para verificar; calcula la suma del `.exe` tú mismo con el comando de
> arriba.

### Posible aviso de Windows SmartScreen

Al ser un ejecutable descargado de internet, Windows puede mostrar
"Windows protegió tu PC". Es normal en programas sin firma de código. Si
confías en la fuente, elige **Más información → Ejecutar de todos modos**.
El ejecutable no requiere permisos de administrador.

---

## 3. Primera ejecución: FFmpeg se descarga solo

Al abrir `YDM-CLI.exe` por primera vez, el programa detecta que no tiene
FFmpeg y lo descarga automáticamente desde BtbN FFmpeg-Builds.

- Aparece un mensaje `FFmpeg no encontrado. Descargando desde BtbN
  FFmpeg-Builds...` y una barra de progreso.
- La descarga es de unos **169 MB**. **No cierres la ventana de la consola
  mientras dura**: si la cierras, tendrás que repetirla.
- Al terminar verás `FFmpeg listo.` y, justo después, el menú principal.

Dónde queda guardado:

```text
%APPDATA%\YDM-CLI\ffmpeg\ffmpeg.exe
```

En la práctica, en tu carpeta de usuario:

```text
C:\Users\<tu-usuario>\AppData\Roaming\YDM-CLI\ffmpeg\ffmpeg.exe
```

FFmpeg no se añade al `PATH` del sistema y no se necesita instalar por
separado. En las siguientes aperturas el programa lo reutiliza y entra
directo al menú.

---

## 4. El menú principal

Al iniciar (después de lo anterior, si toca) verás:

```text
  ── Menú Principal ──
  [1] Descargar música
  [2] Descargar lista de músicas desde archivo
  [3] Descargar playlist o álbum
  [4] Convertir archivos a otro formato
  [5] Configuración
  [6] Salir
```

Escribe el número de la opción y pulsa `Enter`. El programa nunca se cierra
por una tecla inesperada: si escribes algo que no está entre 1 y 6, te avisa
y vuelve a mostrar el menú.

| Opción | Qué hace |
|---|---|
| 1 | Descarga una canción a partir de un enlace |
| 2 | Descarga varias canciones desde un archivo `.txt` |
| 3 | Descarga una playlist o álbum completa |
| 4 | Convierte archivos de audio de un formato a otro |
| 5 | Cambia carpetas, bitrate y otros ajustes |
| 6 | Sale del programa |

---

## 5. Descargar una sola canción (opción 1)

1. Selecciona `1`.
2. Pega el enlace de YouTube o YouTube Music cuando te lo pida. Sirve
   cualquier formato de enlace de vídeo:

   ```text
   https://www.youtube.com/watch?v=jNQXAC9IVRw
   https://music.youtube.com/watch?v=jNQXAC9IVRw
   ```

3. Pulsa `Enter`. El programa muestra el directorio de descarga, una barra
   de progreso con porcentaje, MB y ETA, y al terminar:

   ```text
   ✔  Descarga completada: Me at the zoo
   ```

4. Pulsa `Enter` para volver al menú.

El archivo se guarda como **MP3** en el directorio configurado (por
defecto `C:\Users\<tu-usuario>\Music\Downloads`), con el bitrate
configurado (por defecto `320k`). Si la fuente ofrece portada, el programa
la recorta a formato cuadrado (1:1) y la incrusta dentro del MP3 junto con
los metadatos (título, artista, álbum).

Para cambiar la carpeta o el bitrate, usa la opción `5` (ver sección 8).

---

## 6. Descargar varias canciones desde un archivo (opción 2)

Útil cuando tienes muchos enlaces a la vez.

1. Crea un archivo de texto, por ejemplo `mi_lista.txt`, con **un enlace por
   línea**. Las líneas vacías y las que empiezan por `#` se ignoran:

   ```text
   # Mi lista de canciones
   https://www.youtube.com/watch?v=jNQXAC9IVRw

   https://music.youtube.com/watch?v=jNQXAC9IVRw
   ```

   El proyecto incluye un archivo de ejemplo: `canciones_lista.txt`.

2. Selecciona `2` en el menú.
3. Escribe la ruta del archivo y pulsa `Enter`. Si pulsas `Enter` sin
   escribir nada, el programa usa `canciones_lista.txt` de la carpeta actual.
4. El programa indica cuántas canciones encontró y las descarga en orden:

   ```text
   ℹ    Se encontraron 3 canciones para descargar.
   ℹ    [1/3] Descargando: https://www.youtube.com/watch?v=jNQXAC9IVRw
   ✔    ✓ Completado: Me at the zoo
   ℹ    [2/3] Descargando: https://www.youtube.com/watch?v=INVALIDVIDEOID123
   ✘    ✗ Falló: ERROR: [youtube] ... This video is unavailable
   ```

5. Al final muestra el resumen y la lista de fallos, si los hubo:

   ```text
   ℹ    Proceso completado. 2/3 descargadas.
   ⚠    Las siguientes canciones fallaron:
       • https://...INVALIDVIDEOID123 → ERROR: [youtube] ...
   ```

   Un fallo **no detiene** el resto de la lista. Pulsa `Enter` para volver al
   menú.

---

## 7. Descargar una playlist o álbum (opción 3)

1. Selecciona `3`.
2. Pega el enlace de la playlist o álbum (YouTube o YouTube Music), por
   ejemplo:

   ```text
   https://www.youtube.com/playlist?list=PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf
   ```

3. El programa obtiene la información de la colección y crea **una subcarpeta
   propia con el nombre de la playlist** dentro del directorio de descargas:

   ```text
   ℹ  Colección detectada: Select Lectures
   ℹ  Total de canciones: 2
   ℹ  Carpeta destino: ...\Music\Downloads\Select Lectures
   ✔    ✓ Descargado: Deep Learning State of the Art (2020)
   ✔    ✓ Descargado: Deep Learning Basics: Introduction and Overview
   ℹ  Proceso completado. 2/2 canciones descargadas.
   ```

4. Pulsa `Enter` para volver al menú.

Si el enlace que pegaste corresponde a **una sola canción** (no a una
playlist), el programa lo detecta y la descarga como pista individual, sin
crear subcarpeta:

```text
ℹ  El enlace corresponde a una pista individual. Descargando canción...
```

---

## 8. Convertir archivos de audio (opción 4)

Para pasar MP3, FLAC, WAV, OGG, AAC, M4A, ALAC u Opus de un formato a otro.

1. Selecciona `4`.
2. **Directorio de origen**: escribe la carpeta donde están los archivos. Si
   pulsas `Enter` sin escribir, usa el directorio de descargas configurado.
3. **Directorio de destino**: escribe la carpeta donde quieres los
   convertidos. Si pulsas `Enter`, usa el directorio de conversiones
   configurado. Si no existe, el programa la crea.
4. **Formato de salida**: escribe uno de los formatos disponibles:

   ```text
   Formatos disponibles: mp3, flac, wav, ogg, aac, m4a, alac, opus
   ```

5. **¿Eliminar los originales tras convertir?** Responde `s` o `n`. Por
   defecto es **`n`** (no se borra nada).
6. El programa busca los archivos de audio de la carpeta, los convierte uno
   a uno y muestra el resultado:

   ```text
   ℹ    1 archivo(s) encontrados.
   ℹ    [1/1] Me at the zoo.mp3 → Me at the zoo.flac
   ✔    ✓ Convertido
   ℹ    Conversión completada. 1/1 exitosas.
   ```

   Pulsa `Enter` para volver al menú.

Si una conversión falla, el programa **elimina solo el archivo parcial**
correspondiente, conserva el original y continúa con el resto del lote. Al
final lista los archivos que fallaron.

> Convertir a un bitrate o formato distinto no recupera calidad que no
> exista en el audio original. Por ejemplo, pasar de MP3 a FLAC o ALAC no
> devuelve la calidad perdida: solo guarda lo que ya había, sin pérdida
> adicional.

---

## 9. Configurar el programa (opción 5)

Selecciona `5` para ver y cambiar los ajustes:

```text
  Configuración actual:
    📁 Descargas    : C:\Users\<tu-usuario>\Music\Downloads
    📁 Conversiones : C:\Users\<tu-usuario>\Music\Converted
    🎵 Formato      : mp3
    📻 Bitrate      : 320k
    ⏱️  Timeout      : 30 s
    🔀 Fragmentos   : 4 simultáneos

  ¿Qué deseas configurar?
  [1] Directorio de descargas
  [2] Directorio de conversiones
  [3] Formato de descarga por defecto
  [4] Bitrate de descarga
  [5] Tiempo máximo de espera de conexión
  [6] Descargas simultáneas de fragmentos
  [7] Volver al menú principal
```

| Ajuste | Valor inicial | Rango / opciones |
|---|---:|---|
| Directorio de descargas | `~/Music/Downloads` | Ruta configurable |
| Directorio de conversiones | `~/Music/Converted` | Ruta configurable |
| Formato por defecto | `mp3` | `mp3`, `flac`, `wav`, `aac`, `m4a`, `opus`, `ogg` |
| Bitrate | `320k` | `128k`, `192k`, `256k`, `320k` |
| Tiempo de espera de conexión | 30 segundos | 5–120 segundos |
| Descargas simultáneas de fragmentos | 4 | 1–8 |

Cuando el programa te pide un valor, **pulsa `Enter` sin escribir nada** para
dejarlo como está.

> **Detalle importante:** después de cambiar **un** ajuste, el configurador
> vuelve automáticamente al **menú principal** (no se queda en el submenú de
> configuración). Si quieres cambiar otro ajuste, vuelve a entrar a la
> opción `5`.

### Dónde se guarda la configuración

```text
C:\Users\<tu-usuario>\.ytdl_music_config.json
```

Se crea solo, la primera vez que cambias algo. No hace falta editarlo a
mano. Si prefieres empezar de cero, borra ese archivo: el programa lo
volverá a crear con los valores por defecto.

> Si editas ese archivo a mano, escribe las rutas con doble barra inversa,
> por ejemplo `"C:\\Music"`. Una sola barra (`"C:\Music"`) hace que el JSON
> sea inválido. En ese caso el programa no muestra error: simplemente
> **ignora el archivo y usa los valores por defecto**, y puede parecer que
> tus cambios no guardan.

---

## 10. Dónde acaban las cosas

| Qué | Dónde |
|---|---|
| Ejecutable | Donde lo hayas guardado (lo mueves libremente) |
| FFmpeg | `%APPDATA%\YDM-CLI\ffmpeg\ffmpeg.exe` |
| Canciones descargadas | `~/Music/Downloads` (configurable) |
| Playlists / álbumes | Subcarpeta con el nombre de la colección, dentro de `~/Music/Downloads` |
| Archivos convertidos | `~/Music/Converted` (configurable) |
| Configuración | `~/.ytdl_music_config.json` |

---

## 11. Solución de problemas

**El programa no arranca / se cierra al instante**

Comprueba que hayas descargado el `YDM-CLI.exe` completo (31.801.401 bytes).
Repite la descarga si el tamaño no coincide.

**No puede descargar FFmpeg**

Revisa tu conexión a internet y que GitHub sea accesible. FFmpeg se guarda en
`%APPDATA%\YDM-CLI\ffmpeg`; no necesita estar en el `PATH`. Si la descarga se
interrumpió, borra la carpeta `%APPDATA%\YDM-CLI\ffmpeg` y vuelve a abrir el
programa.

**Fallan las descargas de YouTube**

Actualiza `yt-dlp` y vuelve a intentarlo. Si ejecutas el programa desde el
código fuente:

```powershell
python -m pip install --upgrade yt-dlp
```

Las plataformas pueden cambiar y exigir una versión reciente. Algunos vídeos
pueden no estar disponibles, ser privados o tener restricciones.

**No se puede convertir un archivo**

Verifica que FFmpeg se haya descargado correctamente, que el archivo de
origen sea compatible, y que haya espacio y permisos de escritura en la
carpeta destino.

**La configuración no se guarda**

Casi siempre es el problema de las rutas explicado en la sección 9: el JSON
tiene que llevar rutas con doble barra inversa. Borra el archivo de
configuración y vuelve a crear los ajustes desde la opción `5`.

**¿Cómo se ejecuta desde el código fuente?**

Si en vez del `.exe` quieres correr el proyecto desde el código, consulta
`README.md` (sección "Instalación y ejecución desde el código"): clonar el
repositorio, crear un entorno virtual, instalar `requirements.txt` y lanzar
`python main.py`.

---

## 12. Resumen del flujo mínimo

```text
1. Descarga YDM-CLI.exe desde la release v2.0.0-alpha
2. Ábrelo y espera a que descargue FFmpeg (~169 MB, solo la primera vez)
3. Opción 1 → pega el enlace → la canción se guarda en MP3 en ~/Music/Downloads
4. Opción 6 para salir
```

Para listas y colecciones, usa las opciones `2` y `3`; para cambiar de
formato, la opción `4`; para ajustar carpetas y calidad, la opción `5`.
