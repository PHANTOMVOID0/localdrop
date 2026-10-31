# LocalDrop 1.0 — verification report

## Environment
- Linux x86_64, Python 3.12, real Chromium via Playwright.
- Validated both the development environment and a newly created `.venv` installed
  through the delivered `python setup.py --dev` script.
- Exact clean-install package versions are listed in docs/TESTED_DEPENDENCIES.txt.

## Results
- **36 API/security regression cases passed.**
- **Real Chromium desktop/mobile-emulated end-to-end test passed.**
- Python compilation, JavaScript syntax, and Bash launcher syntax checks passed.
- No browser JavaScript page errors during the tested workflow.
- Desktop and phone-width screenshots were inspected during development.
- ZIP integrity and a re-extracted source-tree regression run are checked before handoff.

## API coverage
Static assets and real QR bytes; upload/download; file categorization; committed
chunk offsets; offset mismatch; server restart/resume; oversized chunk rollback;
empty files; SHA-256 dedup and repeat finalization; executable extension block;
traversal/Windows reserved name sanitization; long Unicode filenames; size/quota
reservation; signed-session authentication; bad PIN and pairing rate limit;
other-device isolation; loopback admin restriction; Origin/Host/CSRF checks;
public-network rejection; protection/retention cleanup; duplicate invalidation;
disabled retention; preservation of unmanaged files; clipboard; cancellation;
settings persistence; tampered cookie rejection; share fallback; WebSocket events
and foreign-Origin rejection; IPv4/IPv6 local-network allowlist.

## Browser coverage
Actual server startup; dashboard login; QR rendering; independent phone pairing;
file picker upload; live dashboard updates; phone-to-PC text sharing; service-worker
POST share interception and IndexedDB queue; offline app shell and retained blob;
reconnection recovery; multi-chunk file upload; three concurrent files; settings;
filename HTML/XSS safety; mobile horizontal-overflow assertion.

## Not physically tested here
- Android system share-sheet registration on a real device.
- Certificate-authority installation on a phone and mkcert installation/trust flow.
- Windows/macOS execution, their desktop notifications, file managers, and login autostart.
- iOS browser variations, OS camera UI, actual camera capture, or user-specific firewall rules.
- Maximum 5 GiB transfers, throughput benchmarks, power-loss durability, browser quota
  exhaustion behavior on every platform, or every background-suspension scenario.

The included share-target browser test exercises service-worker handling, not a claim
that a real Android share sheet was tested. The offline test uses localhost's secure
context; real phones must use trusted HTTPS for the same PWA features. Native desktop
notifications were disabled during automated testing. This is tested source code, not
a security audit or a guarantee across all operating systems. Browser Background Sync
and closed-app uploads remain best effort.

One non-failing upstream warning appears with the clean-install dependency set:
Starlette warns that its HTTPX TestClient adapter is deprecated in favor of HTTPX2.
The delivered tests still pass; production upload requests do not use that adapter.
