# Archive - superseded IPC-101 enclosure development

> Historical design: superseded print exports were removed on 2026-09-26. Use `mechanical/enclosure/PRINT_THESE.md` for the current assembly; recover historical exports from Git or regenerate them.


**NOT FOR CURRENT PRINTING.** Use [PRINT THESE](../PRINT_THESE.md).

| Folder / file | Contents | Status |
|---|---|---|
| [superseded-rev-g](superseded-rev-g/) | Rev G box STLs and dimensions | Superseded enclosure/mounting approach |
| [exploratory-h-h1-h2](exploratory-h-h1-h2/) | Exploratory H/H1/H2 SCAD models and correction notes | Superseded experiments; never the authoritative Rev H T-rail baseline |
| [superseded-rev-i](superseded-rev-i/) | Initial Rev I box/carrier STLs and preview | Superseded by R3-compatible I.1; the archived box includes the front-opening correction |
| [DEVELOPMENT_HISTORY.md](DEVELOPMENT_HISTORY.md) | Earlier combined enclosure README | Historical decisions, measurements, limitations and revision notes |

Artifacts were moved without changing their geometry. Rejected intermediate versions that were already replaced before this cleanup remain recoverable from Git history. This archive is not evidence of physical validation.

The original R3, M.4 faceplate, authoritative Rev H mounting baseline and current I.1 parts remain in the parent folder. Older Python helpers also remain there because the current build imports them. Historical Rev G and Rev I regeneration now writes into the corresponding archive folders, keeping superseded print outputs out of the current folder. Rev H remains unchanged.
