# Trial seals (ADR ٦١) — OpenITI texts, reference-only, status: تجريبي

Each `*.gz` here is a verbatim copy of the OpenITI file named in `MANIFEST.tsv`, from the repository and commit
recorded there, gzip-compressed without a timestamp. The decompressed sha256 and size of each are recorded in
`tools/gen_trial_seals.py` and in `MANIFEST.tsv`; `python tools/gen_trial_seals.py --check` verifies them.

Licence: the OpenITI corpus release (version 2025.1.9, https://zenodo.org/records/17767721) is distributed under
**Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)**. Attribution: the OpenITI
corpus (KITAB project and partners); the underlying texts are (until ADR ١١٥ also Ibn Hishām's *Mughnī al-Labīb*, now in `corpora/kitab/`) al-Zarkashī's *al-Burhān fī
ʿUlūm al-Qurʾān*, al-Naḥḥās's *Iʿrāb al-Qurʾān* and al-ʿUkbarī's *al-Tibyān fī Iʿrāb al-Qurʾān*.

Owner's decision (2026-10-14, ADR ٦١): **trial** seals — usable only for preregistered measurement; they anchor nothing,
no judgement is built on them, and nothing in `gate/` reads them. Promotion to a final seal requires the owner's
signature. Nothing in this repository edits these files.

**ADR ١١٥ (2026-10-19):** *Mughnī al-Labīb* was promoted to a final seal by the owner's permission and moved to
`corpora/kitab/`; three texts remain here.
