#!/usr/bin/env bash
# test_hifz.sh — مصادمةُ المستدعي بعقد البيت المستدعى، **بلا شبكةٍ قطعًا**.
#
# لا يُستنسَخ هنا OpenITI ولا يُبنى مختبرُ git: يُصطنَع `fetch_source.sh` في
# مجلَّدٍ مؤقَّتٍ تحت /tmp يُخرج ما يُؤمَر به من المخارج الخمسة، فتُصادَم قسمةُ
# الأحكام وحدَها. والشبكةُ ليست عقدًا فلا تُمتحَن.
set -uo pipefail

HIFZ_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB="$(mktemp -d "${TMPDIR:-/tmp}/hifz-test.XXXXXX")"
trap 'rm -rf "$LAB"' EXIT

pass=0; fail=0
ok()   { pass=$((pass + 1)); printf '  ✓ %s\n' "$1"; }
bad()  { fail=$((fail + 1)); printf '  ✗ %s\n' "$1"; }
claim() { # claim <وصف> <منتظَر> <واقع>
  if [ "$2" = "$3" ]; then ok "$1"; else bad "$1 — منتظَرٌ «$2» وواقعٌ «$3»"; fi
}

# ــ البيتُ المصطنَع ــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ
# سكربتُه في الجذر تمامًا كالحقيقيّ: HAMIL_ROOT/fetch_source.sh لا SOURCES/.
HOUSE="$LAB/hamil-hala-zaman-program"
mkdir -p "$HOUSE"
cat > "$HOUSE/fetch_source.sh" <<'STUB'
#!/usr/bin/env bash
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
printf '%s\n' "$*" >> "$ROOT/calls.log"
case "${1:-}" in
  --list)
    printf '%-18s %-16s %-8s %s\n' "المعرِّف" "المستودع" "الحال" "الملحوظة"
    printf '%-18s %-16s %-8s %s\n' "ibnmalik_alfiyya" "OpenITI/0675AH" "مختوم" "ابن_مالك_الألفية"
    printf '%-18s %-16s %-8s %s\n' "nahhas_icrab_sham" "OpenITI/0350AH" "مختوم" "النحاس_إعراب_القرآن"
    printf '%-18s %-16s %-8s %s\n' "ibnjinni_muluki" "-" "معذور" "لا_أثرَ_له"
    printf '%-18s %-16s %-8s %s\n' "qatr_pending" "OpenITI/0775AH" "مرشَّح" "لم_يُختَم_بعد"
    exit 0 ;;
  --fetch) ;;
  *) echo "طورٌ مجهول" >&2; exit 2 ;;
esac
id="${2:-}"
rc="$(cat "$ROOT/rc" 2>/dev/null || echo 0)"
if [ "$rc" = "0" ]; then
  dest="${SOURCES_DIR:?SOURCES_DIR لم يُمرَّر}/$id.txt"
  mkdir -p "$(dirname "$dest")"
  printf 'الحمد\nلله رب العالمين\n' > "$dest"
  echo "$id مطابقُ الختم ✓ → $dest (deadbeef)"
  exit 0
fi
echo "حكمٌ مصطنَعٌ $rc لـ$id" >&2
exit "$rc"
STUB
chmod +x "$HOUSE/fetch_source.sh"

# بيانٌ مصطنَعٌ بحقوله العشرة: منه يُقرأ موضعُ البايتات — لا من سطرٍ مطبوع.
mkdir -p "$HOUSE/corpora/inbox"
printf 'وضعه المالكُ بيده\n' > "$HOUSE/corpora/inbox/محلّيّ.txt"
{
  printf '#id\trepo\tref\tpattern\tpath\tblob\tbytes\tsha256\tstate\tnote\n'
  printf 'ibnmalik_alfiyya\tOpenITI/0675AH\tmaster\t-\t-\tdead\t97798\tbeef\tمختوم\tالألفية\n'
  printf 'nahhas_icrab_sham\tOpenITI/0350AH\tmaster\t-\t-\tdead\t4170848\tbeef\tمختوم\tالإعراب\n'
  printf 'shakhsiyya_j1\tself\tb7abcad\t-\tج١.docx\tdead\t283112\tbeef\tمختوم\tمن_التاريخ\n'
  printf 'mahalli\tlocal\t-\t-\tمحلّيّ.txt\tdead\t30\tbeef\tمختوم\tبيد_المالك\n'
} > "$HOUSE/sources_manifest.tsv"

export HAMIL_ROOT="$HOUSE"
export SOURCES_DIR="$LAB/sources"
export SOURCES_CACHE="$LAB/cache"
export HIFZ_FOLDS="$LAB/folds"
export HIFZ_RETRIES=1

set_rc() { printf '%s' "$1" > "$HOUSE/rc"; }
calls()  { cat "$HOUSE/calls.log" 2>/dev/null || true; }
reset()  { : > "$HOUSE/calls.log"; rm -rf "$SOURCES_DIR" "$HIFZ_FOLDS"; }

# ــ الأحكامُ الأربعةُ لا «فشلٌ» واحد ــــــــــــــــــــــــــــــــــــــــــ
echo "الأحكامُ الخمسةُ تُفرَّق بالاسم:"
for rc in 0 1 2 3 4; do
  reset; set_rc "$rc"
  out="$(bash "$HIFZ_DIR/unfold.sh" ibnmalik_alfiyya 2>/dev/null)"; got=$?
  claim "المخرجُ $rc يُرفَع كما هو" "$rc" "$got"
  if [ "$rc" = "0" ]; then
    claim "النجاحُ يطبع مسارَ البايتات" "$SOURCES_DIR/ibnmalik_alfiyya.txt" "$out"
  fi
done

# التعذُّرُ وحدَه يُعاد: 1 يُنادى مرّتين (محاولةٌ وإعادةٌ واحدة)، و4 مرّةً واحدة.
reset; set_rc 1
bash "$HIFZ_DIR/unfold.sh" ibnmalik_alfiyya >/dev/null 2>&1
claim "التعذُّرُ يُعاد" "2" "$(calls | grep -c -- '--fetch')"

reset; set_rc 4
bash "$HIFZ_DIR/unfold.sh" ibnmalik_alfiyya >/dev/null 2>&1
claim "مخالفةُ الختم لا تُعاد" "1" "$(calls | grep -c -- '--fetch')"

reset; set_rc 3
bash "$HIFZ_DIR/unfold.sh" ibnmalik_alfiyya >/dev/null 2>&1
claim "البيانُ المعطوبُ لا يُعاد" "1" "$(calls | grep -c -- '--fetch')"

# ــ النداءُ بالمعرِّف وحدَه: لا --all ولا --fetch --all ــــــــــــــــــــــ
echo "النداءُ بالمعرِّف وحدَه:"
reset; set_rc 0
bash "$HIFZ_DIR/unfold.sh" nahhas_icrab_sham >/dev/null 2>&1
claim "النداءُ بالمعرِّف بحرفه" "--fetch nahhas_icrab_sham" "$(calls | grep -- '--fetch' | tail -n 1)"
claim "لا --all في نداءٍ قطّ" "0" "$(calls | grep -c -- '--all')"

bash "$HIFZ_DIR/unfold.sh" --all >/dev/null 2>&1
claim "--all يُردُّ خطأَ استعمالٍ عند المستدعي" "2" "$?"

bash "$HIFZ_DIR/unfold.sh" >/dev/null 2>&1
claim "النداءُ بلا معرِّفٍ خطأُ استعمال" "2" "$?"

HAMIL_ROOT="$LAB/لا-بيت" bash "$HIFZ_DIR/unfold.sh" ibnmalik_alfiyya >/dev/null 2>&1
claim "بيتٌ غائبٌ خطأُ استعمالٍ لا تعذُّرُ جلب" "2" "$?"

# ــ موضعُ البايتات من البيان لا من سطرٍ مطبوع ـــــــــــــــــــــــــــــــ
echo "الموضعُ يُقرأ من البيان:"
reset; set_rc 0
claim "البعيدُ يُودَع في SOURCES_DIR" "$SOURCES_DIR/ibnmalik_alfiyya.txt" \
  "$(bash "$HIFZ_DIR/unfold.sh" ibnmalik_alfiyya 2>/dev/null)"
claim "المحلّيُّ يبقى حيث وضعه المالك" "$HOUSE/corpora/inbox/محلّيّ.txt" \
  "$(bash "$HIFZ_DIR/unfold.sh" mahalli 2>/dev/null)"
bash "$HIFZ_DIR/unfold.sh" shakhsiyya_j1 >/dev/null 2>&1
claim "self لا يُسلِّم بايتاتٍ فلا يُطوى" "1" "$?"

# وهذا هو المقصد: صيغةُ السطر المطبوع زينةٌ لا عقدٌ، فتغيُّرُها لا يكسر شيئًا.
reset; set_rc 0
sed -i 's|echo "\$id مطابقُ الختم ✓ → \$dest (deadbeef)"|echo "تمّ: $id [$dest]"|' "$HOUSE/fetch_source.sh"
claim "تغيُّرُ صيغة السطر لا يزحزح الموضع" "$SOURCES_DIR/ibnmalik_alfiyya.txt" \
  "$(bash "$HIFZ_DIR/unfold.sh" ibnmalik_alfiyya 2>/dev/null)"

# ــ المعرِّفاتُ تُقرأ آليًّا من البيان، المختومُ وحدَه ــــــــــــــــــــــــ
echo "المعرِّفاتُ من البيان لا من قائمةٍ يدويّة:"
ids="$(bash "$HIFZ_DIR/fold.sh" --ids)"
claim "المختومان وحدَهما" "ibnmalik_alfiyya
nahhas_icrab_sham" "$ids"
claim "المعذورُ لا يُطوى" "0" "$(printf '%s\n' "$ids" | grep -c 'ibnjinni_muluki')"
claim "المرشَّحُ لا يُطوى" "0" "$(printf '%s\n' "$ids" | grep -c 'qatr_pending')"
claim "سطرُ العناوين لا يُعَدُّ معرِّفًا" "0" "$(printf '%s\n' "$ids" | grep -c 'المعرِّف')"

# ــ folds/ بنيةٌ لا بايتات ــــــــــــــــــــــــــــــــــــــــــــــــــــ
echo "الطيَّةُ بنيةٌ لا بايتات:"
reset; set_rc 0
bash "$HIFZ_DIR/fold.sh" --fold-sealed >/dev/null 2>&1
claim "طيّةٌ لكلِّ مختوم" "2" "$(ls "$HIFZ_FOLDS" 2>/dev/null | grep -c '\.fold$')"
claim "لا بايتةَ نصٍّ في الطيّة" "0" "$(grep -l 'العالمين' "$HIFZ_FOLDS"/*.fold 2>/dev/null | wc -l | tr -d ' ')"
claim "البنيةُ مقيسةٌ: سطران" "lines	2" "$(grep '^lines' "$HIFZ_FOLDS/ibnmalik_alfiyya.fold")"

# مخالفةُ الختم: لا يُطوى منها شيءٌ ألبتّة.
reset; set_rc 4
bash "$HIFZ_DIR/fold.sh" --fold ibnmalik_alfiyya >/dev/null 2>&1
claim "المخالفُ ختمَه يُرفَع حكمُه 4" "4" "$?"
claim "ولا يُطوى منه شيء" "0" "$(ls "$HIFZ_FOLDS" 2>/dev/null | wc -l | tr -d ' ')"

# ــ المخرجاتُ والذاكرةُ داخلَ Alghanem لا في بيت البايتات ــــــــــــــــــــ
# ــ المخرجاتُ والذاكرةُ داخلَ Alghanem لا في بيت البايتات ــــــــــــــــــــ
# (صندوقُ الوارد مهادٌ صنعتُه أنا هنا؛ المُدَّعى أنّ المستدعيَ لا يودِع مخرجاتِه
#  ولا ذاكرتَه هناك — وموضعُهما الافتراضيّ corpora/sources.)
echo "لا يكتب المستدعي في شجرةِ من يستدعيه:"
claim "لا مخرجاتٍ في بيت البايتات" "0" "$([ -e "$HOUSE/corpora/sources" ] && echo 1 || echo 0)"
claim "المخرجاتُ في شجرة Alghanem" "1" "$([ -d "$SOURCES_DIR" ] && echo 1 || echo 0)"

printf '\nالمصادمُ: %d موافقةً · %d مخالفةً\n' "$pass" "$fail"
[ "$fail" = "0" ] || exit 1
