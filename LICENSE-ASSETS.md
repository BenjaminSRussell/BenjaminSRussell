# License for the sheets, the copy and the README

Copyright (c) 2025–2026 Benjamin Russell.

The following are licensed under the **Creative Commons Attribution 4.0 International**
license (CC BY 4.0), <https://creativecommons.org/licenses/by/4.0/>:

- every SVG sheet the generator draws (`assets/**/*.svg` on `main` and `assets/v9/*.svg` on the
  `chart` branch) and the social preview PNGs under `social/`;
- the data files the sheets are drawn from (`assets/stats.json`, `assets/log.json`,
  `assets/layout.lock.json`, `assets/build-report.json`);
- the printed strings, notices, alt text and captions in `chart.toml`;
- the prose of `README.md` and `DESIGN.md`.

You may share and adapt them for any purpose, including commercially, provided you give
appropriate credit ("Benjamin Russell, github.com/BenjaminSRussell"), link to the license and
indicate if changes were made. No warranty is given.

The **code** that draws the sheets (`scripts/`, `tests/`, `.github/`) is under the MIT license in
[LICENSE](LICENSE). To draw your own chart, fork the repository, fill in `chart.toml` and run the
workflow; the sheets redraw from your repositories.

## Fonts

The typefaces in `scripts/fonts/` are not covered by either license above. Each is distributed
under the **SIL Open Font License, Version 1.1**, whose text is kept beside the font files:

- Instrument Serif (Regular, Italic) — Copyright 2022 The Instrument Serif Project Authors;
- IBM Plex Sans Condensed and IBM Plex Mono — Copyright © 2017 IBM Corp.

The OFL permits bundling subsets of these fonts inside the SVG sheets as outlines, which is how
they are used here. The Reserved Font Names "Instrument Serif" and "Plex" may not be used for
modified versions of the fonts.
