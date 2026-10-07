import Slge.Jidh
import Slge.AbniyaTable

/-!
# قوالبُ الاسم على أبنية سيبويه: الهيكلُ مودَعٌ مختوم، والقوالبُ متمايزةٌ على الأصول النظيفة

* **الهيكل** (`skeletonOf`): القالبُ حروفًا بلا حركات — الأصولُ ف ع ل، والزوائدُ بحواملها، والشدّةُ حرفٌ واحد،
  والتاءُ الأخيرةُ تاءُ تأنيثٍ تُسقط (اصطلاحُ الأبنية). والعضويّةُ في أبنية سيبويه (`inAbniya`) تقبل الهمزةَ الأولى
  وصلًا أو قطعًا، لأنّ الخانةَ لا تميّزهما (الوصلُ بقيّةُ رسمٍ في الغانم).
* `outside_abniya`: الأوزانُ التي ليست هياكلُها عند سيبويه بأرقامها — مسمّاة، لا تُدَّعى.
* **التمايز** (`separated`): قالبان يفترقان على كلّ أصلين نظيفين (لا حرفَ زيادةٍ فيهما) إذا اختلفا في زائدٍ، أو
  زائدٌ قبالةَ أصل، أو أصلان بحالتين مختلفتين — وفي الآخر بالحامل وحدَه لأنّ الإعرابَ يُسوّى (`Jidh.onTemplateMod`).
  `separated_sound`: لكلّ قالبين من الجدول وأصلين نظيفين وحالتي آخر، الملآن بعد التسوية مختلفان.
* `awzan_separated`: كلُّ زوجين من الجدول مفصولان إلّا الأزواجَ المسمّاة في `ambiguous` (فَعَلَ/فَعَلٌ، أَفْعَلَ/أَفْعَلُ،
  الماضي/الأمر، والجدولُ المكرَّر بأسماءٍ مختلفة) — وهي بعينها ما يعيده الجذعُ قراءاتٍ متعدّدة.
-/

namespace Slge.Abniya

open Slge.Wazn

/-- حاملُ الرمز في الهيكل: الأصولُ ف ع ل (20، 18، 23) والزوائدُ بحواملها. -/
def symCarrier : Sym → Nat
  | .slot i _ => if i.val = 0 then 20 else if i.val = 1 then 18 else 23
  | .lit c => c.carrier.val

/-- الشدّةُ حرفٌ واحد: رمزٌ ساكنٌ يتلوه الرمزُ نفسُه متحرّكًا يُسقط (إلّا الألف). -/
def collapse : List Sym → List Nat
  | [] => []
  | x :: y :: t =>
    if (stateOf x).val = 3 ∧ symCarrier x = symCarrier y ∧ symCarrier x ≠ 1 then collapse (y :: t)
    else symCarrier x :: collapse (y :: t)
  | [x] => [symCarrier x]

/-- هيكلُ القالب (اصطلاحُ الأبنية: التاءُ الأخيرةُ تاءُ تأنيث). -/
def skeletonOf (t : Template) : List Nat :=
  let s := collapse t
  if s.getLast? = some 3 then s.dropLast else s

/-- العضويّةُ في أبنية سيبويه: الهيكلُ بعينه، أو بهمزةٍ أولى وصلًا (ا) بدل القطع (ء). -/
def inAbniya (t : Template) : Bool :=
  let s := skeletonOf t
  abniya.contains s || (match s with | 0 :: rest => abniya.contains (1 :: rest) | _ => false)

set_option maxRecDepth 100000 in
/-- الأوزانُ خارج أبنية سيبويه — بأرقامها: مصادرُ الانفعال والافتعال والافعلال والاستفعال، ومضارعُ التفعّل
والافتعال واسما فاعلهما ومفعولُ الافتعال، ومنتهى الجموع بالياء، وفَعَالَى/فُعَالَى. 14 من 125. -/
theorem outside_abniya :
    (List.range Wazn.N).filter (fun k => !inAbniya (Sarf.templ k)) =
      [23, 26, 44, 45, 46, 47, 72, 75, 76, 102, 104, 106, 109, 110] := by decide

set_option maxRecDepth 100000 in
/-- قوالبُ الاسم الأربعة المضافة (فِعْل، فَعَال، فُعَيْل، فَاعُول) هياكلُها عند سيبويه؛ وحوافُّها من آبائها في
`Shabaka.edges` (`edges_apply`). -/
theorem ism_in_abniya : [121, 122, 123, 124].all (fun k => inAbniya (Sarf.templ k)) = true := by decide

/-! ## التمايز على الأصول النظيفة -/

/-- حروفُ الزيادة: ما يظهر زائدًا في قالبٍ من الجدول (ء ا ت س م ن و ي). -/
def augments : List (Fin 29) := [0, 1, 3, 12, 24, 25, 27, 28]

/-- كلُّ زائدٍ في الجدول من حروف الزيادة. -/
def litIn : Sym → Bool
  | .lit c => augments.contains c.carrier
  | .slot _ _ => true

set_option maxRecDepth 100000 in
theorem awzan_lits : ∀ t ∈ awzan, ∀ x ∈ t, litIn x = true := by decide

set_option maxRecDepth 100000 in
theorem templ_lits : ∀ k ∈ List.range Wazn.N, ∀ x ∈ Sarf.templ k, litIn x = true := by decide

/-- أصلٌ نظيف: لا حرفَ زيادةٍ فيه. -/
def Clean (r : Root) : Prop := ∀ i, r i ∉ augments

/-- رمزان يفترقان في غير الآخر: زائدان مختلفان، أو زائدٌ وأصل، أو أصلان بحالتين. -/
def sep : Sym → Sym → Bool
  | .lit c, .lit c' => c != c'
  | .slot _ s, .slot _ s' => s != s'
  | _, _ => true

/-- في الآخر: الحاملُ وحدَه (الحالةُ تُسوّى). -/
def sepLast : Sym → Sym → Bool
  | .lit c, .lit c' => c.carrier != c'.carrier
  | .slot _ _, .slot _ _ => false
  | _, _ => true

def separated : Template → Template → Bool
  | [], [] => false
  | [], _ :: _ => true
  | _ :: _, [] => true
  | [x], [y] => sepLast x y
  | [_], _ :: _ :: _ => true
  | _ :: _ :: _, [_] => true
  | x :: a :: t, y :: b :: t' => sep x y || separated (a :: t) (b :: t')

theorem length_setLast : ∀ (w : List SCell) (st : Fin 4), (Zuruf.setLast w st).length = w.length
  | [], _ => rfl
  | [_], _ => rfl
  | _ :: y :: t, st => by simp [Zuruf.setLast, length_setLast (y :: t) st]

theorem fillSym_carrier_ne (r r' : Root) (hr : Clean r) (hr' : Clean r') (x y : Sym)
    (hx : litIn x = true) (hy : litIn y = true) (h : sepLast x y = true) :
    (fillSym r x).carrier ≠ (fillSym r' y).carrier := by
  cases x with
  | lit c =>
    cases y with
    | lit c' =>
      simp only [sepLast, bne_iff_ne, ne_eq] at h
      simpa [fillSym] using h
    | slot j s' =>
      intro he
      simp only [fillSym] at he
      simp only [litIn, List.contains_iff_mem] at hx
      exact hr' j (he ▸ hx)
  | slot i s =>
    cases y with
    | lit c' =>
      intro he
      simp only [fillSym] at he
      simp only [litIn, List.contains_iff_mem] at hy
      exact hr i (he ▸ hy)
    | slot j s' => simp [sepLast] at h

theorem fillSym_ne (r r' : Root) (hr : Clean r) (hr' : Clean r') (x y : Sym)
    (hx : litIn x = true) (hy : litIn y = true) (h : sep x y = true) :
    fillSym r x ≠ fillSym r' y := by
  cases x with
  | lit c =>
    cases y with
    | lit c' => simp only [sep, bne_iff_ne, ne_eq] at h; simpa [fillSym] using h
    | slot j s' =>
      intro he
      have := congrArg SCell.carrier he
      simp only [fillSym] at this
      simp only [litIn, List.contains_iff_mem] at hx
      exact hr' j (this ▸ hx)
  | slot i s =>
    cases y with
    | lit c' =>
      intro he
      have := congrArg SCell.carrier he
      simp only [fillSym] at this
      simp only [litIn, List.contains_iff_mem] at hy
      exact hr i (this ▸ hy)
    | slot j s' =>
      simp only [sep, bne_iff_ne, ne_eq] at h
      intro he
      have := congrArg SCell.state he
      simp only [fillSym] at this
      exact h this

/-- قالبان مفصولان لا يقرآن ملءً واحدًا بعد تسوية الآخر على أصلين نظيفين. -/
theorem separated_sound (r r' : Root) (hr : Clean r) (hr' : Clean r') :
    ∀ (t t' : Template), (∀ x ∈ t, litIn x = true) → (∀ y ∈ t', litIn y = true) →
      separated t t' = true → ∀ st st', Zuruf.setLast (fill t r) st ≠ Zuruf.setLast (fill t' r') st'
  | [], [], _, _, h, _, _ => by simp [separated] at h
  | [], _ :: _, _, _, _, st, st' => by
    intro he; have := congrArg List.length he; simp [length_setLast, fill] at this
  | _ :: _, [], _, _, _, st, st' => by
    intro he; have := congrArg List.length he; simp [length_setLast, fill] at this
  | [x], [y], hx, hy, h, st, st' => by
    simp only [separated] at h
    intro he
    simp only [fill, List.map, Zuruf.setLast, List.cons.injEq, and_true] at he
    have hc := congrArg SCell.carrier he
    exact fillSym_carrier_ne r r' hr hr' x y (hx x (by simp)) (hy y (by simp)) h hc
  | [_], _ :: _ :: _, _, _, _, st, st' => by
    intro he; have := congrArg List.length he; simp [length_setLast, fill] at this
  | _ :: _ :: _, [_], _, _, _, st, st' => by
    intro he; have := congrArg List.length he; simp [length_setLast, fill] at this
  | x :: a :: t, y :: b :: t', hx, hy, h, st, st' => by
    simp only [separated, Bool.or_eq_true] at h
    intro he
    simp only [fill, List.map, Zuruf.setLast, List.cons.injEq] at he
    rcases h with h | h
    · exact fillSym_ne r r' hr hr' x y (hx x (by simp)) (hy y (by simp)) h he.1
    · have ih := separated_sound r r' hr hr' (a :: t) (b :: t')
        (fun z hz => hx z (List.mem_cons_of_mem _ hz)) (fun z hz => hy z (List.mem_cons_of_mem _ hz)) h st st'
      exact ih (by simpa [fill] using he.2)

/-- الأزواجُ غيرُ المفصولة في الجدول — مسمّاة: الماضي ومصدرُه (فَعَلَ/فَعَلٌ)، الماضي والصفة (أَفْعَلَ/أَفْعَلُ)،
الماضي والأمر، والقالبُ المكرَّر بأسماءٍ مختلفة (فُعُول، فِعَال ×3، فَاعِل/فَاعِلْ، مِفْعَال، فِعْلَة). -/
def ambiguous : List (Nat × Nat) :=
  [(0, 36), (11, 54), (14, 116), (15, 117), (30, 94), (35, 41), (35, 93), (41, 93), (48, 115),
   (51, 60), (64, 86)]

set_option maxRecDepth 100000 in
theorem ambiguous_sound : ambiguous.all (fun p => !separated (Sarf.templ p.1) (Sarf.templ p.2)) = true := by
  decide

set_option maxRecDepth 100000 in
/-- كلُّ زوجين من الجدول مفصولان إلّا المسمّاة. -/
theorem awzan_separated :
    (List.range Wazn.N).all (fun k => (List.range Wazn.N).all (fun k' =>
      !(k < k') || separated (Sarf.templ k) (Sarf.templ k') || ambiguous.contains (k, k'))) = true := by
  decide +kernel

/-- التمايز: قالبان مختلفان غيرُ مسمّيين لا يقرآن ملءً واحدًا على أصلين نظيفين بعد تسوية الآخر. -/
theorem awzan_disjoint (k k' : Nat) (hk : k < Wazn.N) (hk' : k' < Wazn.N) (hlt : k < k')
    (hamb : (k, k') ∉ ambiguous) (r r' : Root) (hr : Clean r) (hr' : Clean r') (st st' : Fin 4) :
    Zuruf.setLast (fill (Sarf.templ k) r) st ≠ Zuruf.setLast (fill (Sarf.templ k') r') st' := by
  have hall := awzan_separated
  simp only [List.all_eq_true, List.mem_range, Bool.or_eq_true, Bool.not_eq_true', decide_eq_false_iff_not,
    List.contains_iff_mem] at hall
  rcases hall k hk k' hk' with (h | h) | h
  · exact absurd hlt h
  · exact separated_sound r r' hr hr' _ _ (templ_lits k (List.mem_range.mpr hk))
      (templ_lits k' (List.mem_range.mpr hk')) h st st'
  · exact absurd h hamb

end Slge.Abniya
