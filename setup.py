#!/usr/bin/env python3
"""One-command environment setup (not a setuptools package)."""
import argparse,json,os,shutil,subprocess,sys,venv
from pathlib import Path
BASE=Path(__file__).resolve().parent

def main():
    parser=argparse.ArgumentParser(description='Install LocalDrop into a local virtual environment')
    parser.add_argument('--dev',action='store_true',help='Include test dependencies')
    parser.add_argument('--shortcut',action='store_true',help='Create a received-folder shortcut on Desktop')
    args=parser.parse_args()
    if sys.version_info<(3,10): raise SystemExit('Python 3.10 or newer is required. Python 3.11–3.13 is recommended.')
    env=BASE/'.venv';python=env/('Scripts/python.exe' if os.name=='nt' else 'bin/python')
    if not python.exists():
        print('Creating isolated Python environment…');venv.create(env,with_pip=True)
    subprocess.check_call([str(python),'-m','pip','install','--upgrade','pip'])
    subprocess.check_call([str(python),'-m','pip','install','-r',str(BASE/('requirements-dev.txt' if args.dev else 'requirements.txt'))])
    if not (BASE/'config.json').exists(): shutil.copyfile(BASE/'config.example.json',BASE/'config.json')
    settings=json.loads((BASE/'config.json').read_text());folder=(BASE/settings['save_dir']).resolve()
    for category in ['photos','videos','documents','other']: (folder/category).mkdir(parents=True,exist_ok=True)
    if args.shortcut: subprocess.check_call([str(python),str(BASE/'scripts/create-shortcut.py')])
    for name in ['start.sh','start.command']:
        try: (BASE/name).chmod(0o755)
        except OSError: pass
    print('\nReady. Windows: double-click start.bat | macOS: start.command | Linux: bash start.sh')
    print('Or run: '+str(python)+' server.py')
    print('Important: unprotected files auto-delete after 7 days; set retention_days to 0 to disable.')
if __name__=='__main__': main()
