"""Generate ARM and PULL bodies with matching flush two-color face labels."""
from enclosure_paths import asset
import argparse,shutil,subprocess
from pathlib import Path

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--openscad',default=shutil.which('openscad.com') or shutil.which('openscad'))
    args=parser.parse_args()
    if not args.openscad:parser.error('Specify --openscad PATH')
    root=Path(__file__).resolve().parent.parent
    for label in ('ARM','PULL'):
        for part,material in [('white','WHITE_PETGHF'),('black','BLACK_AMS')]:
            subprocess.run([args.openscad,'-o',str(asset(root, f'CrossWind_IPC101_{label}_Cap_R1_{material}.stl')),
                '-D',f'label="{label}"','-D',f'part="{part}"',str(asset(root, 'CrossWind_IPC101_Button_Caps_R1.scad'))],check=True)
