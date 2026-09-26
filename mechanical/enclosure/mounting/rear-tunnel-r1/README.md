# Rear harness tunnel R1 ? fit prototype

> Export cleanup, 2026-09-26: superseded print links below are historical. Use `mechanical/enclosure/PRINT_THESE.md` for current parts. Source and Git history retain regeneration/recovery information.

[Three-view preview](REAR_TUNNEL_R1_preview.png) ? [CAD verification](REAR_TUNNEL_R1_verification.json)

The bracket now carries a stationary tunnel through the CrossWind alpha base's nominal 1/2-inch (12.7 mm) plywood wall. A removable rear collar overlaps the sleeve and sandwiches the wall. The enclosure retains its upward sliding mount and lifts away from the tunnel. The matching enclosure base closes the original bottom wiring port and adds a 52 mm rear opening; it retains the top STOP roof R1 attachment geometry.

## Confirmed design inputs

- User's existing 12-way DT-style pair: 41 mm wide, 22.16 mm high, approximately 73 mm long **when connected**. The user reports plenty of clearance through the printed 50 mm bore ring; retain the 50 mm bore. The rectangular cross-section diagonal is 46.605 mm.
- Three board branches total 11 positions: keypad 4, OLED 5, isolated STOP 2. One position remains spare; no pin assignment or wiring release is made here.
- Access inside the base requires removing the thrower deck. Routine disconnect must therefore be reachable from the front after undocking the control box.
- Roof locator coupons slide together well, per user. M3 x 30 clamp-up is untested because the user does not yet have screws that long.

## Bore fit confirmed

50 mm bore test ring (retired export; recover from Git history): 56 mm outside diameter, 50 mm clear bore, 6 mm thick. Print flat. Pass both unplugged connector halves through it with the latch untouched; also try the connected pair. It should pass without forcing or scraping. This tests cross-section only, not harness bend radius or removal motion.

**Physical feedback:** the user reports "plenty of clearance" through the printed ring. The connector passage fit is accepted; this does not verify the wired service loop during removal.

**Do not cut the plywood yet.** The proposed hole is 58 mm for a 56 mm sleeve, subject to actual wall thickness and a physical harness-motion mock-up. Next, trial-fit the bracket and collar and check the actual harness through the full slide-and-pull motion.

## Prototype parts

| Part | Print file | Notes |
|---|---|---|
| Bracket with tunnel | [Bracket](CrossWind_IPC101_Rear_Tunnel_Bracket_R1_PRINT.stl) | Replaces Rev H bracket; existing rail placement retained. Rail faces down in export; slicer supports are required beneath the plate and must not damage sliding faces. |
| Rear retaining collar | [Collar](CrossWind_IPC101_Rear_Tunnel_Collar_R1_PRINT.stl) | Flange down, sleeve upward. 56.6 mm socket overlaps the 56 mm tunnel. |
| Rear-entry enclosure base | [Base](CrossWind_IPC101_Rear_Tunnel_Base_R1_PRINT.stl) | Replaces the top STOP R1 base; old floor port and plate holes closed. Reuse the [R1 roof](../../controls/stop/top-mounted/TOP_STOP_R1.md). |
| Plywood layout stencil | [Template](CrossWind_IPC101_Rear_Tunnel_Wall_Template_R1_PRINT.stl) | 58 mm center opening and 50 x 50 mm screw-center pattern. Prototype dimensions only. |

The tunnel center is X78/Z50 in installed assembly coordinates, i.e. centered across the 140 mm bracket and 45 mm above its lower edge. The sleeve runs from Y-39 to Y-10.5, stopping 10.5 mm behind the enclosure rear plane. It does not enter or interlock with the moving box.

Nominal wall faces are Y-15 and Y-27.7. The rear collar bears at Y-27.7 and its flange is 4 mm thick. Four provisional M3 x 25 socket screws enter from inside the base, through the collar and wall into M3 nuts held in bracket-front hex pockets. Their 50 x 50 mm pattern is centered on the tunnel. Drill the four screw holes to provide clearance (modeled as 4 mm in plywood), not as threaded plywood holes. Load the nuts before installing the bracket. Retain the existing bracket mounting holes for enclosure loads; the collar screws clamp the passage. Recheck lengths if adding washers or a gasket.

The collar can slide along the sleeve before clamping, but the modeled assembly is checked only at nominal 12.7 mm wall thickness. Measure the actual wall and trial assemble before installing. A face gasket and rear opening seal remain to be designed; do not infer an ingress rating from the overlap.

## Service-loop layout and required physical check

1. During initial assembly, route the base-side harness through the tunnel. Put its strain relief deeper inside the base, leaving a free service loop between the anchor and connector. Establish loop length from the actual lift-and-pull motion; no numerical loop length has been validated.
2. Keep the connector behind the plywood while docked. The space between box and bracket is for flexible wires, not the 73 mm connector body.
3. To remove the box, release the pin and lift it approximately 70 mm. The harness must slide and bend freely while the rear opening moves upward past the fixed tunnel.
4. Once the rails disengage, bring the box forward and draw the connector through the tunnel, then unplug it from the front. Keep the base-side end accessible for reassembly.

**The unresolved fit is the wired bundle in the rear gap during the upward slide.** Rigid CAD clearance is not proof that wires will bend without pinching. Mock up the 10.5 mm tunnel-mouth-to-box spacing with the actual wire bundle; if it binds or requires a tight bend, revise the rear entry before a full enclosure print. Check internal board clearance and routing as well; the PCB model does not contain populated components.

## Verification

The generated report records 204 interference checks: nominal plywood and fasteners; centered connector passage; 71 box slide positions; 66 cassette positions; 51 roof positions. All eight STL exports are connected, watertight, consistently wound and fit a 256 mm cube.

The original bracket's retaining-pin bore was exactly tangent to a rail edge, producing a non-manifold STL seam. R1 adds 0.1 mm radial relief there (3.6 mm cutter versus 3.4 mm). All other rail geometry is checked against Rev H. Check the retaining pin on the printed bracket; this is not a load or retention qualification.

Regenerate:

```powershell
python -B mechanical/enclosure/tooling/generate_rear_tunnel_r1.py
python -B mechanical/enclosure/tooling/preview_rear_tunnel_r1.py
```
