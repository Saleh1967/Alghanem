# فهرسُ عقد الشرح — كلُّ سطرٍ بدعواه ووسمه ومرساته من سجلّ الدعاوى

مولَّدٌ بـ`python tools/gen_sharh_index.py`؛ لا يُحرَّر باليد (ADR ٤٤). لكلّ صورةٍ من مودَع المصحف أسطرٌ (الدعوى، القيمة، الوحدة) من قرّاء السُّلَّم القائمين، ووسمُ السطر ومرساتُه وسمُ دعواه وسندُها في `status.LEDGER` بعينه — فلا سطرَ أقوى من سنده. لا نصَّ في العقد؛ والكلمةُ تخرج بـ`gate.exit` في الغانم (`tools/gen_sharh_text.py`).

18,179 صورةً على 78,207 موضعًا (والمواضعُ المرفوضةُ في البوّابة 38 لا أسطرَ لها)؛ أسطرٌ على المواضع: 679,490؛ خروقُ العقد: 0.

الوسومُ على المواضع: مبرهن 523,076 (77.0%)، مفحوص_استقصاء 156,414 (23.0%).

| الدعوى | الوسم | المرساة | أسطرٌ على الصور | أسطرٌ على المواضع |
|---|---|---|---:|---:|
| `TAWABI-case` | مبرهن | `lean:Slge.Tawabi.four_markers_one_case` | 18,179 | 78,207 |
| `MADD-lazim` | مبرهن | `lean:Slge.Madd.lazim_iff_not_binary` | 65 | 107 |
| `ILAL-samai` | مبرهن | `lean:Slge.Ilal.samai_closed` | 3 | 18 |
| `ILAL-descent` | مبرهن | `lean:Slge.Ilal.descend_ascends` | 1,088 | 5,952 |
| `MAQAYIS-member` | مبرهن | `lean:Slge.Maqayis.member_sound` | 15,298 | 48,735 |
| `WUJUD-partition` | مبرهن | `lean:Slge.Wujud.table_length` | 15,298 | 48,735 |
| `TAWZI-reader` | مبرهن | `lean:Slge.Tawzi.tawzi_restores` | 943 | 27,805 |
| `QIRAA-reader` | مبرهن | `lean:Slge.Qiraa.harf_no_hukm` | 18,635 | 97,065 |
| `HUKM-judge` | مبرهن | `lean:Slge.Hukm.hukm_none_iff` | 13,097 | 40,078 |
| `SAWABIQ-reader` | مبرهن | `lean:Slge.Sawabiq.sawabiq_restores` | 4,947 | 20,174 |
| `GRANT-mursam` | مبرهن | `lean:Slge.Grant.mursam_sound` | 18,114 | 78,100 |
| `ENTRY` | مفحوص_استقصاء | `test:tests/test_entry.py::test_kitabun_enters_as_five_cells_and_exits_byte_for_byte` | 18,179 | 78,207 |
| `CERT-n` | مفحوص_استقصاء | `test:tests/test_deposits.py::test_certificate_n_is_carried_whole` | 18,179 | 78,207 |
| `FOLD` | مبرهن | `lean:Slge.slgeFold_injective` | 18,114 | 78,100 |

## ما ليس هنا — باسمه

- رقمُ الآية سورةً وآيةً: لا جدولَ مختومًا لحدود السور، فالآيةُ برقم سطرها في المدوّنة المختومة.
- السطرُ يقول ما يقوله قارئُه على الصورة وحدَها: لا سياقَ جملةٍ ولا حسمَ بين القراءات.
