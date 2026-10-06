import Slge.Madd

/-!
# الجذع: تسويةُ الآخر قبل القالب، وفصلُ الزوائد بردٍّ بعينه

* **الإعرابُ والمزاجُ حالةُ الخانة الأخيرة لا جزءٌ من القالب.** القوالبُ أُودعت بآخرٍ واحد (الضمّ للاسم، الفتح
  للماضي…)، فلا تُطابَق الكلمةُ إلّا بعد **تسوية آخرها** إلى حالة آخر القالب (`onTemplateMod`). وهذا مبرهَن:
  استخراجُ الجذر لا يرى الحالاتِ أصلًا (`rootOf_setLast`: لكلّ قالبٍ وكلمةٍ وحالة)، وملءُ القالب بأيّ حالةٍ في آخره
  يُقرأ على قالبه ويُستردّ جذرُه بعينه (`onTemplateMod_setLast`: لكلّ قالبٍ سليم ولكلّ جذرٍ ولكلّ حالة).
* **فصلُ الزوائد عمليّةٌ تُردّ بعينها.** السوابقُ من الجداول الحاصرة (و ف ب ل ك س أ لَ، وأل بعمليّة `Marifa.al`)،
  واللواحقُ من جداول الضمائر المتّصلة ولواحق الفاعل (`Filiyya.objectSuffixes`، `subjectSuffixes`)؛ والقطعُ
  `peelPrefix`/`peelSuffix`/`dropAl` كلٌّ منه يُردّ بالإلصاق (`peelPrefix_sound`، `peelSuffix_sound`،
  `dropAl_sound`: لكلّ كلمة)، والقارئُ `jidh` لا يعيد قراءةً إلّا وردُّها الكلمةُ بعينها (`jidh_restores`).
* القراءةُ: (سوابق، أل؟، جذع، لاحقة، قوالبُ الجذع بعد التسوية) — وقد تتعدّد (وَجَدَ: وَ+جَدَ أو وَجَدَ)؛ التعدّدُ
  يُقرأ كما هو والقرينةُ تفصله (مقيسٌ على MASAQ بقسمته المحجوبة).
ما ليس هنا — باسمه: الإعلالُ (قَالَ/كَانَ: مبرهَنٌ في الغانم `A116.Ilal` ولم يُنقل)، وقالبا فِعْلٍ وفَعَالٍ (غيرُ
مودَعين)، وتاءُ التأنيث واللواحقُ المركّبة. الحصرُ المُرسَل: لا شيء — هذه البوّابةُ من فحص الشجرة لا من حصر.
-/

namespace Slge.Jidh

open Slge.Categories (c)
open Slge.Zuruf (setLast)

/-! ## تسويةُ الآخر -/

/-- حالةُ آخر القالب. -/
def lastState (t : Wazn.Template) : Fin 4 :=
  match t.getLast? with
  | some s => Wazn.stateOf s
  | none => 0

/-- المطابقةُ بعد تسوية الآخر إلى حالة القالب. -/
def onTemplateMod (t : Wazn.Template) (w : List SCell) : Bool :=
  Sarf.onTemplate t (setLast w (lastState t))

theorem map_carrier_setLast : ∀ (w : List SCell) (st : Fin 4),
    (setLast w st).map (·.carrier) = w.map (·.carrier)
  | [], _ => rfl
  | [_], _ => rfl
  | _ :: y :: t, st => by
    simp only [setLast, List.map, List.cons.injEq, true_and]
    exact map_carrier_setLast (y :: t) st

theorem extract_of_carriers : ∀ (t : Wazn.Template) (w w' : List SCell),
    w.map (·.carrier) = w'.map (·.carrier) → Wazn.extract t w = Wazn.extract t w'
  | [], _, _, _ => rfl
  | _ :: _, [], [], _ => rfl
  | _ :: _, [], _ :: _, h => by simp at h
  | _ :: _, _ :: _, [], h => by simp at h
  | s :: t, x :: w, x' :: w', h => by
    simp only [List.map, List.cons.injEq] at h
    obtain ⟨hx, hw⟩ := h
    cases s with
    | lit _ => simp only [Wazn.extract]; exact extract_of_carriers t w w' hw
    | slot i _ => simp only [Wazn.extract, hx]; rw [extract_of_carriers t w w' hw]

/-- استخراجُ الجذر لا يرى الحالات: تسويةُ الآخر لا تمسّ الجذر — لكلّ قالبٍ وكلمةٍ وحالة. -/
theorem rootOf_setLast (t : Wazn.Template) (w : List SCell) (st : Fin 4) (i : Fin 3) :
    Wazn.rootOf t (setLast w st) i = Wazn.rootOf t w i := by
  unfold Wazn.rootOf
  rw [extract_of_carriers t _ _ (map_carrier_setLast w st)]

theorem lastState_cons (s : Wazn.Sym) (t : Wazn.Template) (h : t ≠ []) :
    lastState (s :: t) = lastState t := by
  unfold lastState
  rw [List.getLast?_cons_of_ne_nil h]

/-- ملءُ القالب آخرُه حالةُ آخر القالب. -/
theorem setLast_fill : ∀ (t : Wazn.Template) (r : Wazn.Root), t ≠ [] →
    setLast (Wazn.fill t r) (lastState t) = Wazn.fill t r
  | [], _, h => absurd rfl h
  | [s], r, _ => by
    cases s <;> simp [Wazn.fill, Wazn.fillSym, setLast, lastState, Wazn.stateOf]
  | s :: s' :: t, r, _ => by
    have ih := setLast_fill (s' :: t) r (by simp)
    rw [lastState_cons s (s' :: t) (by simp)]
    simp only [Wazn.fill, List.map] at ih ⊢
    simp only [setLast]
    rw [ih]

/-- تسويةُ الآخر مبرهَنة: ملءُ قالبٍ سليم بأيّ حالةٍ في آخره يُقرأ على قالبه ويُستردّ جذرُه بعينه — لكلّ قالبٍ
وجذرٍ وحالة. -/
theorem onTemplateMod_setLast (t : Wazn.Template) (ht : Wazn.WF t) (hne : t ≠ []) (r : Wazn.Root)
    (st : Fin 4) :
    onTemplateMod t (setLast (Wazn.fill t r) st) = true ∧
    ∀ i, Wazn.rootOf t (setLast (Wazn.fill t r) st) i = some (r i) := by
  constructor
  · unfold onTemplateMod
    rw [Shibh.setLast_setLast, setLast_fill t r hne]
    exact Sarf.onTemplate_fill t ht r
  · intro i
    rw [rootOf_setLast, Wazn.rootOf_fill t ht r i]

/-! ## القطعُ بردٍّ بعينه -/

def peelPrefix (p w : List SCell) : Option (List SCell) :=
  if w.take p.length == p then some (w.drop p.length) else none

theorem peelPrefix_sound {p w s : List SCell} (h : peelPrefix p w = some s) : p ++ s = w := by
  unfold peelPrefix at h
  split at h
  · rename_i hp
    simp only [Option.some.injEq] at h
    subst h
    have := List.take_append_drop p.length w
    rw [beq_iff_eq.1 hp] at this
    exact this
  · simp at h

def peelSuffix (q w : List SCell) : Option (List SCell) :=
  if q.length ≤ w.length && w.drop (w.length - q.length) == q then
    some (w.take (w.length - q.length)) else none

theorem peelSuffix_sound {q w s : List SCell} (h : peelSuffix q w = some s) : s ++ q = w := by
  unfold peelSuffix at h
  split at h
  · rename_i hq
    simp only [Bool.and_eq_true, decide_eq_true_eq, beq_iff_eq] at hq
    simp only [Option.some.injEq] at h
    subst h
    have := List.take_append_drop (w.length - q.length) w
    rw [hq.2] at this
    exact this
  · simp at h

/-- أل في الكلمة: لا، أو بهمزتها (ابتداءً)، أو موصولةً بلا همزةٍ بعد سابقة (وَلْأَرْضِ: همزةُ الوصل ساقطة). -/
inductive Al where
  | none | full | silent
  deriving DecidableEq, Repr

/-- أل على الجذع بصورتها. -/
def withAl : Al → List SCell → List SCell
  | .none, s => s
  | .full, s => Marifa.al s
  | .silent, s => (Marifa.al s).drop 1

/-- إسقاطُ أل: الجذعُ ما تعيد `withAl` منه الكلمةَ بعينها. -/
def dropAl (a : Al) (w : List SCell) : Option (List SCell) :=
  match a with
  | .none => some w
  | .full => if Marifa.hasAl w && Marifa.al (w.drop 2) == w then some (w.drop 2) else none
  | .silent => if w.drop 1 ≠ [] && (Marifa.al (w.drop 1)).drop 1 == w then some (w.drop 1) else none

theorem dropAl_sound {a : Al} {w s : List SCell} (h : dropAl a w = some s) : withAl a s = w := by
  cases a with
  | none => simp only [dropAl, Option.some.injEq] at h; subst h; rfl
  | full =>
    simp only [dropAl] at h
    split at h
    · rename_i hc
      simp only [Bool.and_eq_true, beq_iff_eq] at hc
      simp only [Option.some.injEq] at h
      subst h
      exact hc.2
    · simp at h
  | silent =>
    simp only [dropAl] at h
    split at h
    · rename_i hc
      simp only [Bool.and_eq_true, beq_iff_eq] at hc
      simp only [Option.some.injEq] at h
      subst h
      exact hc.2
    · simp at h

/-! ## الجداول -/

/-- السوابقُ المفردة: و ف ب ل ك س أ (الاستفهام) لَ (التوكيد). -/
def proclitics : List (List SCell) :=
  [[c 27 0], [c 20 0], [c 2 1], [c 23 1], [c 22 0], [c 12 0], [c 0 0], [c 23 0]]

/-- اللواحق: الضمائرُ المتّصلة ولواحقُ الفاعل. -/
def enclitics : List (List SCell) :=
  Filiyya.objectSuffixes ++ Filiyya.subjectSuffixes.map (·.1)

/-- معاني الجذع بعد تسوية آخره، بجذرٍ لا ألفَ فيه؛ والمضارعُ بردّ صدره ياءً. -/
def stemSenses (s : List SCell) : List Nat :=
  let v := Marifa.dropTanwin s
  let direct := (List.range 121).filter fun k =>
    let u := setLast v (lastState (Sarf.templ k))
    Maqam.onTemplateRoot k u
  if direct ≠ [] then direct
  else match v.head? with
    | some x => if x.carrier.val = 0 ∨ x.carrier.val = 25 ∨ x.carrier.val = 3 then
        (List.range 121).filter fun k =>
          Maqam.onTemplateRoot k (setLast (Maqam.withPrefix 28 v) (lastState (Sarf.templ k)))
      else []
    | none => []

structure Reading where
  pre : List (List SCell)
  al : Al
  stem : List SCell
  suf : List SCell
  templates : List Nat
  deriving DecidableEq, Repr

/-- الردُّ: السوابقُ ثمّ أل الجذع بصورتها ثمّ اللاحقة. -/
def Reading.restore (r : Reading) : List SCell :=
  r.pre.flatten ++ withAl r.al r.stem ++ r.suf

/-- قراءاتُ الكلمة: كلُّ قطعٍ من الجداول يعيد الكلمةَ بعينها وجذعُه على قالبٍ بعد التسوية. -/
def jidh (w : List SCell) : List Reading :=
  let pres : List (List (List SCell)) := [[]] ++ proclitics.map ([·]) ++
    (proclitics.flatMap fun p => proclitics.map fun q => [p, q])
  let sufs : List (List SCell) := [] :: enclitics
  (pres.flatMap fun pre => sufs.flatMap fun suf => [Al.none, Al.full, Al.silent].filterMap fun al =>
    -- الموصولةُ بلا همزةٍ لا تكون إلّا بعد سابقةٍ غيرِ همزة الاستفهام (آلْآنَ تُكتب بالمدّ)
    if al = .silent ∧ (pre = [] ∨ (pre.getLast?.map (·.head?.map (·.carrier.val))) = some (some 0)) then none
    else
    match peelPrefix pre.flatten w with
    | none => none
    | some w1 =>
      match peelSuffix suf w1 with
      | none => none
      | some w2 =>
        match dropAl al w2 with
        | none => none
        | some stem =>
          let ts := stemSenses stem
          if stem ≠ [] ∧ ts ≠ [] then
            let r : Reading := ⟨pre, al, stem, suf, ts⟩
            if r.restore == w then some r else none
          else none)

/-- كلُّ قراءةٍ تُردّ إلى الكلمة بعينها — لكلّ كلمة (القارئُ لا يعيد إلّا ما ردُّه الكلمة). -/
theorem jidh_restores (w : List SCell) : ∀ r ∈ jidh w, r.restore = w := by
  intro r hr
  unfold jidh at hr
  simp only [List.mem_flatMap, List.mem_filterMap] at hr
  obtain ⟨pre, _, suf, _, al, _, hm⟩ := hr
  revert hm
  split
  · simp
  · split
    · simp
    · split
      · simp
      · split
        · simp
        · split
          · intro hm
            split at hm
            · simp only [Option.some.injEq] at hm
              subst hm
              rename_i hbeq
              exact beq_iff_eq.1 hbeq
            · simp at hm
          · simp

def walard : List SCell := [c 27 0, c 23 3, c 0 0, c 10 3, c 15 1]                 -- وَلْأَرْضِ (صورةُ الشهادة)
def alard : List SCell := [c 0 0, c 23 3, c 0 0, c 10 3, c 15 2]                   -- أَلْأَرْضُ
def washshams : List SCell := [c 27 0, c 13 3, c 13 0, c 24 3, c 12 1]             -- وَشَّمْسِ
def rabbi : List SCell := [c 10 0, c 2 3, c 2 1]                                    -- رَبِّ
def kadhdhabu : List SCell := [c 22 0, c 9 3, c 9 0, c 2 2, c 27 3]                 -- كَذَّبُو
def tajalu : List SCell := [c 3 0, c 5 3, c 18 0, c 23 2, c 27 3]                   -- تَجْعَلُو
def bikitabihim : List SCell := [c 2 1, c 22 1, c 3 0, c 1 3, c 2 1, c 26 1, c 24 3] -- بِكِتَابِهِمْ
def wajada : List SCell := [c 27 0, c 5 0, c 8 0]                                   -- وَجَدَ

/-- وَلْأَرْضِ: و + أل موصولةً + أَرْض على فَعْلٍ؛ أَلْأَرْضُ: أل بهمزتها؛ وَشَّمْسِ: أل موصولةٌ شمسيّة. -/
theorem jidh_witnesses_al :
    (jidh walard).map (fun r => (r.pre.length, r.al, r.stem, r.templates)) =
      [(1, .silent, [c 0 0, c 10 3, c 15 1], [29])] ∧
    (jidh alard).map (fun r => (r.pre.length, r.al, r.templates)) = [(0, .full, [29])] ∧
    (jidh washshams).map (fun r => (r.pre.length, r.al, r.stem, r.templates)) =
      [(1, .silent, [c 13 0, c 24 3, c 12 1], [29])] := by
  refine ⟨by decide, by decide, by decide⟩

/-- رَبِّ: مجرورٌ يُقرأ على فَعْلٍ بعد التسوية؛ وَجَدَ: فعلٌ أو مصدرٌ بعد التسوية (0، 36) — التعدّدُ يُقرأ والقرينةُ
تفصل. -/
theorem jidh_witnesses_case :
    (jidh rabbi).map (·.templates) = [[29]] ∧ (jidh wajada).map (·.templates) = [[0, 36]] := by
  refine ⟨by decide, by decide⟩

/-- كَذَّبُوا: قراءتان على الخانة (فَعَّلَ + واو الجماعة، أو كَ + الذَّبُو)؛ تَجْعَلُوا: يَفْعَلُ بردّ الصدر + واو؛
بِكِتَابِهِمْ: ب + كِتَاب + هِمْ. -/
theorem jidh_witnesses_affix :
    (jidh kadhdhabu).map (fun r => (r.al, r.suf, r.templates)) =
      [(.none, [c 27 3], [12]), (.silent, [], [2])] ∧
    (jidh tajalu).map (fun r => (r.stem, r.suf, r.templates)) =
      [([c 3 0, c 5 3, c 18 0, c 23 2], [c 27 3], [4])] ∧
    (jidh bikitabihim).map (fun r => (r.pre.length, r.suf.length, r.templates)) = [(1, 2, [35, 41, 93])] := by
  refine ⟨by decide, by decide, by decide⟩

end Slge.Jidh
