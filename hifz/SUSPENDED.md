# معلَّق — hifz/

نُقلت وحداتُ هذا المجلّد إلى `suspended/hifz/` في 2026-10-05 (التاريخُ في git؛ لا حذف).

**السبب:** text-level pipeline bypassing the gate

**لا تعود وحدةٌ إلّا بثلاثة:** (1) مدخلُها ومخرجُها عبر `gate.api`، (2) اختباراتٌ مستقلّةٌ عن شيفرتها مطعَّمةٌ بالطفرة، (3) ADR مسجَّل.

السجلُّ الكامل: `SUSPENDED_REGISTRY.json`.


## الوحدات

- `hifz/.gitignore`
- `hifz/README.md`
- `hifz/fold.sh`
- `hifz/test_hifz.sh`
- `hifz/unfold.sh`
