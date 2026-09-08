# TPU button diaphragm test set

Purpose: compare printed 95A TPU flexibility for ARM/PULL and P504 before committing to final faceplate boots. These are standalone bench coupons, not drop-in sealed caps. No existing faceplate, enclosure, or PCB has been modified.

## First print

Start with `ARM_PULL_TPU_WEB_0.6mm.stl` in TPU and **two copies** of `ARM_PULL_CLAMP_FRAME_RIGID.stl` in rigid filament. Print the TPU flat as exported: smooth continuous skin on the bed, raised central actuator-contact pad upward. Suggested experimental layer height is 0.2 mm, giving 2/3/4 layers for the 0.4/0.6/0.8 mm webs. Inspect the slicer to ensure the skin is fully filled with no gaps; use a conservative profile appropriate to the actual TPU. Ordinary TPU feeds from the A1 external spool, not AMS Lite. Follow filament-maker drying guidance.

Clamp the 1.2 mm thick outer flange between the two matching rigid frames using four M3 bolts, washers and nuts. M3 x 12 mm is a starting candidate; confirm engagement with your washers/nuts. Tighten evenly without distorting the flange. Hole centres are (4,4), (40,4), (4,34), (40,34) mm; holes are 3.4 mm. Overall coupon is 44 x 38 mm. Frames are 3 mm thick, with flat flange contact. This fixture is independent of the actual panel mounting holes; do not drill your faceplate to this pattern.

ARM/PULL uses a 15.2 x 10 mm central reinforcement and 26 x 20 mm frame opening. P504 uses an 18 mm cross reinforcement and 26 mm circular opening. Both have a 1 mm added central thickness on the actuator side; no switch socket is provided. Use the matching frame style. The central pad faces the actuator in eventual use, opposite the user's finger. Flat webs are an initial compliance experiment; final boots may need a formed fold or dome for lower force.

## Compare

- Press centrally, then near each edge; compare 0.4, 0.6 and 0.8 mm samples.
- Check that the membrane returns completely, does not rub the frame, and does not crack or whiten around the reinforcement.
- For P504, compare all four directions and centre pressing; without a supported coupling this does not establish switch actuation.
- Record preferred feel, print defects and any permanent deformation after repeated pressing. Use consistent conditions to compare samples.
- After the PCB spacing is known, test with the real switches for required travel, operating force, return and absence of preload. TPU does not replace guided rigid plungers or the P504 shaft coupling.

Do not place a boot over the IDEC STOP actuator. These samples are not waterproof-qualified seals; layer integrity, flange compression, fatigue and actual assembled leakage remain unverified. The 44 x 38 mm fixture envelope is not the proposed final boot footprint and has not been checked against adjacent faceplate controls or OLED clearance.

Run `python mechanical/panel/tpu-prototypes/generate_tpu_prototypes.py` from the project root (requires manifold3d). All eight generated meshes passed solid-status, connected-body, positive-volume and open-bolt-hole checks. Test thicknesses represent candidates, not measured performance predictions.
