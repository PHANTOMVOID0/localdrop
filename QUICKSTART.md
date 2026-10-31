# LocalDrop — start in a few minutes

## 1. Extract the ZIP
Extract the entire `localdrop` folder to a writable location, for example
Documents/LocalDrop. Do not run directly inside a ZIP viewer. Keep all subfolders.

## 2. Install Python and launch
Python 3.10+ is required. On Windows enable **Add python.exe to PATH** when installing.

**Windows:** double-click **start.bat**. It runs setup on first launch, then starts
LocalDrop. Alternatively open a terminal in this folder and run:
```bat
py -3 setup.py
.venv\Scripts\python.exe server.py
```

**macOS / Linux:** open Terminal in this folder:
```sh
python3 setup.py
bash start.sh
```
For macOS you can also use `bash start.command`. If you want to double-click
`start.command`, run `chmod +x start.command start.sh` first.
On Debian/Ubuntu, if Python says ensurepip/venv is missing, install the Python venv
package for your installed Python version before retrying.

First setup downloads dependencies and requires internet. File transfers after setup
stay local. Wait until the terminal prints the QR and server address.

## 3. Open the dashboard on your PC
It should open automatically. Otherwise visit:
**http://127.0.0.1:8000/dashboard**
If you changed the port or enabled TLS, use the new port/scheme instead.
Allow the server through your firewall on **Private networks only**, if prompted.
Do not enable router port forwarding.

## 4. Connect your phone
Put both devices on the same normal Wi-Fi, not a guest network with isolation.
Scan the dashboard QR with your phone camera and open the link. It pairs automatically.
Alternatively type the LAN address printed in the terminal, then enter the dashboard
PIN. Tap **Choose files**, select your files, and keep the page open until **Delivered**.
Tap **Take a photo** to capture a new image; tap **Send text or link** to share a note.

## 5. Find your files
Use **Open folder** in the PC dashboard or open `received/` inside the extracted
project. Files are organized into photos, videos, documents, and other.
The unique prefix on each filename prevents overwrites. Dashboard Download restores
the original filename. Image previews, protect/unprotect, and delete are available.

> **Do not skip this:** unprotected files are permanently removed after **7 days**.
> Click **Settings** and set retention to **0** to disable, or protect important files.
> Keep a separate backup. Cleanup does not move files to the Recycle Bin.

## Android share-menu integration (optional)
Basic HTTP uploads above do not require app installation. To see LocalDrop in the
Android share menu, follow **docs/HTTPS.md** to use trusted HTTPS, open LocalDrop in
a supported Android browser (typically Chrome), install it, and open it once. Then
select photos in Gallery → Share → LocalDrop. This is a PWA, not an APK.

## Stop and restart
Press **Ctrl+C** in the server terminal. Run the same launcher to restart.
Interrupted browser uploads resume from committed chunks while the original blobs
remain in that browser's queue. Clear data only when you intend to discard the queue.

For connection problems, see **docs/TROUBLESHOOTING.md**.
