# Tutorial: downloading music with YDM-CLI

Step-by-step guide to downloading the program from GitHub and starting to
download music. It is written for **Windows 10/11** and assumes you do not
have Python or FFmpeg installed: you do not need them, the executable
handles them on its own.

The steps in this guide were tested with the real executable from the
`v2.0.0-alpha` release.

---

## 1. What you need

- Windows 10 or later.
- An internet connection (to download FFmpeg the first time and to fetch
  content from YouTube / YouTube Music).
- Nothing else. You do not need to install Python, `yt-dlp`, or FFmpeg.

> Use the program only with content you have the right to download. The user
> is responsible for respecting copyright and the platforms' terms of use.

---

## 2. Downloading the program from GitHub

1. Open the release page:

   https://github.com/LK-Ronald/YDM-CLI/releases/tag/v2.0.0-alpha

2. Scroll down to the **Assets** section of that page.

3. Download the **`YDM-CLI.exe`** file (about 30 MB). It is a single-file
   console executable: nothing has to be installed, you save it wherever you
   want, and it opens with a double click.

### Checking that the file is complete (optional but recommended)

The `YDM-CLI.exe` from that release has this size and SHA-256 sum:

```text
Size:  31,801,401 bytes
SHA-256: 8ef7fe76ba484e53e13acc7c105ade1b8ff2396d2b1ee228f4812445a204f7ad
```

In PowerShell, inside the folder where you downloaded it:

```powershell
Get-FileHash .\YDM-CLI.exe -Algorithm SHA256
```

The printed value must match the one above (in uppercase).

> **Warning about `YDM.exe.sha256`**: that release also includes a
> `YDM.exe.sha256` file. Its content **does not match** the `YDM-CLI.exe`
> published next to it (it mentions `YDM.exe` and a different sum). Do not
> use it to verify; compute the sum of the `.exe` yourself with the command
> above.

### Possible Windows SmartScreen warning

Because it is an executable downloaded from the internet, Windows may show
"Windows protected your PC". This is normal for programs without code
signing. If you trust the source, choose **More info → Run anyway**. The
executable does not require administrator permissions.

---

## 3. First run: FFmpeg downloads itself

When you open `YDM-CLI.exe` for the first time, the program detects that it
does not have FFmpeg and downloads it automatically from BtbN FFmpeg-Builds.

- A message appears: `FFmpeg no encontrado. Descargando desde BtbN
  FFmpeg-Builds...`, along with a progress bar.
- The download is about **169 MB**. **Do not close the console window while
  it runs**: if you close it, you will have to repeat it.
- When it finishes you will see `FFmpeg listo.` and, right after, the main
  menu.

Where it is saved:

```text
%APPDATA%\YDM-CLI\ffmpeg\ffmpeg.exe
```

In practice, in your user folder:

```text
C:\Users\<your-user>\AppData\Roaming\YDM-CLI\ffmpeg\ffmpeg.exe
```

FFmpeg is not added to the system `PATH` and does not need to be installed
separately. On subsequent launches the program reuses it and goes straight
to the menu.

---

## 4. The main menu

When you start it (after the previous step, if it applies) you will see:

```text
  ── Main Menu ──
  [1] Download music
  [2] Download a list of songs from a file
  [3] Download a playlist or album
  [4] Convert files to another format
  [5] Settings
  [6] Exit
```

Type the option number and press `Enter`. The program never closes because
of an unexpected key: if you type something that is not between 1 and 6, it
warns you and shows the menu again.

| Option | What it does |
|---|---|
| 1 | Downloads a single song from a link |
| 2 | Downloads several songs from a `.txt` file |
| 3 | Downloads a full playlist or album |
| 4 | Converts audio files from one format to another |
| 5 | Changes folders, bitrate and other settings |
| 6 | Exits the program |

---

## 5. Downloading a single song (option 1)

1. Select `1`.
2. Paste the YouTube or YouTube Music link when prompted. Any video link
   format works:

   ```text
   https://www.youtube.com/watch?v=jNQXAC9IVRw
   https://music.youtube.com/watch?v=jNQXAC9IVRw
   ```

3. Press `Enter`. The program shows the download directory, a progress bar
   with percentage, MB and ETA, and when it finishes:

   ```text
   ✔  Download completed: Me at the zoo
   ```

4. Press `Enter` to return to the menu.

The file is saved as **MP3** in the configured directory (by default
`C:\Users\<your-user>\Music\Downloads`), with the configured bitrate (by
default `320k`). If the source offers a cover, the program crops it to a
square format (1:1) and embeds it inside the MP3 along with the metadata
(title, artist, album).

To change the folder or the bitrate, use option `5` (see section 8).

---

## 6. Downloading several songs from a file (option 2)

Useful when you have many links at once.

1. Create a text file, for example `mi_lista.txt`, with **one link per
   line**. Blank lines and lines starting with `#` are ignored:

   ```text
   # My song list
   https://www.youtube.com/watch?v=jNQXAC9IVRw

   https://music.youtube.com/watch?v=jNQXAC9IVRw
   ```

   The project includes an example file: `canciones_lista.txt`.

2. Select `2` in the menu.
3. Type the path of the file and press `Enter`. If you press `Enter` without
   typing anything, the program uses `canciones_lista.txt` from the current
   folder.
4. The program reports how many songs it found and downloads them in order:

   ```text
   ℹ    3 songs found to download.
   ℹ    [1/3] Downloading: https://www.youtube.com/watch?v=jNQXAC9IVRw
   ✔    ✓ Completed: Me at the zoo
   ℹ    [2/3] Downloading: https://www.youtube.com/watch?v=INVALIDVIDEOID123
   ✘    ✗ Failed: ERROR: [youtube] ... This video is unavailable
   ```

5. At the end it shows the summary and the list of failures, if any:

   ```text
   ℹ    Process completed. 2/3 downloaded.
   ⚠    The following songs failed:
       • https://...INVALIDVIDEOID123 → ERROR: [youtube] ...
   ```

   A failure does **not stop** the rest of the list. Press `Enter` to return
   to the menu.

---

## 7. Downloading a playlist or album (option 3)

1. Select `3`.
2. Paste the link of the playlist or album (YouTube or YouTube Music), for
   example:

   ```text
   https://www.youtube.com/playlist?list=PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf
   ```

3. The program gets the collection information and creates **its own
   subfolder named after the playlist** inside the downloads directory:

   ```text
   ℹ  Collection detected: Select Lectures
   ℹ  Total songs: 2
   ℹ  Destination folder: ...\Music\Downloads\Select Lectures
   ✔    ✓ Downloaded: Deep Learning State of the Art (2020)
   ✔    ✓ Downloaded: Deep Learning Basics: Introduction and Overview
   ℹ  Process completed. 2/2 songs downloaded.
   ```

4. Press `Enter` to return to the menu.

If the link you pasted corresponds to **a single song** (not a playlist), the
program detects it and downloads it as an individual track, without creating
a subfolder:

```text
ℹ  The link corresponds to an individual track. Downloading song...
```

---

## 8. Converting audio files (option 4)

To convert MP3, FLAC, WAV, OGG, AAC, M4A, ALAC, or Opus from one format to
another.

1. Select `4`.
2. **Source directory**: type the folder where the files are. If you press
   `Enter` without typing, it uses the configured downloads directory.
3. **Destination directory**: type the folder where you want the converted
   files. If you press `Enter`, it uses the configured conversions
   directory. If it does not exist, the program creates it.
4. **Output format**: type one of the available formats:

   ```text
   Available formats: mp3, flac, wav, ogg, aac, m4a, alac, opus
   ```

5. **Delete the originals after converting?** Answer `s` or `n`. By default
   it is **`n`** (nothing is deleted).
6. The program looks for the audio files in the folder, converts them one by
   one, and shows the result:

   ```text
   ℹ    1 file(s) found.
   ℹ    [1/1] Me at the zoo.mp3 → Me at the zoo.flac
   ✔    ✓ Converted
   ℹ    Conversion completed. 1/1 successful.
   ```

   Press `Enter` to return to the menu.

If a conversion fails, the program **deletes only the corresponding partial
file**, keeps the original, and continues with the rest of the batch. At the
end it lists the files that failed.

> Converting to a different bitrate or format does not recover quality that
> does not exist in the original audio. For example, converting from MP3 to
> FLAC or ALAC does not bring back the lost quality: it only stores what was
> already there, with no additional loss.

---

## 9. Configuring the program (option 5)

Select `5` to view and change the settings:

```text
  Current settings:
    📁 Downloads    : C:\Users\<your-user>\Music\Downloads
    📁 Conversions  : C:\Users\<your-user>\Music\Converted
    🎵 Format       : mp3
    📻 Bitrate      : 320k
    ⏱️  Timeout      : 30 s
    🔀 Fragments    : 4 simultaneous

  What do you want to configure?
  [1] Downloads directory
  [2] Conversions directory
  [3] Default download format
  [4] Download bitrate
  [5] Maximum connection timeout
  [6] Simultaneous fragment downloads
  [7] Back to the main menu
```

| Setting | Initial value | Range / options |
|---|---:|---|
| Downloads directory | `~/Music/Downloads` | Configurable path |
| Conversions directory | `~/Music/Converted` | Configurable path |
| Default format | `mp3` | `mp3`, `flac`, `wav`, `aac`, `m4a`, `opus`, `ogg` |
| Bitrate | `320k` | `128k`, `192k`, `256k`, `320k` |
| Connection timeout | 30 seconds | 5–120 seconds |
| Simultaneous fragment downloads | 4 | 1–8 |

When the program asks for a value, **press `Enter` without typing anything**
to leave it as it is.

> **Important detail:** after changing **one** setting, the configurator
> returns automatically to the **main menu** (it does not stay in the
> settings submenu). If you want to change another setting, enter option `5`
> again.

### Where the settings are saved

```text
C:\Users\<your-user>\.ytdl_music_config.json
```

It is created on its own the first time you change something. There is no
need to edit it by hand. If you prefer to start from scratch, delete that
file: the program will create it again with the default values.

> If you edit that file by hand, write paths with a double backslash, for
> example `"C:\\Music"`. A single backslash (`"C:\Music"`) makes the JSON
> invalid. In that case the program does not show an error: it simply
> **ignores the file and uses the default values**, and it may seem like
> your changes are not saving.

---

## 10. Where things end up

| What | Where |
|---|---|
| Executable | Wherever you saved it (you can move it freely) |
| FFmpeg | `%APPDATA%\YDM-CLI\ffmpeg\ffmpeg.exe` |
| Downloaded songs | `~/Music/Downloads` (configurable) |
| Playlists / albums | Subfolder named after the collection, inside `~/Music/Downloads` |
| Converted files | `~/Music/Converted` (configurable) |
| Settings | `~/.ytdl_music_config.json` |

---

## 11. Troubleshooting

**The program does not start / closes instantly**

Check that you downloaded the complete `YDM-CLI.exe` (31,801,401 bytes).
Repeat the download if the size does not match.

**It cannot download FFmpeg**

Check your internet connection and that GitHub is accessible. FFmpeg is
saved in `%APPDATA%\YDM-CLI\ffmpeg`; it does not need to be in the `PATH`.
If the download was interrupted, delete the `%APPDATA%\YDM-CLI\ffmpeg`
folder and open the program again.

**YouTube downloads fail**

Update `yt-dlp` and try again. If you run the program from the source code:

```powershell
python -m pip install --upgrade yt-dlp
```

The platforms may change and require a recent version. Some videos may not
be available, may be private, or may have restrictions.

**A file cannot be converted**

Verify that FFmpeg downloaded correctly, that the source file is compatible,
and that there is space and write permissions in the destination folder.

**The settings are not saved**

It is almost always the path problem explained in section 9: the JSON has to
have paths with a double backslash. Delete the settings file and recreate
the settings from option `5`.

**How do you run it from the source code?**

If instead of the `.exe` you want to run the project from the code, see
`README.md` (section "Instalación y ejecución desde el código"): clone the
repository, create a virtual environment, install `requirements.txt` and run
`python main.py`.

---

## 12. Minimum flow summary

```text
1. Download YDM-CLI.exe from the v2.0.0-alpha release
2. Open it and wait for it to download FFmpeg (~169 MB, only the first time)
3. Option 1 → paste the link → the song is saved as MP3 in ~/Music/Downloads
4. Option 6 to exit
```

For lists and collections, use options `2` and `3`; to change format, option
`4`; to adjust folders and quality, option `5`.
