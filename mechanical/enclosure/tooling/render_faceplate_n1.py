"""Render both matching N1 materials using OpenSCAD (tested with 2021.01)."""
from enclosure_paths import asset
import argparse
import shutil
import subprocess
from pathlib import Path

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--openscad',default=shutil.which('openscad.com') or shutil.which('openscad'))
    parser.add_argument('--revision',choices=['N1','N11','N12','N13','N14'],default='N1')
    args=parser.parse_args()
    if not args.openscad:parser.error('Specify --openscad PATH to the OpenSCAD command-line executable')
    root=Path(__file__).resolve().parent.parent
    for part,material in [('white','WHITE_PETGHF'),('black','BLACK_AMS')]:
        subprocess.run([args.openscad,'-o',str(asset(root, f'CrossWind_IPC101_Faceplate_Rev{args.revision}_{material}.stl')),
                        '-D',f'part="{part}"',str(asset(root, f'CrossWind_IPC101_Faceplate_Rev{args.revision}.scad'))],check=True)
