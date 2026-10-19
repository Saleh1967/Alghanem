# Kitab seals (ADR ٦٨) — OpenITI texts, status: مختوم (owner's permission, 2026-10-15)

Each `*.gz` here is a verbatim copy of the OpenITI file named in `MANIFEST.tsv`, from the repository and commit recorded
there, gzip-compressed without a timestamp. The decompressed sha256 and size of each are recorded in `tools/gen_kitab.py`
and in `MANIFEST.tsv`; `python tools/gen_kitab.py --check` verifies them.

Licence: the OpenITI corpus is distributed under **Creative Commons Attribution-NonCommercial-ShareAlike 4.0
International (CC BY-NC-SA 4.0)**. Attribution: the OpenITI corpus (KITAB project and partners); the underlying texts are
Sībawayh's *al-Kitāb* (two digitisations, JK006989 and Shamela0023018) and Abū Saʿīd al-Sīrāfī's *Sharḥ Kitāb Sībawayh*
(Sham19Y0017726).

Use: anchors for the rows of `formal/a116/A116/Makharij.lean`, checked by `tests/test_makharij.py`. Al-Sīrāfī's commentary
is used only where it quotes the Kitāb after «قال سيبويه»; it is the commentator's transmission of the text, not a
manuscript of the Kitāb. Nothing in `gate/` reads these files. Nothing in this repository edits them.

**Added under ADR ١١٥ (owner's permission in session, 2026-10-19 02:40 Amman time: «موافق اختم البيب ختم نهائي وحمل قطر الندى
واختمه»):** Ibn Hishām's *Mughnī al-Labīb* (Shamela0006972, promoted from the trial seal of ADR ٦١ with the same sha256) and
Ibn Hishām's *Matn Qaṭr al-Nadā* (Shamela0011376), both from OpenITI/0775AH at commit 61b0c789; same licence and use rules.
