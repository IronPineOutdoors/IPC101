# Rev H2 correction note

Status: **REJECTED / DO NOT PRINT**

Rev H1 fixed the open underside and external corner nubs from Rev H, but its generic IPC-101-to-Alpha connector cassette created an awkward external box on the side of the enclosure.

Rev H2 removed that connector cassette and cleaned up the shell, but a second mounting-interface problem was then identified during review: the existing CrossWind mount uses **channels that the enclosure slides/fits into**. Rev H2 preserved only the general Rev G size / internal wood-screw pattern, not the full channel-engagement geometry. Therefore Rev H2 cannot be considered compatible with the existing mount.

## Lessons carried forward

- Keep the enclosure exterior clean.
- Keep the lower/underside shell closed.
- The existing **slide-channel mounting interface is REQUIRED geometry** and must be copied from the proven enclosure/mount relationship, not approximated from screw-hole locations.
- Preserve the exact docking/channel-engagement region first; redesign only the enclosure volume forward of that retained interface.
- Keep the PCB carrier/chassis as a separate internal part.
- Retain the current ~16.5 mm faceplate-back to PCB-top spacing only as a provisional design target.
- Do **not** create a connector opening until the actual IPC-101-to-Alpha connector is selected.
- Once selected, use a flush panel-mount cutout sized to the real connector.

Rev H, H1, and H2 are superseded. The next revision must begin from the proven channel-fitting enclosure geometry or the actual mounting-bracket CAD/measurements.
