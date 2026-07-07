# Public Boundary

This package intentionally contains only public aggregate artifacts:

- aggregate CSV and Markdown reports;
- generated figures;
- dataset and evaluation cards;
- release, citation, and reproducibility metadata.

This package intentionally excludes:

- upstream raw image payloads;
- local real-transfer photos and collection packs;
- source dataset archives;
- hosted-provider raw request/response dumps;
- provider caches;
- credential or account-authentication material.

This boundary is part of the benchmark design. It keeps the Kaggle package
auditable while avoiding redistribution of upstream raw data, private local
collection payloads, or provider-specific raw responses.
