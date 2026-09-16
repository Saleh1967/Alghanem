# corpora/ — vendored corpus bytes, and the attribution each one owes

A corpus file may sit here only when **its own licence permits redistribution**
and the attribution that licence requires is written below. Attribution is a
licence condition, not a courtesy (`AttributionIsAConditionNotACourtesy`), and
it is recorded here before any figure is issued from the bytes.

Corpora whose licences do **not** permit it are not vendored and never will be
from this directory: the Quranic Arabic Corpus (GPL) and the Tanzil text it
embeds (CC BY-ND) stay outside the tree, deposited by digest and byte length
only.

## MASAQ.csv

- **Corpus**: MASAQ — Morphologically-Analyzed and Syntactically-Annotated Quran
- **Author**: Majdi Sawalha, University of Jordan
- **DOI**: [10.17632/9yvrzxktmr.2](https://doi.org/10.17632/9yvrzxktmr.2)
- **Licence**: CC BY 3.0 — redistribution permitted with attribution
- **Expected byte length**: 20,302,008
- **Expected SHA-256**: `d43d2a813afbe0490254bb26623d6041ed352a273d333e731ddbcda3bd0b6f3a`

`src/alghanem/arabic/masaq_corpus_deposit.py` matches **both** the length and
the digest before it returns any figure. A file of the same name that differs
in either is another file and is refused, not read
(`AMirrorWithAnotherDigestIsNotTheseBytes`): a public mirror of byte length
18,650,409 and digest `777d0cc8…` re-derives the fourteen tag counts exactly and
diverges on all six byte-and-line figures, and its header lacks `Column5`.

Until `MASAQ.csv` is placed here, the path may still be passed in
`ALGHANEM_MASAQ_PATH`; the resolution order is the explicit argument, then that
variable, then this directory. No path is guessed when none of the three
resolves.

The bytes carry the Quran text, which is not this repository's to licence; the
deposit vendors an annotation of it under the terms its annotator published,
and adopts no claim from it.
