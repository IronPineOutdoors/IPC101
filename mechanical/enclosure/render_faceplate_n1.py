"""Render both matching N1 materials using OpenSCAD (tested with 2021.01)."""
import argparse
import shutil
import subprocess
from pathlib import Path

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--openscad',default=shutil.which('openscad.com') or shutil.which('openscad'))
    args=parser.parse_args()
    if not args.openscad:parser.error('Specify --openscad PATH to the OpenSCAD command-line executable')
    root=Path(__file__).resolve().parent
    for part,material in [('white','WHITE_PETGHF'),('black','BLACK_AMS')]:
        subprocess.run([args.openscad,'-o',str(root/f'CrossWind_IPC101_Faceplate_RevN1_{material}.stl'),
                        '-D',f'part="{part}"',str(root/'CrossWind_IPC101_Faceplate_RevN1.scad')],check=True)
