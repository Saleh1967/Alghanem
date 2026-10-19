#!/usr/bin/env bash
# fold.sh — الطيُّ: كتابةُ **بنيةِ** المصدر المختوم في `folds/`، لا بايتاتِه.
#
# القاعدةُ التي لا تُخرَق: `folds/` تحمل البنيةَ لا البايتات. فكلُّ ما يُكتَب
# هنا أعدادٌ وأطوالٌ وأسماء — لا سطرَ نصٍّ واحدًا من المصدر. والفكُّ (unfold.sh)
# يجلب من جديدٍ ولا يخزِّن؛ فلا نسخةَ ثانيةً من البايتات تتخلّف في هذه الشجرة.
#
# والمعرِّفاتُ تُقرأ آليًّا من البيان نفسِه عبر `--list`، من الحقل الأوَّل حيث
# الحالُ «مختوم» — أي حيث الختمُ مقيس. لا قائمةَ يدويّةً هنا: القائمةُ اليدويّةُ
# نسخةٌ ثانيةٌ تتخلّف عن البيان بلا أن يُنذِر أحد.
#
# الأطوار:
#   --ids            عرضُ المعرِّفات المختومة كما قُرئت من البيان
#   --fold <معرِّف>   طيُّ بنيةِ مصدرٍ واحد
#   --fold-sealed    طيُّ بنيةِ كلِّ مختوم، مصدرًا مصدرًا بحكمٍ مفرَد
set -uo pipefail

HIFZ_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HAMIL_ROOT="${HAMIL_ROOT:-$(cd "$HIFZ_DIR/../.." && pwd)/hamil-hala-zaman-program}"
FETCH="$HAMIL_ROOT/fetch_source.sh"
FOLDS="${HIFZ_FOLDS:-$HIFZ_DIR/folds}"

E_USAGE=2
SEALED="مختوم"

say() { printf '%s\n' "$1" >&2; }

usage() {
  say "استعمالٌ: bash hifz/fold.sh --ids | --fold <معرِّف> | --fold-sealed"
  exit "$E_USAGE"
}

[ -f "$FETCH" ] || { say "صريخ: لا سكربتَ جلبٍ في $FETCH — يُعلَن بـHAMIL_ROOT"; exit "$E_USAGE"; }

# sealed_ids — المعرِّفاتُ المختومةُ مقروءةً من البيان آليًّا.
# سطرُ العناوين يُتخطّى، والحقلُ الثالثُ هو الحال، والأوّلُ هو المعرِّف.
sealed_ids() {
  bash "$FETCH" --list | awk -v sealed="$SEALED" 'NR > 1 && $3 == sealed { print $1 }'
}

fold_one() { # fold_one <معرِّف>
  local id="$1" path rc lines longest words chars
  path="$(bash "$HIFZ_DIR/unfold.sh" "$id")"
  rc=$?
  [ "$rc" = "0" ] || return "$rc"
  [ -f "$path" ] || { say "«$id» فُكَّ ولا ملفَّ في $path"; return 1; }

  # القياسُ بنيةٌ محضة: أعدادٌ وأطوال. ولا تُنسَخ بايتةٌ واحدةٌ إلى الطيّة.
  lines="$(wc -l < "$path" | tr -d ' ')"
  words="$(wc -w < "$path" | tr -d ' ')"
  chars="$(wc -m < "$path" 2>/dev/null | tr -d ' ')"
  longest="$(awk '{ n = length($0); if (n > m) m = n } END { print m + 0 }' "$path")"

  mkdir -p "$FOLDS"
  {
    printf '# طيّةُ «%s» — بنيةٌ لا بايتات. الفكُّ يجلب من جديدٍ ولا يخزِّن.\n' "$id"
    printf 'id\t%s\n' "$id"
    printf 'lines\t%s\n' "$lines"
    printf 'words\t%s\n' "$words"
    printf 'chars\t%s\n' "$chars"
    printf 'longest_line\t%s\n' "$longest"
  } > "$FOLDS/$id.fold"
  say "«$id» مطويٌّ بنيةً → $FOLDS/$id.fold"
  return 0
}

[ $# -ge 1 ] || usage
mode="$1"; shift

case "$mode" in
  --ids)
    sealed_ids
    ;;
  --fold)
    [ $# -eq 1 ] || usage
    case "$1" in --all) say "صريخ: لا --all — استعمِل --fold-sealed ليُحكَم على كلٍّ مفرَدًا"; exit "$E_USAGE" ;; esac
    fold_one "$1"
    exit $?
    ;;
  --fold-sealed)
    rc=0
    while IFS= read -r id; do
      [ -n "$id" ] || continue
      # كلُّ معرِّفٍ يُنادى وحدَه فيُعرَف حكمُه باسمه؛ وأعلى الأحكام يُرفَع.
      fold_one "$id" || { one=$?; [ "$one" -gt "$rc" ] && rc="$one"; }
    done < <(sealed_ids)
    exit "$rc"
    ;;
  -h|--help) usage ;;
  *) say "صريخ: طورٌ مجهول: $mode"; exit "$E_USAGE" ;;
esac
