#!/usr/bin/env bash
# مدخلُ التشغيل الواحد: يستدعي فحوصَ tools/checks.tsv نفسَها محليًّا وفي CI.
#
#   bash tools/run_checks.sh                 # كلُّ الفحوص، ويستمرّ بعد الفاشل
#   bash tools/run_checks.sh --fail-fast     # يقف عند أوّل فشل، والباقي NOT_RUN
#   bash tools/run_checks.sh --strict        # التخطّي خروجٌ غيرُ صفريّ (CI)
#   bash tools/run_checks.sh --only ruff-check,mypy
#   bash tools/run_checks.sh --list
#
# يكتب لكلِّ فحصٍ سجلًّا ورمزَ خروجٍ ومدّةً في دليل السجلّات، مع بصمةِ البيئة
# والـSHA في environment.txt، ليُنسَب السجلُّ إلى النسخة التي اختُبرت لا إلى غيرها.
set -u -o pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
manifest="$repo_root/tools/checks.tsv"
logs_dir="${ALGHANEM_CHECK_LOGS:-$repo_root/.check-logs}"
fail_fast=0
strict=0
list_only=0
selection=""

usage() {
    sed -n '2,13p' "${BASH_SOURCE[0]}"
}

while [ "$#" -gt 0 ]; do
    case "$1" in
        --manifest) manifest="$2"; shift 2 ;;
        --logs) logs_dir="$2"; shift 2 ;;
        --only) selection="$2"; shift 2 ;;
        --fail-fast) fail_fast=1; shift ;;
        --strict) strict=1; shift ;;
        --list) list_only=1; shift ;;
        -h|--help) usage; exit 0 ;;
        *) echo "run_checks: وسيطٌ غيرُ معروف: $1" >&2; usage >&2; exit 2 ;;
    esac
done

if [ ! -f "$manifest" ]; then
    echo "run_checks: لا مانيفست في $manifest" >&2
    exit 2
fi

names=()
requires=()
commands=()
while IFS=$'\t' read -r name requirement command || [ -n "${name:-}" ]; do
    case "$name" in ''|'#'*) continue ;; esac
    if [ -z "${command:-}" ]; then
        echo "run_checks: سطرٌ ناقصُ الأعمدة في المانيفست: $name" >&2
        exit 2
    fi
    if [ -n "$selection" ]; then
        case ",$selection," in *",$name,"*) ;; *) continue ;; esac
    fi
    names+=("$name")
    requires+=("$requirement")
    commands+=("$command")
done < "$manifest"

if [ "${#names[@]}" -eq 0 ]; then
    echo "run_checks: لا فحصَ مختارًا" >&2
    exit 2
fi

if [ "$list_only" -eq 1 ]; then
    printf '%s\n' "${names[@]}"
    exit 0
fi

mkdir -p "$logs_dir"
summary="$logs_dir/summary.tsv"
printf 'check\tstatus\texit_code\tseconds\tnote\n' > "$summary"

{
    echo "head_sha: $(git -C "$repo_root" rev-parse HEAD 2>/dev/null || echo unknown)"
    echo "tree_is_clean: $([ -z "$(git -C "$repo_root" status --porcelain 2>/dev/null)" ] && echo yes || echo no)"
    echo "started_utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "python: $(python -VV 2>&1 | tr '\n' ' ')"
    python - <<'PY'
import locale
import platform
import sys
import unicodedata

print(f"unicodedata: {unicodedata.unidata_version}")
print(f"maxunicode: {sys.maxunicode}")
print(f"filesystem_encoding: {sys.getfilesystemencoding()}")
print(f"stdout_encoding: {sys.stdout.encoding}")
print(f"preferred_encoding: {locale.getpreferredencoding(False)}")
print(f"platform: {platform.platform()}")
PY
    echo "locale_env: LANG=${LANG:-unset} LC_ALL=${LC_ALL:-unset}"
    echo "--- installed distributions ---"
    python -m pip freeze 2>/dev/null || echo "pip freeze unavailable"
} > "$logs_dir/environment.txt" 2>&1
echo "بيئةُ التشغيل مسجَّلةٌ في $logs_dir/environment.txt"

failed=0
skipped=0
index=0
while [ "$index" -lt "${#names[@]}" ]; do
    name="${names[$index]}"
    requirement="${requires[$index]}"
    command="${commands[$index]}"
    log="$logs_dir/$name.log"
    index=$((index + 1))

    if [ "$failed" -ne 0 ] && [ "$fail_fast" -eq 1 ]; then
        printf '%s\tNOT_RUN\t-\t-\t%s\n' "$name" "لم يُبلَغ بعد فشلٍ سابق" >> "$summary"
        echo "NOT_RUN  $name"
        continue
    fi

    if [ "$requirement" != "-" ] && [ -z "${!requirement:-}" ]; then
        printf '%s\tSKIPPED\t-\t-\t%s\n' "$name" "$requirement غيرُ مضبوط" >> "$summary"
        echo "SKIPPED  $name ($requirement غيرُ مضبوط)"
        skipped=$((skipped + 1))
        continue
    fi

    echo "RUN      $name: $command"
    started="$(date +%s)"
    # pipefail داخلَ الصَدَفة الفرعيّة أيضًا، فلا يبتلع tee رمزَ خروج الأمر قبله.
    bash -c "set -o pipefail; $command" 2>&1 | tee "$log"
    code="$?"
    seconds="$(( $(date +%s) - started ))"

    if [ "$code" -eq 0 ]; then
        printf '%s\tPASS\t0\t%s\t-\n' "$name" "$seconds" >> "$summary"
        echo "PASS     $name (${seconds}s)"
    else
        printf '%s\tFAIL\t%s\t%s\t-\n' "$name" "$code" "$seconds" >> "$summary"
        echo "FAIL     $name (رمز الخروج $code، ${seconds}s)"
        failed=$((failed + 1))
    fi
done

echo
echo "خلاصةُ الفحوص ($logs_dir/summary.tsv):"
column -t -s $'\t' "$summary" 2>/dev/null || cat "$summary"

if [ "$failed" -ne 0 ]; then
    echo "النتيجة: $failed فحصًا فاشلًا." >&2
    exit 1
fi
if [ "$skipped" -ne 0 ]; then
    if [ "$strict" -eq 1 ]; then
        echo "النتيجة: $skipped فحصًا متخطّى، و--strict لا يقرأ التخطّي نجاحًا." >&2
        exit 1
    fi
    echo "النتيجة: لا فشلَ، لكنّ $skipped فحصًا لم يُشغَّل لغياب شرطه؛ ليس نجاحًا كاملًا."
    exit 0
fi
echo "النتيجة: كلُّ الفحوص المختارة نجحت."
