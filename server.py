#!/usr/bin/env python3
import argparse,logging,threading,webbrowser
from backend.config import Settings
from backend.app import create_app
from backend.core.qr_generator import terminal

def main():
    parser=argparse.ArgumentParser(description='LocalDrop — Scan. Share. Done.')
    parser.add_argument('--no-browser',action='store_true'); parser.add_argument('--port',type=int); parser.add_argument('--ip',help='Advertised LAN IP')
    args=parser.parse_args(); s=Settings()
    if args.port: s.port=args.port
    if args.ip: s.lan_ip=args.ip
    app=create_app(s);url=app.state.base_url
    logging.basicConfig(level=logging.INFO,format='%(asctime)s %(levelname)s %(message)s')
    print('\nLocalDrop 1.0 — Scan. Share. Done.\n')
    print('Phone: '+url+'/#pair='+app.state.security.identity['pair'])
    print('Pairing PIN: '+app.state.security.identity['pin'])
    terminal(url+'/#pair='+app.state.security.identity['pair'])
    scheme='https' if s.ssl_certfile else 'http'
    dashboard=f'{scheme}://127.0.0.1:{s.port}/dashboard'
    print('Dashboard: '+dashboard+'\nSaving to: '+str(s.save_dir))
    print(f'Retention: {s.retention_days} days (0 = disabled). Ctrl+C to stop.')
    if not s.ssl_certfile: print('HTTP mode: browser uploads work; installed PWA/share target needs trusted HTTPS. See docs/HTTPS.md.')
    if not args.no_browser and s.open_browser:
        threading.Timer(1.5,lambda:webbrowser.open(dashboard)).start()
    import uvicorn
    uvicorn.run(app,host=s.host,port=s.port,proxy_headers=False,ssl_certfile=str(s.base/s.ssl_certfile) if s.ssl_certfile else None,ssl_keyfile=str(s.base/s.ssl_keyfile) if s.ssl_keyfile else None)
if __name__=='__main__': main()
