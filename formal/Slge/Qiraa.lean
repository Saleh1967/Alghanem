import Slge.Tawzi
import Slge.Sawabiq
import Slge.Huruf

/-!
# القراءةُ الموحَّدة: الحرفُ أوّلًا، والجذعُ على الصورة وعلى أصلها المردود (ADR ٤٢)

ثلاثةُ قرّاءٍ قائمين تُركَّب ولا يُزاد عليها شيء:

* **الحرفُ بالموزِّع قبل الجذع.** ما يقرؤه `Tawzi.tawzi` ونواتُه من حروف المعاني (`Huruf.table`، 68 حرفًا)
  حرفٌ (`harf`)؛ فلا جذرَ يُحكم عليه منه (`harf_no_hukm`: فِي، مِنْ، إِلَى، لَكُمْ) — **ولا تُحذف** قراءاتُ الجذع
  (`jidh_sub_qiraa`): فالكتابةُ الواحدة قد تكون حرفًا وفعلًا (عَلَى/عَلَا، خَلَا)، والترتيبُ لا الحذف.
* **الجذعُ على الصورة** كما هي (`Jidh.jidh`): تُردّ إلى الكلمة بعينها.
* **الجذعُ على الأصل المردود.** ما ردّت `Sawabiq` ساقطَه في الوصل (همزةُ الوصل بحركتها أو بالوجهين، ولامُ الأمر
  المسكَّنة) يقرؤه الجذعُ على `pre ++ under` (فَمْشُوْ ← فَءِمْشُوْ)؛ وأل الموصولةُ يقرؤها الجذعُ أصلًا
  (`Al.silent`) فلا تُكرَّر. كلُّ قراءةٍ تُردّ: سابقتُها إلى الكلمة بعينها وجذعُها إلى الأصل بعينه
  (`qiraa_restores`)، وأصلُها يصعد بسلسلته إلى جذعها (`qiraa_ascends`).
-/

namespace Slge.Qiraa

open Slge.Categories (c)

/-- خاناتُ حروف المعاني (`Huruf.table`). -/
def hurufCells : List (List SCell) := Huruf.table.map (·.cells)

/-- قراءاتُ الموزِّع التي نواتُها من حروف المعاني. -/
def harf (w : List SCell) : List Tawzi.Mabni :=
  (Tawzi.tawzi w).filter fun m => hurufCells.contains m.core && Tawzi.base m

/-- قراءةٌ موحَّدة: قراءةُ الجذع، وقراءةُ السابقة التي رُدّ بها الأصلُ إن كانت. -/
structure Reading where
  via : Option Sawabiq.Reading
  r : Jidh.Reading
  deriving DecidableEq, Repr

/-- قراءاتُ السابقة الموصولة غيرِ أل: ما سقط فيها رُدّ (`under ≠ rest`). -/
def lifted (w : List SCell) : List Sawabiq.Reading :=
  (Sawabiq.sawabiq w).filter fun m => m.under != m.rest && m.kind != .al

/-- الجذعُ على الأصل المردود. -/
def restored (w : List SCell) : List Reading :=
  (lifted w).flatMap fun m => (Jidh.jidh (m.pre ++ m.under)).map fun r => ⟨some m, r⟩

/-- القراءةُ الموحَّدة: الجذعُ على الصورة ثمّ على الأصل المردود. -/
def qiraa (w : List SCell) : List Reading := (Jidh.jidh w).map (⟨none, ·⟩) ++ restored w

/-- ما يُحكم على جذره: لا شيءَ إن قرأ الموزِّعُ الكلمةَ حرفًا، وإلّا القراءةُ الموحَّدة كلُّها. -/
def hukmReadings (w : List SCell) : List Reading := if (harf w).isEmpty then qiraa w else []

/-! ## المبرهَن -/

/-- قراءةُ الحرف تُردّ إلى الكلمة بعينها ونواتُها من حروف المعاني. -/
theorem harf_restores {w : List SCell} {m : Tawzi.Mabni} (h : m ∈ harf w) :
    Tawzi.restore m = w ∧ m.core ∈ hurufCells := by
  simp only [harf, List.mem_filter, Bool.and_eq_true, List.contains_iff_mem] at h
  exact ⟨Tawzi.tawzi_restores h.1, h.2.1⟩

/-- قراءاتُ الحكم لا ترى قواعدَ ADR ٥٢: كلُّ قراءة حرفٍ بلا قاعدة. -/
theorem harf_base {w : List SCell} {m : Tawzi.Mabni} (h : m ∈ harf w) : Tawzi.base m = true := by
  unfold harf at h
  have := (List.mem_filter.1 h).2
  simp only [Bool.and_eq_true] at this
  exact this.2

/-- لا جذرَ يُحكم عليه من حرف: ما قرأه الموزِّعُ حرفًا فلا قراءةَ للحكم. -/
theorem harf_no_hukm {w : List SCell} (h : harf w ≠ []) : hukmReadings w = [] := by
  simp [hukmReadings, List.isEmpty_iff, h]

/-- وما لم يُقرأ حرفًا فقراءاتُ الحكم هي القراءةُ الموحَّدة كلُّها. -/
theorem hukm_of_not_harf {w : List SCell} (h : harf w = []) : hukmReadings w = qiraa w := by
  simp [hukmReadings, h]

/-- لا تُحذف قراءةُ جذعٍ على الصورة: كلُّها في القراءة الموحَّدة — لكلّ كلمة. -/
theorem jidh_sub_qiraa (w : List SCell) : ∀ r ∈ Jidh.jidh w, (⟨none, r⟩ : Reading) ∈ qiraa w := by
  intro r hr
  simp only [qiraa, List.mem_append, List.mem_map]
  exact Or.inl ⟨r, hr, rfl⟩

/-- كلُّ قراءةٍ تُردّ: بلا سابقةٍ إلى الكلمة بعينها، وبسابقةٍ موصولةٍ: السابقةُ إلى الكلمة والجذعُ إلى أصلها
المردود — لكلّ كلمة. -/
theorem qiraa_restores (w : List SCell) : ∀ q ∈ qiraa w,
    (q.via = none ∧ q.r.restore = w) ∨
    ∃ m, q.via = some m ∧ Sawabiq.restore m = w ∧ m.under ≠ m.rest ∧ q.r.restore = m.pre ++ m.under := by
  intro q hq
  simp only [qiraa, restored, List.mem_append, List.mem_map, List.mem_flatMap] at hq
  rcases hq with ⟨r, hr, rfl⟩ | ⟨m, hm, r, hr, rfl⟩
  · exact Or.inl ⟨rfl, Jidh.jidh_restores w r hr⟩
  · simp only [lifted, List.mem_filter, Bool.and_eq_true, bne_iff_ne, ne_eq] at hm
    exact Or.inr ⟨m, rfl, Sawabiq.sawabiq_restores hm.1, hm.2.1, Jidh.jidh_restores _ r hr⟩

/-- أصلُ كلّ قراءةٍ يصعد بسلسلة إعلالها إلى جذعها — لكلّ كلمة (`Jidh.jidh_ascends`). -/
theorem qiraa_ascends (w : List SCell) :
    ∀ q ∈ qiraa w, Ilal.ascend q.r.ilal (q.r.asl ++ q.r.suf) = some (q.r.stem ++ q.r.suf) := by
  intro q hq
  simp only [qiraa, restored, List.mem_append, List.mem_map, List.mem_flatMap] at hq
  rcases hq with ⟨r, hr, rfl⟩ | ⟨m, _, r, hr, rfl⟩
  · exact Jidh.jidh_ascends w r hr
  · exact Jidh.jidh_ascends _ r hr

/-! ## الشواهد بالحساب -/

def fi : List SCell := [c 20 1, c 28 3]                             -- فِي
def lakum : List SCell := [c 23 0, c 22 2, c 24 3]                  -- لَكُمْ
def ila : List SCell := [c 0 1, c 23 0, c 1 3]                      -- إِلَى
def famshu : List SCell := [c 20 0, c 24 3, c 13 2, c 27 3]         -- فَمْشُوْ (صورةُ الشهادة)
def kataba : List SCell := [c 22 0, c 3 0, c 2 0]                   -- كَتَبَ

/-- فِي ولَكُمْ وإِلَى حروفٌ لا حكمَ على جذرها؛ وكَتَبَ ليست حرفًا فقراءاتُها للحكم. -/
theorem witnesses_harf :
    harf fi ≠ [] ∧ harf lakum ≠ [] ∧ harf ila ≠ [] ∧ harf kataba = [] ∧
    hukmReadings fi = [] ∧ hukmReadings kataba = qiraa kataba := by
  refine ⟨by decide +kernel, by decide +kernel, by decide +kernel, by decide +kernel,
    harf_no_hukm (by decide +kernel), hukm_of_not_harf (by decide +kernel)⟩

/-- فَمْشُوْ: الصورةُ الموصولة قراءةٌ واحدة (فَمْشُ)، والأصلُ المردود بهمزة وصلٍ مكسورة (فَءِمْشُوْ، `liftArid`
وقاعدةُ الثالث معًا) خمسُ قراءاتٍ كلُّها بسابقة الفعل الموصولة. -/
theorem witness_famshu :
    (Jidh.jidh famshu).length = 1 ∧ (restored famshu).length = 5 ∧
    (restored famshu).all (fun q => q.via.map (·.kind) == some .waslFil) = true ∧
    (qiraa famshu).length = 6 := by decide +kernel

end Slge.Qiraa
