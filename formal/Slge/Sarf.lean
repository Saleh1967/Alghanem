import Slge.Marifa
import Slge.Wazn

/-!
# الممنوعُ من الصرف: جرُّه نصبُه، وشرطا صرفه عمليّتان

**القانونُ الحاسم** على الخانات: الممنوعُ من الصرف لا تنوينَ له، وجرُّه بالفتحة — أي أنّ صورةَ جرّه
**هي صورةُ نصبه بعينها** (`jarr_eq_nasb`)، بخلاف المنصرف الذي يفرّق الكسرُ والتنوينُ جرَّه من نصبه
(`sarf_jarr_ne_nasb`). و**شرطا الصرف** عمليّتان: أل (`Marifa.al`) والإضافةُ (`Marifa.idafa`)؛
وبعدهما الجرُّ بالكسرة كالمنصرف (`al_jarr_kasra`، `idafa_jarr_kasra`).

**العللُ** على نوعين: ما تقرؤه الخانة (علّةُ الصيغة) وما لا تقرؤه (علّةُ المعجم):
* **صيغةُ منتهى الجموع**: على قالبٍ من قوالب `Wazn.awzan` الاثني عشر؛ القراءةُ `onTemplate` سليمةٌ
  لكلّ أصل (`onTemplate_fill`).
* **ألفُ التأنيث المقصورة**: ألفٌ ساكنةٌ بعد فتحٍ رابعةً فأكثر (`maqsura`)؛ **الممدودة**: همزةٌ بعد ألفٍ
  ساكنةٍ بعد فتح (`mamduda`) — والهمزةُ الأصليّةُ (أَبْنَاء) لا تفرّقها الخانة: دَينٌ معجميّ مسمًّى.
* **فَعْلَان، أَفْعَل، فَعْلَاء، فُعْلَى**: قوالبُ من `awzan` كذلك.
* **العلمُ** (التأنيث، العجمة، التركيب، الألفُ والنون، وزنُ الفعل، العدل): معجمٌ لا خانة.

القياسُ على MASAQ (754 اسمًا بعد جارٍّ، بشهادات البوّابة) في بايثون: أل ⇒ كسر، إضافة ⇒ كسر، والمجرّدُ
منوَّنُ كسرٍ أو مفتوحٌ بلا تنوين (الممنوع).
-/

namespace Slge.Sarf

open Slge.Categories (c)
open Slge.Zuruf (setLast)

/-- المنصرفُ النكرة: جرُّه كسرٌ وتنوين، ونصبُه فتحٌ وتنوين. -/
def sarfJarr (w : List SCell) : List SCell := setLast w 1 ++ [c 25 3]
def sarfNasb (w : List SCell) : List SCell := setLast w 0 ++ [c 25 3]

/-- الممنوعُ: جرُّه ونصبُه فتحٌ بلا تنوين. -/
def mamnuJarr (w : List SCell) : List SCell := setLast w 0
def mamnuNasb (w : List SCell) : List SCell := setLast w 0

theorem jarr_eq_nasb (w : List SCell) : mamnuJarr w = mamnuNasb w := rfl

theorem sarf_jarr_ne_nasb (w : List SCell) (hne : w ≠ []) : sarfJarr w ≠ sarfNasb w := by
  intro h
  unfold sarfJarr sarfNasb at h
  have h1 := List.append_inj_left' h rfl
  obtain ⟨k, hk⟩ := Zuruf.lastOf_setLast w 1 hne
  obtain ⟨k', hk'⟩ := Zuruf.lastOf_setLast w 0 hne
  rw [h1] at hk; rw [hk] at hk'
  cases hk'

/-- شرطُ الصرف الأوّل: بأل يُجرّ بالكسرة. -/
def alJarr (w : List SCell) : List SCell := Marifa.al (setLast w 1)

theorem al_jarr_kasra (w : List SCell) (hne : w ≠ []) :
    (Afal.lastOf (alJarr w)).map SCell.state = some 1 := by
  obtain ⟨k, hk⟩ := Zuruf.lastOf_setLast w 1 hne
  unfold alJarr Marifa.al
  have : ∀ v : List SCell, Afal.lastOf (Marifa.shamsi v) = Afal.lastOf v := by
    intro v
    match v with
    | a :: l :: x :: t =>
      show Afal.lastOf (if _ then _ else _) = _
      split <;> simp [Afal.lastOf]
    | [] => rfl
    | [_] => rfl
    | [_, _] => rfl
  rw [this]
  cases hs : setLast w 1 with
  | nil => rw [hs] at hk; simp [Afal.lastOf] at hk
  | cons y t => rw [hs] at hk; simpa [Afal.lastOf] using congrArg (Option.map SCell.state) hk

/-- شرطُ الصرف الثاني: مضافًا يُجرّ بالكسرة (المضافُ إليه يلحق). -/
def idafaJarr (w suffix : List SCell) : List SCell := Marifa.idafa (setLast w 1) suffix

theorem idafa_jarr_kasra (w : List SCell) (hne : w ≠ []) (hw : Nida.hasTanwin (setLast w 1) = false) :
    (Afal.lastOf (Marifa.dropTanwin (setLast w 1))).map SCell.state = some 1 := by
  obtain ⟨k, hk⟩ := Zuruf.lastOf_setLast w 1 hne
  unfold Marifa.dropTanwin; rw [hw]; simp only [Bool.false_eq_true, ite_false]
  rw [hk]; rfl

/-! ## عللُ الصيغة -/

/-- أعلى قالب؟ `rootOf` يستخرج الأصلَ ثمّ `fill` يعيد الصورةَ بعينها (بالضمّ في الآخر كما أُودعت). -/
def onTemplate (t : Wazn.Template) (w : List SCell) : Bool :=
  match Wazn.rootOf t w 0, Wazn.rootOf t w 1, Wazn.rootOf t w 2 with
  | some a, some b, some d => Wazn.fill t (fun i => if i = 0 then a else if i = 1 then b else d) == w
  | _, _, _ => false

theorem onTemplate_fill (t : Wazn.Template) (ht : Wazn.WF t) (r : Wazn.Root) :
    onTemplate t (Wazn.fill t r) = true := by
  unfold onTemplate
  rw [Wazn.rootOf_fill t ht r 0, Wazn.rootOf_fill t ht r 1, Wazn.rootOf_fill t ht r 2]
  simp only
  have : (fun i : Fin 3 => if i = 0 then r 0 else if i = 1 then r 1 else r 2) = r := by
    funext i
    match i with
    | 0 => rfl
    | 1 => rfl
    | 2 => rfl
  rw [this]; simp

/-- قوالبُ منتهى الجموع (أرقامُها في `Wazn.awzan`). -/
def muntaha : List Nat := [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112]
/-- فَعْلَان، أَفْعَل، فَعْلَاء، فُعْلَى، فَعْلَى. -/
def sifaT : List Nat := [54, 55, 80, 81, 82]

def templ (k : Nat) : Wazn.Template := Wazn.awzan.getD k []

/-- ألفُ التأنيث المقصورة: ألفٌ ساكنةٌ بعد فتحٍ، رابعةً فأكثر. -/
def maqsura (w : List SCell) : Bool :=
  w.length ≥ 4 && (match w.reverse with
    | a :: p :: _ => a.carrier.val == 1 && a.state.val == 3 && p.state.val == 0
    | _ => false)

/-- ألفُ التأنيث الممدودة: همزةٌ بعد ألفٍ ساكنةٍ بعد فتح، رابعةً فأكثر. -/
def mamduda (w : List SCell) : Bool :=
  w.length ≥ 4 && (match w.reverse with
    | h :: a :: p :: _ => h.carrier.val == 0 && a.carrier.val == 1 && a.state.val == 3 &&
                          p.state.val == 0
    | _ => false)

/-- الألفُ والنونُ الزائدتان: ألفٌ ساكنةٌ فنونٌ في الآخر بعد ثلاثةٍ فأكثر. -/
def alifNun (w : List SCell) : Bool :=
  w.length ≥ 5 && (match w.reverse with
    | n :: a :: _ => n.carrier.val == 25 && a.carrier.val == 1 && a.state.val == 3
    | _ => false)

inductive Illa where
  | muntahaJumu | maqsura | mamduda | sifa  -- وزنُ أَفْعَل/فَعْلَان/فَعْلَاء/فُعْلَى: صفةٌ أو علمٌ على وزن الفعل
  | alifNun | unread
  deriving DecidableEq, Repr

/-- علّةُ الصيغة المقروءة؛ `unread` = علّةُ معجم (علمٌ) أو منصرف. -/
def illa (w : List SCell) : Illa :=
  let w2 := setLast w 2
  if muntaha.any (fun k => onTemplate (templ k) w2) then .muntahaJumu
  else if mamduda w then .mamduda
  else if maqsura w then .maqsura
  else if sifaT.any (fun k => onTemplate (templ k) w2) then .sifa
  else if alifNun w then .alifNun
  else .unread

/-- شواهدُ من البوّابة: مَسَاجِدَ، مَصَابِيحَ، شُفَعَاءَ، كُبْرَى، أَحْمَرَ، عَطْشَانَ؛ وآدَمَ على وزن أَفْعَل
(العلميّةُ ووزنُ الفعل) تقرؤه الخانة؛ وسُلَيْمَانَ بألفٍ ونون؛ وإِبْرَاهِيمَ (العجمة) معجمٌ لا خانة. -/
def witnesses : List (String × List SCell × Illa) := [
  ("مَسَاجِدَ", [c 24 0, c 12 0, c 1 3, c 5 1, c 8 0], .muntahaJumu),
  ("مَصَابِيحَ", [c 24 0, c 14 0, c 1 3, c 2 1, c 28 3, c 6 0], .muntahaJumu),
  ("شُفَعَاءَ", [c 13 2, c 20 0, c 18 0, c 1 3, c 0 0], .mamduda),
  ("كُبْرَى", [c 22 2, c 2 3, c 10 0, c 1 3], .maqsura),
  ("أَحْمَرَ", [c 0 0, c 6 3, c 24 0, c 10 0], .sifa),
  ("عَطْشَانَ", [c 18 0, c 16 3, c 13 0, c 1 3, c 25 0], .sifa),
  ("آدَمَ", [c 0 0, c 1 3, c 8 0, c 24 0], .sifa),            -- على وزن أَفْعَل: العلميّةُ ووزنُ الفعل
  ("سُلَيْمَانَ", [c 12 2, c 23 0, c 28 3, c 24 0, c 1 3, c 25 0], .alifNun),
  ("إِبْرَاهِيمَ", [c 0 1, c 2 3, c 10 0, c 1 3, c 26 1, c 28 3, c 24 0], .unread)
]

theorem witnesses_illa : witnesses.all (fun w => illa w.2.1 == w.2.2) = true := by decide

theorem muntaha_wf : muntaha.all (fun k => decide (Wazn.WF (templ k))) = true := by decide

end Slge.Sarf
