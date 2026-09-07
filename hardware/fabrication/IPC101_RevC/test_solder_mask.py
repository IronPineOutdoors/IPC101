"""Regression checks for the mask omission that caused the fabrication rejection."""
import contextlib
import io
from pathlib import Path
import sys
import tempfile
import unittest

import pcbnew
from validate_solder_mask import ROOT, validate
sys.path.insert(0, str(ROOT/'hardware/kicad'))
from generate_rev_c_pcb import restore_through_hole_mask_openings

BOARD = ROOT/'hardware/kicad/IPC101.kicad_pcb'
GERBERS = Path(__file__).with_name('gerbers')


class MaskRegressionTests(unittest.TestCase):
    def test_missing_source_layer_is_rejected_and_generator_restores_it(self):
        board = pcbnew.LoadBoard(str(BOARD))
        pad = next(iter(board.FindFootprintByReference('D1').Pads()))
        layers = pcbnew.LSET.AllCuMask()
        pad.SetLayerSet(layers)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'regression.kicad_pcb'
            pcbnew.SaveBoard(str(path), board)
            with self.assertRaisesRegex(ValueError, 'missing F.Mask'):
                validate(path)
            restore_through_hole_mask_openings(board)
            pcbnew.SaveBoard(str(path), board)
            with contextlib.redirect_stdout(io.StringIO()):
                validate(path)

    def test_empty_bottom_gerber_is_rejected(self):
        def read(name):
            if name.endswith('.gbs'):
                return b'%TF.FileFunction,Soldermask,Bot*%\n%FSLAX46Y46*%\n%MOMM*%\nM02*\n'
            return (GERBERS/name).read_bytes()
        with contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(ValueError, 'missing 29 solderable pad openings'):
                validate(BOARD, read)

    def test_corrected_exports_pass(self):
        with contextlib.redirect_stdout(io.StringIO()):
            validate(BOARD, lambda name: (GERBERS/name).read_bytes())


if __name__ == '__main__':
    unittest.main()
