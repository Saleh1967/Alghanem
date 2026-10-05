"""دعوى الإيداع في البيان لا تُكتَب إلّا والبايتاتُ حاضرةٌ في الشجرة.

هذا الاختبارُ مسنونٌ على **واقعةٍ وقعت**، لا على احتمالٍ مُتخيَّل: إيداعُ
`1ca5383` عنوانُه «‏Deposit MASAQ bytes in-tree: `corpora/MASAQ.csv` as a
sanctioned path»، ولم يحمل بايتةً واحدةً من المدوَّنة. فبقيت ثلاثةُ مواضعَ في
الشجرة تُخبِر أنّ البايتاتِ مُودَعةٌ وأنّ الأرقامَ العشرين تُعاد في CI بلا
تصريح، والملفُّ غيرُ موجودٍ أصلًا. ولم يُسقِط ذلك اختبارًا واحدًا، لأنّ
الاختباراتِ كلَّها كانت تقيس **الشيفرة** ولا تقيس **ما تقوله عن نفسها**.

وهذا ما يسدُّه هنا: عنوانُ الملفّ في الشجرة لا يكفي شاهدًا على حضوره، وجملةٌ
تُخبِر عن إيداعٍ دعوى قابلةٌ للتكذيب بوجود الملفّ أو غيابه. فما دام
`corpora/MASAQ.csv` غائبًا، تُمنَع الجملُ المُخبِرة عن حضوره.

وحدُّ هذا الاختبارِ مكتوبٌ فلا يُوسَّع بعدَه: لا يقرأ بايتاتِ المدوَّنة، ولا
يُعيد اشتقاقَ رقمٍ، ولا يحكم على صدق البصمة ولا الطول — تلك موضعُها
`read_masaq_bytes`. وهو يقيس المطابقةَ بين دعوًى مكتوبةٍ وواقعِ الشجرة، لا
غير. وحضورُ الملفّ يرفع المنع، ولا يجعل الدعوى صادقة: المطابقةُ على الطول
والبصمة تبقى شرطَ كلِّ رقم.
"""

from __future__ import annotations

from pathlib import Path

from alghanem.arabic.masaq_corpus_deposit import (
    MASAQ_RELATIVE_PATH,
    vendored_masaq_path,
)

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]

DECLARED_READMES = ("README.md", "corpora/README.md")
"""البيانانِ اللذان أخبرا عن الإيداع؛ مسنونانِ مُعدَّدانِ لا مُلتقَطانِ بمسح."""

EXAMPLES_DIRECTORY = "examples"
"""شجرةُ الأمثلة تُمسَح ولا يُسمّى فيها ملفٌّ بعينه.

والسببُ مقيس: سجلُّ المنجَز يَعُدّ المثالَ **مُشغَّلًا في شاهد** بمجرّد ورود
اسمه في ملفّ اختبار، وهو نصُّ `ExampleScriptReferenceIsNotExecution`. فتسميةُ
مثالٍ هنا تُصعِّد رتبتَه بلا تشغيل، فيُمسَح المجلَّد ولا يُسمّى.
"""

DEPOSIT_ASSERTING_PHRASES = (
    "bytes are deposited at",
    "bytes are deposited in",
    "its bytes are deposited",
    "the bytes are deposited",
    "البايتاتُ مُودَعةٌ في الشجرة",
    "مُودَعةٌ في الشجرة",
)
"""جملٌ تُخبِر عن حضورِ البايتات، لا عن سَنِّ موضعها؛ والفرقُ بينهما هو المقصود."""


def _read(relative_path: str) -> str:
    return (REPOSITORY_ROOT / relative_path).read_text(encoding="utf-8")


def _documents_that_may_assert_a_deposit() -> tuple[str, ...]:
    """البيانانِ المسنونانِ وكلُّ مثالٍ في الشجرة، مرتَّبةً بمساراتها."""

    examples = REPOSITORY_ROOT / EXAMPLES_DIRECTORY
    scripts = (
        sorted(
            path.relative_to(REPOSITORY_ROOT).as_posix()
            for path in examples.rglob("*.py")
        )
        if examples.is_dir()
        else []
    )
    return (*DECLARED_READMES, *scripts)


def test_no_document_asserts_a_deposit_the_tree_does_not_hold() -> None:
    """ما دامت البايتاتُ غائبةً، فلا جملةَ تُخبِر عن حضورها."""

    if vendored_masaq_path().is_file():
        return

    offences = [
        (relative_path, phrase)
        for relative_path in _documents_that_may_assert_a_deposit()
        for phrase in DEPOSIT_ASSERTING_PHRASES
        if phrase in _read(relative_path)
    ]
    assert offences == [], (
        f"`{MASAQ_RELATIVE_PATH}` غيرُ موجودٍ في الشجرة، ومع ذلك تُخبِر هذه "
        f"المواضعُ عن حضوره: {offences}. فإمّا أن تُودَع البايتاتُ، وإمّا أن "
        "تُصحَّح الجملة؛ ولا تُترَك دعوى إيداعٍ بلا مُودَع."
    )


def test_the_declared_readmes_exist_and_name_the_sanctioned_path() -> None:
    """البيانانِ قائمانِ ويُسمّيانِ الموضعَ المسنون، وإلّا فالاختبارُ يقيس عدمًا."""

    for relative_path in DECLARED_READMES:
        assert MASAQ_RELATIVE_PATH in _read(relative_path), relative_path


def test_the_examples_tree_is_swept_and_is_not_empty() -> None:
    """المسحُ يُصيب أمثلةً فعلًا؛ ومسحٌ يُرجِع فراغًا لا يمنع شيئًا."""

    swept = _documents_that_may_assert_a_deposit()
    assert len(swept) > len(DECLARED_READMES)
