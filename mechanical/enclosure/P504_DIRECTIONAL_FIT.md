# P504 directional restriction — 2026-09-22

The user reports center/select works but directional movement is blocked in the printed faceplate. N1.3 still has the inherited 6.2 mm aperture; earlier Rev C used 8 mm with a 5 mm cap hub. That earlier clearance is a starting point, not proof that it fits the currently installed cap or pedestal.

**Hold the next full faceplate print until directional travel is checked.** First establish whether the bare stick moves normally with the printed thumb cap removed. If it does, inspect cap/hub contact with the opening or cap underside contact with the panel. If the bare stick is also restricted, investigate rear seating/pedestal/switch restriction rather than assuming a larger opening solves it. Do not force movement.

The [8 mm P504 clearance coupon](CrossWind_IPC101_P504_Clearance_R1_8mm_PRINT.stl) is a 30 x 30 x 4.8 mm piece with the same 2 mm plate and exact N1.3 rear cradle, marked P504-R1 on the rear. Print front down as exported, then fit the actual switch, pedestal/sleeve and cap as used on the panel. Check all four directions, center/select and return. Report whether movement is free with and without the cap. The coupon is not an adapter installed on top of the existing faceplate.

The 8 mm opening adds 0.9 mm radial clearance over the old hole. Only the front aperture and hidden coupon mark change; the rear cradle is preserved. This test is reversible and avoids committing another whole faceplate to an unverified diameter. A larger aperture alone will not fix a cap seated too deeply, a trapped sleeve, or an overconstrained switch body.

Source: `generate_p504_clearance_r1.py`. `P504_clearance_R1_verification.json` records mesh validity, open aperture and preserved cradle. These CAD checks do not establish actual directional movement. No replacement full faceplate geometry is released by this coupon.
