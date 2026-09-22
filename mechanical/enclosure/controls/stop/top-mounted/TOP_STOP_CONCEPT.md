# Integrated top STOP - packaging concept

User direction (2026-09-22): move the received IDEC XA1E-BV302R onto the top behind the sloped faceplate. Enclosure and/or faceplate may grow. The plywood/cardboard mock-up shape is not a styling constraint. Design should look intentional, with the red stop prominent. Preserve the working carrier and proven detachable mount where practical.

[Three-view concept](TOP_STOP_concept_preview.png). This is a packaging study, not a printable enclosure release or final industrial design. The preview uses older faceplate artwork solely as a geometric reference; the approved stacked tree and traced CrossWind artwork remain selected.

A flush installation at the existing top interferes with the original R3 carrier and cradle using the conservative 32 mm square, 33 mm rear-depth package established for the S1 pod. The tested top center is installed X78/Y10. These envelopes are deliberately larger than the nominal 27.9 mm manufacturer rear depth; the actual contact body, terminals and soldered leads still need physical checking.

The candidate has a rounded upper housing spanning the 174 mm enclosure width, with a gently sloped front transition. Its mounting surface is Z141 mm versus the existing shell maximum Z108.384 mm: an increase of 32.616 mm. Red operator and yellow collar are schematic for visual placement, not exact manufacturer CAD. A 2.5 mm top mounting land uses the previously accepted 16.3 mm keyed cutout dimensions.

The upper housing removes vertically before the front cassette is withdrawn. This avoids the removal obstruction found in the first fixed-roof trial. The base receives an internal 24 x 24 mm cable passage above the carrier. A 20 x 20 x 10 mm wire reserve clears the modeled base and stack. No change to the STOP circuit is proposed.

Checks in TOP_STOP_study.json: static shell/PCB/R3/cradle/bezel/faceplate clearance; conservative switch and wire envelopes; unchanged existing rear interface; 71 bracket slide positions; 66 cassette withdrawal positions with roof removed; 51 vertical roof/switch removal positions. These are rigid CAD envelopes and do not certify real harness motion or populated-board clearance.

Still required before print release: coherent exterior refinement beyond this first packaging form; upper-housing fasteners and locating features; gasket/seal strategy; real contact-block installation access, solder-joint routing and strain relief; physical switch clearance and operator/reset access. Roof is not yet fastened in this concept. Current I.1 and S1 print files remain unchanged.

Regenerate:

```powershell
python -B mechanical/enclosure/tooling/study_top_stop.py
python -B mechanical/enclosure/tooling/preview_top_stop.py
```
