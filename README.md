# LocalDrop
## Scan. Share. Done.
A complete local Wi-Fi file-transfer app: Python/FastAPI server, live PC dashboard,
mobile-first upload client, and installable PWA with a Web Share Target.

**Start here:** [QUICKSTART.md](QUICKSTART.md).

> **Important: files automatically delete after 7 days by default.** Protect a file
> in the dashboard, or set `retention_days` to `0` to disable deletion. Deletion is
> permanent, not a trip to the Recycle Bin. This is a transfer inbox, not a backup.

## Requirements
- PC: Python 3.10 or newer; Python 3.11–3.13 recommended, Windows/macOS/Linux.
- A current browser; PC and phone on the same trusted local network.
- Internet once to install dependencies; subsequent transfers need no internet.
- Optional: `mkcert` and a trusted CA certificate on the phone for HTTPS/PWA mode.
- No Node.js build, CDN, cloud server, account, or database server required.

## Quick launch
```sh
python setup.py
```
Then use the platform launcher:
- **Windows:** double-click `start.bat`, or `py -3 setup.py` then `.venv\Scripts\python server.py`.
- **macOS:** `python3 setup.py`, then `bash start.command`.
- **Linux:** `python3 setup.py`, then `bash start.sh`.

Setup creates an isolated `.venv`, installs all Python requirements, and copies
`config.example.json` to `config.json`. Launchers also run setup on first launch.
The PC dashboard opens at `http://127.0.0.1:8000/dashboard`. Scan its QR on your phone.
If setup reports that `venv` is unavailable, install your OS's Python venv package.

## Included features
- Real QR code in terminal and dashboard; LAN IP detection and manual override.
- Device pairing by QR secret or six-digit PIN; signed HttpOnly session cookie.
- Direct-to-disk **bounded-memory** upload chunks, 1 MiB from the client.
- Three concurrent **files**, ordered chunks per file (prevents assembly races).
- Durable server offsets in SQLite; resume across a PC server restart.
- SHA-256 deduplication; duplicates do not create another physical stored file.
- Browser IndexedDB queue; retries after 5, 15, 60 seconds, then manual retry.
- Background Sync integration where supported; foreground retries everywhere.
- Android Web Share Target via installed PWA and controlling service worker.
- Share text/URLs as a note file from Android, or directly to dashboard clipboard.
- Dark/light dashboard, live progress, real devices/stats, hourly activity chart.
- File search (latest 500), download, safe raster-image preview, protect/delete.
- Storage quota, file size limit, blocked executable extensions, host/origin guards.
- Hourly retention cleanup, storage summary, native notifications (best effort).
- Browser notification permission control, opt-in sound, open received folder.
- Setup/start scripts, HTTPS helper, optional Desktop shortcut and login autostart.
- API regression suite and real Chromium end-to-end smoke test.

## Two operating modes — read this first
| Feature | Plain HTTP over Wi-Fi | Trusted HTTPS on the phone |
|---|---|---|
| Scan QR, pair, select files, send | Yes | Yes |
| Dashboard and live progress | Yes | Yes |
| Retry while page stays open | Yes | Yes |
| Durable IndexedDB queue | Browser-dependent; fallback keeps files in tab | Yes, subject to quota/eviction |
| Service worker/offline shell | No on LAN HTTP | Yes |
| Installable PWA / Android share target | No | Supported browser + installed app required |
| Upload after closing app | No guarantee | No guarantee; OS/browser may suspend it |

Localhost on the PC is a special secure-context exception; that exception does not
make `http://192.168.x.x` on your phone secure. Merely clicking through a self-signed
certificate warning is not a reliable solution. See [docs/HTTPS.md](docs/HTTPS.md).
iOS browser upload works; this project does **not** provide an iOS native share extension.
It is a PWA, not an Android APK. Android share-sheet registration varies by browser/OS.

## Files and architecture
```
server.py / localdrop.py      Entrypoints
setup.py                     Install into .venv
start.bat / start.sh / start.command
config.example.json          Safe configuration template
backend/
  app.py / config.py          App factory, routes, network/Host/Origin guards
  api/                       Uploads, files, clipboard, pairing, stats, share fallback
  core/                      Storage, security, file manager, cleanup, QR, notification
  websocket/manager.py        Real-time event distribution
frontend/
  shared/                    Dependency-free CSS and DOM helpers
  dashboard/                 HTML, CSS, chart/QR/WebSocket/dashboard JS
  mobile/                    HTML, CSS, manifest, SW, uploader/retry engine, icons
scripts/                     HTTPS, optional shortcut, optional login autostart
tests/                       API tests and real-browser smoke test
data/                        Runtime SQLite, pairing identity, incomplete .part files
received/{photos,videos,documents,other}/
docs/                        HTTPS, API, security, troubleshooting, design notes
```
SQLite replaces the proposal's separate JSON state files to avoid torn writes and
make resumable offsets transactional. The shared `engine.js` owns upload, queue,
retry, and cancellation logic; there are no empty retry/uploader placeholders.
A lightweight asyncio scheduler replaces an extra APScheduler dependency.
Filename-derived categorization avoids libmagic's platform-specific setup.
Files use a random prefix to avoid collisions; original names remain in the UI.

## Configuration
Edit `config.json`; restart for network/path/limit/TLS changes. Retention and
notifications can also be saved from the dashboard without restart.

| Key | Default | Meaning |
|---|---|---|
| `host` / `port` | `0.0.0.0` / `8000` | Listener; never forward this port on your router |
| `lan_ip` | empty | Override auto-detected advertised LAN IPv4 address |
| `public_url` | empty | Optional LAN hostname URL for QR; certificate must cover it |
| `save_dir` | `received` | Relative to project folder, or an absolute folder |
| `max_file_bytes` | 5368709120 | 5 GiB maximum per file |
| `max_storage_bytes` | 53687091200 | 50 GiB, including reservations for incomplete uploads |
| `retention_days` | `7` | Permanently delete old unprotected originals; 0 disables |
| `cleanup_interval_seconds` | `3600` | Cleanup check interval |
| `block_executables` | `true` | Extension denylist, not malware scanning |
| `notifications` | `true` | Best-effort native PC notifications |
| `open_browser` | `true` | Auto-open PC dashboard |
| `ssl_certfile` / `ssl_keyfile` | empty | TLS file paths relative to project folder |

Start without opening a browser: `python server.py --no-browser` (inside `.venv`).
Override port/IP: `python server.py --port 8080 --ip 192.168.1.20`.
`LOCALDROP_HOME` can isolate runtime config/data/received into another directory;
static app assets always remain in the extracted project.
Use **one server process/worker**; multi-worker deployment is not supported.

## Security and important limits
Binding to `0.0.0.0` does not itself make a server local-only. This app explicitly
checks RFC1918/loopback/link-local/ULA peers and Host/Origin headers. Still use your
firewall; no router port forwarding, tunnels, public reverse proxies, or untrusted Wi-Fi.
The PC dashboard/admin session is loopback-only. Access it using `127.0.0.1` or
`localhost`, not the LAN address. Phones have access only to their own transfer history.
Clipboard text is shown on the dashboard and copied **only** when you click Copy;
we do not silently overwrite the operating system clipboard.

Do not execute untrusted uploads. Extension blocking is not content validation,
antivirus, or a sandbox. Never use this project as a public file-hosting service.
HTTP is unencrypted: use trusted HTTPS if other network users cannot be trusted.
Pairing codes are secrets. Share a QR only with authorized users.

See [docs/SECURITY.md](docs/SECURITY.md) for the threat model and reset procedure.

## Optional helpers
Run with the virtual environment Python:
```sh
python scripts/create-shortcut.py
python scripts/setup_https.py --ip 192.168.1.20
python scripts/autostart.py install
python scripts/autostart.py remove
```
Autostart is per-user **login**, not a system boot service. It is opt-in and does
not start immediately. Existing autostart files are never silently overwritten.
Desktop paths can differ on OneDrive/localized systems; create a manual shortcut if needed.

## Tests
```sh
python setup.py --dev
# Activate .venv first, or use its Python executable explicitly.
python -m pytest -q
python -m playwright install chromium
python tests/browser_smoke.py
```
On Linux, Chromium may need system libraries: use Playwright's documented
`python -m playwright install --with-deps chromium` with appropriate OS permissions.
The smoke test launches its own isolated temporary server/home; it does not alter
your real received files. No benchmark throughput is claimed.

## Technical honesty
Browser Background Sync is opportunistic; it is not a guaranteed background upload
service. Keep the app open for large files. Offline caches contain only static app
assets, not authenticated API responses. Offline mode can display the shell/retain
queued blobs but cannot transfer to a PC that is unreachable. Browser storage can
be denied, exhausted, or evicted. A tab-only fallback is clearly labeled.
SHA-256 verification runs before the success response; success means the file has
actually been finalized. Deduplication saves storage, not network bandwidth.
The raw upload body uses fixed-sized application buffers; memory usage is bounded,
not literally zero. Native share `formData()` may buffer/spool in the browser.
No claim of guaranteed instantaneous, zero-copy, or unlimited-speed transfer is made.

Release test results: [TEST_REPORT.md](TEST_REPORT.md).
Dependencies are installed from PyPI; this ZIP does not contain a virtual environment,
a precompiled executable, or an APK. See [THIRD_PARTY.md](THIRD_PARTY.md).
