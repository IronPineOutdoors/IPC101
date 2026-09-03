# IPC-101 P0 Control Panel Layout

All coordinates are millimeters from the lower-left PCB corner, component/front view. **The 100 x 140 mm outline is PROVISIONAL.**

| Item | X | Y | Panel requirement / note |
|---|---:|---:|---|
| PCB outline | 0–100 | 0–140 | 1.6 mm FR-4 |
| Mount H1 | 5 | 5 | 3.2 mm hole, 6 mm keepout |
| Mount H2 | 95 | 5 | same |
| Mount H3 | 5 | 135 | same |
| Mount H4 | 95 | 135 | same |
| OLED region | centered above navigation | TBD | Hosyond B0G2RFLG1L; listed active area 55.01 x 27.49 mm, but cutout and holes require sample measurements |
| Navigation SW3 | 50 | 83 | verify sample; allow 24 x 24 finger zone |
| START SW1 | 28 | 55 | B3F-4055 center; cap-dependent opening |
| STOP operator | 72 | 55 | 22.3 mm nominal panel cutout; not PCB mounted |
| PULL SW2 | 50 | 25 | use large/high-contrast cap or overlay target |
| J1 ordinary UI | 50 | 5 | rear/bottom edge access; strain relief required |
| J3 STOP | 82 | 5 | rear; isolated two-wire routing |

Maintain 3 mm copper-to-edge clearance and 6 mm around mounting hardware. Reserve panel area above navigation for the larger display, but do not drill or cut it until the received module's PCB width/height, hole centers/diameters, active-area offset, header location, and maximum height have been measured. Target rear clearance is 15 mm plus connector/display cable bend radius. Maximum PCB-mounted height is provisionally 12 mm. The tactiles are not weather sealed.

Final panel work must verify cap travel/preload, OLED window and gasket, navigation footprint, anti-glare cover, fastener heads, connector access, and gloved reach. Front hierarchy is OLED, navigation, START/red STOP, then prominent PULL.
