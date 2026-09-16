# `corpora/` — موضعُ المدوَّنات، لا مستودعُ بايتاتها

**بايتاتُ المدوَّنات غيرُ منسوخةٍ إلى هذه الشجرة**، وإن كانت الرخصةُ تُجيز
النسخ. الشجرةُ تحفظ البصمةَ والطولَ والإسناد، ويُمرَّر موضعُ البايتات من
خارجها؛ ولهذا يُتجاهَل كلُّ `*.csv` في هذا المجلّد (انظر `.gitignore`).

## MASAQ

| الحقل | القيمة |
| --- | --- |
| البصمة (SHA‑256) | `d43d2a813afbe0490254bb26623d6041ed352a273d333e731ddbcda3bd0b6f3a` |
| طولُ البايتات | `20302008` |
| DOI | `10.17632/9yvrzxktmr.2` |
| الرخصة | `CC BY 3.0` |

نصُّ الإسناد — وهو **شرطُ رخصةٍ** لا لطفَ عبارة:

> MASAQ: Morphologically-Analyzed and Syntactically-Annotated Quran, Majdi
> Sawalha, University of Jordan, DOI 10.17632/9yvrzxktmr.2, licensed CC BY 3.0

### تمريرُ المسار

ضع `MASAQ.csv` حيث شئت — داخل هذا المجلّد أو خارجه — ثمّ صرِّح بمساره في
متغيّر البيئة `ALGHANEM_MASAQ_PATH`:

```bash
export ALGHANEM_MASAQ_PATH=/absolute/path/to/MASAQ.csv
python examples/arabic/rederive_masaq_witnesses.py
```

ولا يُخمَّن موضعُ الملفّ ولا يُقرأ من اسمٍ: تُرفَض البايتاتُ ما لم تطابق
البصمةَ والطولَ المُودَعَين معًا، فملفٌّ بالاسم نفسِه ليس هذا الملفَّ.
