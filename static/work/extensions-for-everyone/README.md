# Extensions for Everyone · Static HTML Slide Package

This directory is a self-contained production export of the HTML slide deck.

Open `index.html` directly in a browser, or open `00-extensions-for-everyone.html` to start the talk. Keyboard navigation is available on each slide: Right, Space, or PageDown moves forward; Left or PageUp moves backward; Home and End jump to the first and last slides.

## Package Layout

- `index.html`: slide index.
- `00-*.html` through `32-*.html`: flat top-level slide pages.
- `src/style.css`: shared slide styling.
- `src/deck.js`: keyboard navigation.
- `src/images/` and `src/generated/`: visual assets used by the deck.
- `src/vendor/`: bundled third-party browser libraries used by the terminal playback slide.
- `src/data/`: local terminal recording data used by slide 20.
- `pgext-galaxy.html` and `repository-download-stats.html`: flat embedded report pages used by slides 09 and 18.
- `src/pgext-galaxy/`: local runtime resources for the galaxy report page.
- `manifest.json`: flattened slide manifest.

## Slides

- 00. Extensions For Everyone
- 01. Who Am I
- 02. Extensibility Matters
- 03. Two Years Later
- 04. Who Benefits
- 05. Galaxy
- 06. Github Stars
- 07. Star Tiering
- 08. The Extension Funnel
- 09. Dimension Analysis
- 10. The Status Quo
- 11. The Trade Off
- 12. Why Linux Native
- 13. Pgext Cloud
- 14. Extension Catalog
- 15. Catalog Details
- 16. Catalog Page Views
- 17. Repository
- 18. Repo Download Stats
- 19. What We Can Still Infer
- 20. The Cli Pig
- 21. Dimension Explosion
- 22. Pg Minor Abi Break
- 23. Os Minor Break
- 24. Rust Problems
- 25. Bulky Extensions
- 26. Naming Conflicts
- 27. Library Conflicts
- 28. Api Break
- 29. Pg 19 Compatibility
- 30. Keeping It Maintainable
- 31. Three Questions
- 32. Thank You
