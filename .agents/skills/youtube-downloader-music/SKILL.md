---
name: youtube-downloader-music
description: >
  Skill para agregar, modificar o extender funcionalidades al proyecto
  YouTube Downloader Music (CLI en Python). Úsala siempre que el usuario
  quiera agregar una nueva opción al menú, modificar la descarga, la
  conversión, la configuración, o cualquier otro comportamiento del programa.
  También aplica cuando el usuario diga "agregar feature", "nueva función",
  "modificar el downloader", "extender el proyecto" o similares.
---

# YouTube Downloader Music — Skill de desarrollo

## Propósito

Permite a cualquier IA agregar o modificar funcionalidades del proyecto
sin leer todos los archivos. Contiene el mapa arquitectónico, los contratos
de cada módulo y las convenciones de estilo para que el código nuevo
encaje sin fricciones.

---

## Arquitectura general

```
youtube_downloader/
├── main.py                  # Punto de entrada: instancia ConfigManager y Menu
├── requirements.txt         # Única dependencia externa: yt-dlp
├── canciones_lista.txt      # Ejemplo de lista de URLs (una por línea, # = comentario)
│
├── core/
│   ├── config_manager.py    # Lectura/escritura de ~/.ytdl_music_config.json
│   └── menu.py              # Despacha opciones; conoce solo las features
│
├── features/                # Una clase por opción de menú (SRP)
│   ├── downloader.py        # Opción 1 — descarga individual
│   ├── batch_downloader.py  # Opción 2 — descarga por lotes desde .txt
│   ├── converter.py         # Opción 3 — conversión de formato con rollback
│   └── configurator.py      # Opción 4 — edición interactiva de config
│
└── utils/
    ├── ui.py                # Colores ANSI, banner, sección, info/success/error/warning
    └── ytdlp_wrapper.py     # Wrapper de yt-dlp: download() → (bool, str) + barra progreso
```

---

## Contratos de los módulos clave

### `core/config_manager.py` — `ConfigManager`

Gestiona `~/.ytdl_music_config.json`.

```python
# Claves disponibles (con sus defaults)
{
  "download_dir":  "~/Music/Downloads",
  "converted_dir": "~/Music/Converted",
  "default_format": "mp3",
  "bitrate": "320k",          # opciones: "128k" | "192k" | "256k" | "320k"
}

config.get(key, fallback=None) -> Any
config.set(key, value)         # no guarda en disco
config.save()                  # persiste en JSON
config.get_all() -> dict       # copia del estado completo
config.ensure_dirs()           # crea download_dir y converted_dir si no existen
```

### `utils/ui.py` — `UI`

Todos los métodos imprimen directamente a stdout.

```python
ui.print_banner()          # limpia pantalla y muestra el encabezado ASCII
ui.print_menu()            # imprime las opciones del menú principal
ui.section(title: str)     # encabezado de sección con color azul
ui.info(message: str)      # ℹ  cian
ui.success(message: str)   # ✔  verde
ui.error(message: str)     # ✘  rojo
ui.warning(message: str)   # ⚠  amarillo
```

### `utils/ytdlp_wrapper.py` — `YtDlpWrapper`

```python
wrapper = YtDlpWrapper(config_manager)
success, message = wrapper.download(url: str, output_dir: str)
# success=True  → message = título de la canción descargada
# success=False → message = descripción amigable del error
```

La descarga usa `bestaudio/best`, convierte a MP3 con el bitrate de config,
embebe metadata (FFmpegMetadata) y maneja errores de JS de YouTube vía
`player_client: ["android", "web"]`.

### `core/menu.py` — `Menu`

```python
# En _dispatch se mapean teclas → métodos .run() de cada feature
options = {
    "1": self._downloader.run,
    "2": self._batch.run,
    "3": self._converter.run,
    "4": self._configurator.run,
    "5": self._exit,
}
```

---

## Cómo agregar una nueva funcionalidad

### 1. Crear la feature

Crea `features/mi_feature.py` siguiendo este patrón:

```python
from core.config_manager import ConfigManager
from utils.ui import UI

class MiFeature:
    def __init__(self, config_manager: ConfigManager):
        self._config = config_manager
        self._ui = UI()

    def run(self) -> None:
        self._ui.section("Título de la funcionalidad")
        # --- lógica aquí ---
        input("\n  Presiona Enter para continuar...")
```

Reglas:
- Una clase, un método público `run()`.
- Toda salida de texto pasa por `self._ui` (nunca `print` directo salvo barras de progreso).
- Siempre terminar con `input("\n  Presiona Enter para continuar...")`.
- Los errores recuperables se reportan con `self._ui.error(...)` sin relanzar la excepción.

### 2. Registrarla en el menú

En `core/menu.py`:

```python
# a) importar
from features.mi_feature import MiFeature

# b) instanciar en __init__
self._mi_feature = MiFeature(config_manager)

# c) agregar al dict de opciones en _dispatch
"6": self._mi_feature.run,
```

### 3. Actualizar la vista del menú

En `utils/ui.py`, método `print_menu()`, agregar la tupla:

```python
("6", "Descripción de la nueva opción"),
```

### 4. (Opcional) Agregar claves de configuración

En `core/config_manager.py`, añadir el default en `DEFAULT_CONFIG`:

```python
DEFAULT_CONFIG = {
    ...
    "mi_clave_nueva": "valor_default",
}
```

Y en `features/configurator.py` agregar la opción al submenú para que el
usuario pueda cambiarla.

---

## Convenciones de código

| Aspecto | Convención |
|---|---|
| Python | 3.10+ — usar `match/case` si encaja, type hints en firmas públicas |
| Strings | comillas dobles `"` |
| Imports | stdlib → terceros → internos, separados por línea en blanco |
| Errores | capturar excepciones específicas; nunca `except Exception` sin re-raise o log |
| Progreso | escribir en `sys.stdout` con `\r` y `sys.stdout.flush()` para no saltar líneas |
| Rollback | si se crea un archivo y la operación falla, borrarlo antes de reportar el error |
| Paths | siempre usar `pathlib.Path`, nunca `os.path.join` |
| Subprocesos | `subprocess.run(..., capture_output=True, timeout=300)` |

---

## Dependencias externas permitidas

| Paquete | Ya incluido | Para qué |
|---|---|---|
| `yt-dlp` | ✅ | descarga de YouTube / YouTube Music |
| `ffmpeg` (binario) | requiere instalación del usuario | conversión de audio |

Si la nueva feature necesita una dependencia nueva, agregarla a
`requirements.txt` con comentario explicativo y documentarlo en el README.

---

## Flujos de error estándar

```python
# Patrón: validar → operar → reportar → continuar
if not path.exists():
    self._ui.error(f"No se encontró: {path}")
    input("\n  Presiona Enter para continuar...")
    return

failed = []
for item in items:
    ok, msg = do_something(item)
    if ok:
        self._ui.success(f"✓ {msg}")
    else:
        self._ui.error(f"✗ {msg}")
        failed.append((item, msg))

if failed:
    self._ui.warning("Los siguientes elementos fallaron:")
    for item, reason in failed:
        print(f"    • {item} → {reason}")
```

---

## Ejemplos de extensiones típicas

- **Metadatos automáticos**: descargar portada y aplicarla al MP3 con `mutagen`.
- **Búsqueda por nombre**: integrar `yt-dlp` con `ytsearch:` para buscar sin URL.
- **Historial de descargas**: guardar URLs descargadas en `~/.ytdl_history.json` para evitar duplicados.
- **Descarga de listas de reproducción**: ya soportado por `yt-dlp`; solo hay que exponer la opción en el menú.
- **Normalización de volumen**: post-procesador de FFmpeg (`loudnorm`) aplicado tras la descarga.
- **Exportar config**: opción dentro del `Configurator` que guarda un `.env` o `.ini` compatible con otras herramientas.
