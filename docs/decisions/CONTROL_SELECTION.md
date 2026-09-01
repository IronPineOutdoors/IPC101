# Control Selection Decision

## 12 mm tactile family selected

Omron B3F-4055 is selected for START and PULL: 12 x 12 mm through-hole body, projected plunger for caps, 260 gf, 1,000,000-cycle mechanical life, active lifecycle, and broad US distribution. The larger body and cap support are materially easier to locate with gloves than common 6 x 6 mm tactiles. The cost and 20–25 mm center spacing are acceptable on the provisional 100 mm panel.

Six-millimeter tactiles win on density and price but have smaller targets, shorter typical life in this family, and less stable panel feel. They are rejected for the two primary actions. STOP is intentionally not standardized: safety prominence and a maintained NC contact outweigh BOM uniformity.

## Five-way navigation selected

Adafruit Product 504 is selected over a rotary encoder. It maps manual LEFT/RIGHT directly, offers UP/DOWN adjustment and CENTER select in one through-hole control, costs about $1.95, and avoids ambiguous encoder rotation during manual motion. A rotary encoder is better for fast numeric adjustment but needs a shaft/knob, panel-bearing decision, three inputs, and different firmware semantics.

Product 504 is prototype-only because Adafruit supplies a similar-part (SKQUCAA010) datasheet rather than an exact manufacturer MPN. The project footprint is therefore a fabrication hold until compared to a received sample. If it differs, update only `SW3` footprint and panel datum; architecture is unchanged.

## STOP selected separately

Omron A22NE-M-PD01-N is the recommended 22 mm red push-lock/turn-reset emergency-stop operator with an NC contact. Final operator, contact-block suffix, panel thickness, boot/shroud, and safety classification must be verified at purchase and system risk review. P0 treats it as a panel-mounted wired device, not a PCB component.
