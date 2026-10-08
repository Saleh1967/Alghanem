import Slge.Jidh
import Slge.ZawaidTable

/-!
# الزوائد: حروفُ سيبويه العشرة، ونونُ التوكيد، وتاءُ التأنيث، وحروفُ المضارعة

المصدرُ «باب علم حروف الزوائد» و«باب النون الثقيلة والخفيفة» من الكتاب (المختوم؛ الجدولُ `ZawaidTable`
مولَّدٌ منه). الزائدةُ عمليّةٌ جبريّةٌ على الخانات مغلقةٌ على الترخيص صعودًا (الإلصاقُ يحفظ الترخيص)
ونزولًا (القطعُ عكسُها بعينه عبر `Jidh.enclitics`)، لا بطاقةٌ تُقرأ:

* **العشرة** حواملُ متمايزة من التسعة والعشرين (`letters_ten`، `letters_nodup`)، وخاناتُها في الحالات
  الأربع أربعون من الـ116 (`cells_forty`) — فالزائدُ خانةٌ كسائر الخانات لا «فردٌ» جديد.
* **نونُ التوكيد**: الثقيلةُ خانتان `ن3 ن0` والخفيفةُ خانةٌ `ن3`؛ تلحقان الفعلَ بعد فتح آخره
  (`tawkid`)، والإلصاقُ يحفظ الترخيص (`tawkid_licensed`)؛ والخفيفةُ خانتُها خانةُ التنوين
  (`khafifa_is_tanwin`: سيبويه في «حروف البدل»: التنوينُ والنونُ الخفيفة يتبادلان) فتمييزُهما بالجهة
  (فعلٌ أو اسم) لا بالخانة.
* **تاءُ التأنيث الساكنة** `ت3` تلحق الفعلَ (`anith_licensed`).
* **القطعُ**: الثقيلةُ والتاءُ في `Jidh.enclitics` فيقرؤهما القارئُ نزولًا (`thaqila_read`،
  `taTanith_read` من `jidh_complete`).
* **حروفُ المضارعة** الأربعةُ من العشرة (`mudaraa_are_zawaid`) والإلصاقُ يحفظ الترخيص
  (`mudaraa_licensed`).
* **الشواهد** من الباب: تَقُولَنَّ، تَعْرِضَنَّ (`shawahid`)، وشواهدُ القرآن حواملَ في `ZawaidTable.witnesses`.
-/

namespace Slge.Zawaid

open Slge
open Slge.Categories (c)

/-- حواملُ الزوائد العشرة بترتيب الباب: ء ا ه ي ن ت س م و ل. -/
def letters : List Nat := table.map (·.1)

theorem letters_ten : letters = [0, 1, 26, 28, 25, 3, 12, 24, 27, 23] := by decide

theorem letters_nodup : letters.Nodup := by decide

theorem letters_lt : letters.all (· < 29) = true := by decide

/-- خاناتُ الزوائد: كلُّ حرفٍ زائد في حالاته الأربع. -/
def cells : List SCell :=
  [c 0 0, c 0 1, c 0 2, c 0 3, c 1 0, c 1 1, c 1 2, c 1 3, c 26 0, c 26 1, c 26 2, c 26 3,
   c 28 0, c 28 1, c 28 2, c 28 3, c 25 0, c 25 1, c 25 2, c 25 3, c 3 0, c 3 1, c 3 2, c 3 3,
   c 12 0, c 12 1, c 12 2, c 12 3, c 24 0, c 24 1, c 24 2, c 24 3, c 27 0, c 27 1, c 27 2, c 27 3,
   c 23 0, c 23 1, c 23 2, c 23 3]

theorem cells_forty : cells.length = 40 ∧ cells.Nodup ∧
    cells.all (fun x => decide (x.carrier.val ∈ letters)) = true := by decide

/-- نونُ التوكيد الثقيلة `ـنَّ` خانتان، والخفيفةُ `ـنْ` خانة، وتاءُ التأنيث الساكنة `ـتْ` خانة. -/
def thaqila : List SCell := [c 25 3, c 25 0]
def khafifa : List SCell := [c 25 3]
def taTanith : List SCell := [c 3 3]

/-- إلصاقُ نون التوكيد بالفعل: فتحُ آخره ثمّ النون (سيبويه: «أحوال الحروف التي قبل النون»). -/
def tawkid (w : List SCell) (heavy : Bool) : List SCell :=
  Zuruf.setLast w 0 ++ (if heavy then thaqila else khafifa)

/-- إلصاقُ تاء التأنيث الساكنة بالماضي: آخرُه مفتوحٌ ثمّ التاء. -/
def anith (w : List SCell) : List SCell := Zuruf.setLast w 0 ++ taTanith

theorem tawkid_licensed (w : List SCell) (heavy : Bool) (hw : licensed w = true) (hne : w ≠ [])
    (hlast : ∀ x, Afal.lastOf w = some x → x.state.val ≠ 3) :
    licensed (tawkid w heavy) = true := by
  unfold tawkid
  cases heavy
  · exact Jumla.suffix_licensed w khafifa 0 (by decide) hw hne hlast (by decide)
  · exact Jumla.suffix_licensed w thaqila 0 (by decide) hw hne hlast (by decide)

theorem anith_licensed (w : List SCell) (hw : licensed w = true) (hne : w ≠ [])
    (hlast : ∀ x, Afal.lastOf w = some x → x.state.val ≠ 3) : licensed (anith w) = true :=
  Jumla.suffix_licensed w taTanith 0 (by decide) hw hne hlast (by decide)

/-- الخفيفةُ خانةُ التنوين بعينها: ما فُتح آخرُه ثمّ `ن3` يقرؤه `Nida.hasTanwin` تنوينًا. -/
theorem khafifa_is_tanwin (w : List SCell) (hne : w ≠ []) :
    Nida.hasTanwin (tawkid w false) = true := by
  unfold tawkid khafifa
  obtain ⟨i, k, hi⟩ := Nawasikh.setLast_eq_append w 0 hne
  rw [hi]
  simp [Nida.hasTanwin, List.reverse_append, c]
  decide

/-- الثقيلةُ والتاءُ لاحقتان يقطعهما القارئ. -/
theorem in_enclitics : thaqila ∈ Jidh.enclitics ∧ taTanith ∈ Jidh.enclitics := by decide

/-- النزولُ يستوفي الصعود: الفعلُ على قالبٍ سليم بجذرٍ نظيف إذا لحقته النونُ الثقيلة (بعد تسوية آخره)
ففي قراءات `jidh` قراءةٌ لاحقتُها النونُ وجذعُها الفعل. -/
theorem thaqila_read (p : List SCell) (hp : p ∈ Jidh.proclitics) (k : Nat) (hk : k < Wazn.N)
    (r : Wazn.Root) (hr : ∀ i, (r i).val ≠ 1)
    (hlic : Madd.pauseLicensed (Zuruf.setLast (Wazn.fill (Sarf.templ k) r) 0) = true) :
    ∃ rd ∈ Jidh.jidh (p ++ Zuruf.setLast (Wazn.fill (Sarf.templ k) r) 0 ++ thaqila),
      rd.suf = thaqila ∧ rd.stem = Zuruf.setLast (Wazn.fill (Sarf.templ k) r) 0 ∧ k ∈ rd.templates := by
  obtain ⟨rd, hmem, _, _, hstem, hsuf, _, hk'⟩ :=
    Jidh.jidh_complete p hp thaqila in_enclitics.1 k hk r hr 0 hlic
  exact ⟨rd, hmem, hsuf, hstem, hk'⟩

theorem taTanith_read (p : List SCell) (hp : p ∈ Jidh.proclitics) (k : Nat) (hk : k < Wazn.N)
    (r : Wazn.Root) (hr : ∀ i, (r i).val ≠ 1)
    (hlic : Madd.pauseLicensed (Zuruf.setLast (Wazn.fill (Sarf.templ k) r) 0) = true) :
    ∃ rd ∈ Jidh.jidh (p ++ Zuruf.setLast (Wazn.fill (Sarf.templ k) r) 0 ++ taTanith),
      rd.suf = taTanith ∧ k ∈ rd.templates := by
  obtain ⟨rd, hmem, _, _, _, hsuf, _, hk'⟩ :=
    Jidh.jidh_complete p hp taTanith in_enclitics.2 k hk r hr 0 hlic
  exact ⟨rd, hmem, hsuf, hk'⟩

/-- حروفُ المضارعة: الهمزةُ والنونُ والياءُ والتاء — من العشرة، «أوّلًا في الفعل» عند سيبويه. -/
def mudaraa : List Nat := [0, 25, 28, 3]

theorem mudaraa_are_zawaid : mudaraa.all (fun k => decide (k ∈ letters)) = true := by decide

theorem mudaraa_licensed (k : Fin 29) (st : Fin 4) (hne : st.val ≠ 3)
    (w : List SCell) (hw : licensed w = true) : licensed (⟨k, st⟩ :: w) = true :=
  Jidh.prefix_licensed ⟨k, st⟩ hne w hw

/-- شواهدُ الباب: تَقُولَنَّ (ولا تقولنّ لشيء)، تَعْرِضَنَّ (وإمّا تعرضنّ)، قَالَتْ. -/
theorem shawahid :
    tawkid [c 3 0, c 21 2, c 27 3, c 23 2] true = [c 3 0, c 21 2, c 27 3, c 23 0, c 25 3, c 25 0] ∧
    licensed (tawkid [c 3 0, c 21 2, c 27 3, c 23 2] true) = true ∧
    tawkid [c 3 2, c 18 3, c 10 1, c 15 2] true = [c 3 2, c 18 3, c 10 1, c 15 0, c 25 3, c 25 0] ∧
    licensed (tawkid [c 3 2, c 18 3, c 10 1, c 15 2] false) = true ∧
    anith [c 21 0, c 1 3, c 23 0] = [c 21 0, c 1 3, c 23 0, c 3 3] ∧
    licensed (anith [c 21 0, c 1 3, c 23 0]) = true ∧
    Nida.hasTanwin (tawkid [c 3 0, c 21 2, c 27 3, c 23 2] false) = true := by decide

end Slge.Zawaid
