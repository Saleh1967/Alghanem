import Slge.Madd
import Slge.Ilal

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
* **الإعلالُ نزولًا:** إن لم يُقرأ الجذعُ على قالبٍ نزل القارئُ بقواعد `Ilal` (حتى خطوتين) إلى أصولٍ يصعد كلٌّ
  منها بسلسلته إلى الجذع بعينه (`jidh_ascends`: لكلّ قراءة)، وما صعد بالجبر ينزل (`jidh_complete_ilal`).
ما ليس هنا — باسمه: قالبا فِعْلٍ وفَعَالٍ (غيرُ مودَعين)، وتاءُ التأنيث واللواحقُ المركّبة، والإعلالُ بثلاث خطوات.
الحصرُ المُرسَل: لا شيء — هذه البوّابةُ من فحص الشجرة لا من حصر.
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

/-- زوائدُ سيبويه اللاحقةُ بالفعل (`Slge.Zawaid` يبرهنها على بابها): نونُ التوكيد الثقيلة `ـَنَّ`،
وتاءُ التأنيث الساكنة `ـَتْ`، وكلٌّ منهما قبل ضميرِ نصبٍ (يَأْتِيَنَّكُمْ، أَخَذَتْكُمْ: إغلاقُ اللواحق على
التركيب)؛ والخفيفةُ `ـَنْ` خانتُها خانةُ التنوين فيقرؤها `stemSenses` بردّه. -/
def zawaidSuffixes : List (List SCell) :=
  [[c 25 3, c 25 0], [c 3 3]] ++
    [[c 25 3, c 25 0], [c 3 3]].flatMap (fun z => Filiyya.objectSuffixes.map (z ++ ·))

/-- اللواحق: الضمائرُ المتّصلة ولواحقُ الفاعل وزوائدُ سيبويه. -/
def enclitics : List (List SCell) :=
  Filiyya.objectSuffixes ++ Filiyya.subjectSuffixes.map (·.1) ++ zawaidSuffixes

/-- القوالبُ التي تُقرأ عليها الكلمةُ بعد تسوية آخرها، بجذرٍ لا ألفَ فيه. -/
def onTemplates (v : List SCell) : List Nat :=
  (List.range Wazn.N).filter fun k => Maqam.onTemplateRoot k (setLast v (lastState (Sarf.templ k)))

/-- معاني الجذع بعد تسوية آخره: كما هو أوّلًا (فالنونُ الساكنةُ قد تكون لامًا: كَوَنْ)، ثمّ بردّ التنوين،
ثمّ المضارعُ بردّ صدره ياءً. -/
def stemSenses (s : List SCell) : List Nat :=
  if onTemplates s ≠ [] then onTemplates s
  else
    let v := Marifa.dropTanwin s
    if Nida.hasTanwin s ∧ onTemplates v ≠ [] then onTemplates v
    else match v.head? with
      | some x => if x.carrier.val = 0 ∨ x.carrier.val = 25 ∨ x.carrier.val = 3 then
          onTemplates (Maqam.withPrefix 28 v)
        else []
      | none => []

/-- صورةُ الجذع التي قُرئ عليها — بترتيب `stemSenses`: كما هو، أو بلا تنوين، أو بصدر المضارع ياءً.
الجذرُ يُستخرج منها لا من الجذع كما هو (فالتنوينُ خانةٌ زائدة على القالب). -/
def stemForm (s : List SCell) : List SCell :=
  if onTemplates s ≠ [] then s
  else
    let v := Marifa.dropTanwin s
    if Nida.hasTanwin s ∧ onTemplates v ≠ [] then v
    else match v.head? with
      | some x => if x.carrier.val = 0 ∨ x.carrier.val = 25 ∨ x.carrier.val = 3 then
          Maqam.withPrefix 28 v
        else v
      | none => v

theorem dropTanwin_of_not (s : List SCell) (h : Nida.hasTanwin s = false) : Marifa.dropTanwin s = s := by
  simp [Marifa.dropTanwin, h]

/-- معاني الجذع هي قوالبُ صورته بعينها: ما يُقرأ عليه الجذعُ يُقرأ على `stemForm`. -/
theorem stemSenses_eq_stemForm (s : List SCell) : stemSenses s = onTemplates (stemForm s) := by
  unfold stemSenses stemForm
  by_cases h1 : onTemplates s ≠ []
  · simp [h1]
  · simp only [h1, ite_false]
    by_cases h2 : Nida.hasTanwin s ∧ onTemplates (Marifa.dropTanwin s) ≠ []
    · simp [h2]
    · simp only [h2, ite_false]
      have hv : onTemplates (Marifa.dropTanwin s) = [] := by
        by_cases ht : Nida.hasTanwin s
        · exact Classical.not_not.mp (fun hne => h2 ⟨ht, hne⟩)
        · rw [dropTanwin_of_not s (by simpa using ht)]; exact Classical.not_not.mp h1
      split
      · split
        · rfl
        · exact hv.symm
      · exact hv.symm

structure Reading where
  pre : List (List SCell)
  al : Al
  stem : List SCell
  suf : List SCell
  /-- أصلُ الجذع قبل الإعلال (الجذعُ نفسُه إن لم يكن إعلال). -/
  asl : List SCell
  /-- سلسلةُ الصعود من الأصل (مع اللاحقة) إلى الجذع (مع اللاحقة). -/
  ilal : Ilal.Chain
  templates : List Nat
  deriving DecidableEq, Repr

/-- الردُّ: السوابقُ ثمّ أل الجذع بصورتها ثمّ اللاحقة. -/
def Reading.restore (r : Reading) : List SCell :=
  r.pre.flatten ++ withAl r.al r.stem ++ r.suf

/-- قراءاتُ قطعٍ واحد (سوابق، لاحقة، أل): الجذعُ مرخَّصٌ في ذاته، وعلى قالبٍ بعد التسوية مباشرةً أو بعد
النزول بالإعلال إلى أصلٍ على قالب. -/
def readingsAt (w : List SCell) (pre : List (List SCell)) (suf : List SCell) (al : Al) : List Reading :=
  match peelPrefix pre.flatten w with
  | none => []
  | some w1 =>
    match peelSuffix suf w1 with
    | none => []
    | some w2 =>
      match dropAl al w2 with
      | none => []
      | some stem =>
        -- النزول: الجذعُ كلمةٌ مرخَّصةٌ (وقفًا) في ذاته — الجبرُ مغلقٌ نزولًا كما هو صعودًا
        if stem ≠ [] ∧ Madd.pauseLicensed stem then
          if stemSenses stem ≠ [] then [⟨pre, al, stem, suf, stem, [], stemSenses stem⟩]
          else (Ilal.descend (stem ++ suf) stem.length).filterMap fun x =>
            match peelSuffix suf x.2 with
            | none => none
            | some asl =>
              if stemSenses asl ≠ [] then some ⟨pre, al, stem, suf, asl, x.1, stemSenses asl⟩ else none
        else []

/-- قراءاتُ الكلمة: كلُّ قطعٍ من الجداول يعيد الكلمةَ بعينها وجذعُه على قالبٍ بعد التسوية (أو بعد الإعلال). -/
def jidh (w : List SCell) : List Reading :=
  let pres : List (List (List SCell)) := [[]] ++ proclitics.map ([·]) ++
    (proclitics.flatMap fun p => proclitics.map fun q => [p, q])
  let sufs : List (List SCell) := [] :: enclitics
  (pres.flatMap fun pre => sufs.flatMap fun suf => [Al.none, Al.full, Al.silent].flatMap fun al =>
    -- الموصولةُ بلا همزةٍ لا تكون إلّا بعد سابقةٍ غيرِ همزة الاستفهام (آلْآنَ تُكتب بالمدّ)
    if al = .silent ∧ (pre = [] ∨ (pre.getLast?.map (·.head?.map (·.carrier.val))) = some (some 0)) then []
    else readingsAt w pre suf al).filter fun r => r.restore == w

/-- كلُّ قراءةٍ تُردّ إلى الكلمة بعينها — لكلّ كلمة (القارئُ لا يعيد إلّا ما ردُّه الكلمة). -/
theorem jidh_restores (w : List SCell) : ∀ r ∈ jidh w, r.restore = w := by
  intro r hr
  unfold jidh at hr
  simp only [List.mem_filter, beq_iff_eq] at hr
  exact hr.2

/-- الإعلالُ نزولًا عكسُ الصعود بعينه: أصلُ كلّ قراءةٍ يصعد بسلسلتها إلى جذعها — لكلّ كلمة. -/
theorem readingsAt_ascends (w : List SCell) (pre : List (List SCell)) (suf : List SCell) (al : Al) :
    ∀ r ∈ readingsAt w pre suf al, Ilal.ascend r.ilal (r.asl ++ r.suf) = some (r.stem ++ r.suf) := by
  intro r hr
  unfold readingsAt at hr
  revert hr
  split
  · simp
  · split
    · simp
    · split
      · simp
      · split
        · split
          · intro hr
            simp only [List.mem_singleton] at hr
            subst hr
            rfl
          · intro hr
            simp only [List.mem_filterMap] at hr
            obtain ⟨x, hx, hr⟩ := hr
            revert hr
            split
            · simp
            · rename_i asl hasl
              intro hr
              split at hr
              · simp only [Option.some.injEq] at hr
                subst hr
                simp only
                rw [peelSuffix_sound hasl]
                exact Ilal.descend_ascends _ _ x hx
              · simp at hr
        · simp

theorem jidh_ascends (w : List SCell) :
    ∀ r ∈ jidh w, Ilal.ascend r.ilal (r.asl ++ r.suf) = some (r.stem ++ r.suf) := by
  intro r hr
  unfold jidh at hr
  simp only [List.mem_filter, List.mem_flatMap] at hr
  obtain ⟨⟨pre, _, suf, _, al, _, hm⟩, _⟩ := hr
  revert hm
  split
  · simp
  · exact readingsAt_ascends w pre suf al r

/-! ## الجبرُ المغلق صعودًا ونزولًا

الزيادةُ عمليّاتٌ على الخانات (سابقةٌ متحرّكة، لاحقةٌ بعد تسوية الآخر إلى حالتها، أل)، والترخيصُ مغلقٌ تحتها
صعودًا؛ والقطعُ عكسُها بعينه نزولًا؛ وما صعد بالجبر ينزل بالقارئ (`jidh_complete`). -/

/-- الصعود ١: سابقةٌ متحرّكة على كلمةٍ مرخَّصة كلمةٌ مرخَّصة — لكلّ سابقةٍ وكلمة. -/
theorem prefix_licensed (p : SCell) (hp : p.state.val ≠ 3) (w : List SCell) (hw : licensed w = true) :
    licensed (p :: w) = true := by
  have hp' : p.isSukun = false := by simp [SCell.isSukun, hp]
  cases w with
  | nil => simp [licensed, noAdj, hp']
  | cons x t =>
    simp only [licensed, Bool.and_eq_true, Bool.not_eq_true'] at hw
    simp only [licensed, noAdj, hp', Bool.not_false, Bool.true_and, Bool.false_and]
    exact hw.2

/-- الصعود ٢: لاحقةٌ من الجدول بعد تسوية آخر الكلمة إلى حالتها المتحرّكة (`Jumla.suffix_licensed`)؛ والساكنةُ
(كَتَبْ + تُ) في `Filiyya.past_licensed`. الإلصاقُ يُردّ بعينه: -/
theorem peelPrefix_append (p s : List SCell) : peelPrefix p (p ++ s) = some s := by
  simp [peelPrefix, List.take_left', List.drop_left']

theorem peelSuffix_append (q s : List SCell) : peelSuffix q (s ++ q) = some s := by
  simp [peelSuffix, List.drop_left', List.take_left']

theorem dropAl_al (s : List SCell) (hne : s ≠ []) : dropAl .full (Marifa.al s) = some s := by
  have h2 : (Marifa.al s).drop 2 = s := by
    unfold Marifa.al Marifa.shamsi
    cases s with
    | nil => exact absurd rfl hne
    | cons x t =>
      simp only []
      split <;> rfl
  simp [dropAl, Marifa.hasAl_al s hne, h2]

/-- الجذعُ على قالبه بعد التسوية مهما كانت حالةُ آخره: `k` من معاني `setLast (fill (templ k) r) st` — لكلّ
قالبٍ سليم وجذرٍ وحالة، بلا شرطٍ على التنوين. -/
theorem mem_stemSenses (k : Nat) (hk : k < Wazn.N) (r : Wazn.Root) (hr : ∀ i, (r i).val ≠ 1) (st : Fin 4) :
    k ∈ stemSenses (setLast (Wazn.fill (Sarf.templ k) r) st) := by
  have hwf := Tabayun.templ_wf k hk
  have hne : Sarf.templ k ≠ [] := by
    intro h; have := hwf; rw [h] at this; exact absurd this.1 (by simp [Wazn.slots])
  have hmem : k ∈ onTemplates (setLast (Wazn.fill (Sarf.templ k) r) st) := by
    unfold onTemplates
    rw [List.mem_filter]
    refine ⟨List.mem_range.2 hk, ?_⟩
    rw [Shibh.setLast_setLast, setLast_fill _ r hne]
    exact Jiha.onTemplateRoot_fill k hwf r hr
  unfold stemSenses
  split
  · exact hmem
  · rename_i h; exact absurd (List.ne_nil_of_mem hmem) h

/-- الاكتمال: ما صعد بالجبر ينزل بالقارئ — لكلّ سابقةٍ من الجدول ولاحقةٍ من الجدول وقالبٍ سليم وجذرٍ لا ألفَ
فيه وحالةِ آخر: `jidh (p ++ setLast (fill (templ k) r) st ++ q)` فيه قراءةٌ سابقتُها `p` ولاحقتُها `q` وجذعُها
`setLast (fill (templ k) r) st` وقالبُها `k`. -/
theorem jidh_complete (p : List SCell) (hp : p ∈ proclitics) (q : List SCell) (hq : q ∈ enclitics)
    (k : Nat) (hk : k < Wazn.N) (r : Wazn.Root) (hr : ∀ i, (r i).val ≠ 1) (st : Fin 4)
    (hlic : Madd.pauseLicensed (setLast (Wazn.fill (Sarf.templ k) r) st) = true) :
    ∃ rd ∈ jidh (p ++ setLast (Wazn.fill (Sarf.templ k) r) st ++ q),
      rd.pre = [p] ∧ rd.al = .none ∧ rd.stem = setLast (Wazn.fill (Sarf.templ k) r) st ∧ rd.suf = q ∧
      rd.ilal = [] ∧ k ∈ rd.templates := by
  generalize hs : setLast (Wazn.fill (Sarf.templ k) r) st = s at hlic ⊢
  have hks : k ∈ stemSenses s := hs ▸ mem_stemSenses k hk r hr st
  have hsne : s ≠ [] := by
    intro h; rw [h] at hks
    have : stemSenses [] = [] := by decide
    rw [this] at hks; exact absurd hks (List.not_mem_nil)
  refine ⟨⟨[p], .none, s, q, s, [], stemSenses s⟩, ?_, rfl, rfl, rfl, rfl, rfl, hks⟩
  unfold jidh
  simp only [List.mem_filter, List.mem_flatMap]
  refine ⟨⟨[p], ?_, q, ?_, .none, by simp, ?_⟩, by simp [Reading.restore, withAl]⟩
  · simp only [List.mem_append, List.mem_map, List.mem_cons]
    exact Or.inl (Or.inr ⟨p, hp, rfl⟩)
  · exact List.mem_cons_of_mem _ hq
  · simp only [reduceCtorEq, false_and, ite_false, readingsAt, List.flatten_cons, List.flatten_nil,
      List.append_nil]
    rw [List.append_assoc, peelPrefix_append]
    simp only [peelSuffix_append, dropAl]
    have hts : stemSenses s ≠ [] := List.ne_nil_of_mem hks
    simp [hsne, hts, hlic]

/-- الاكتمالُ بالإعلال: ما صعد بقاعدةٍ من أصلٍ على قالبٍ ينزل بالقارئ — لكلّ قالبٍ سليم وجذرٍ وحالةٍ وقاعدةٍ
وموضع: إن كان الجذعُ الظاهر `w` مرخَّصًا ولا قالبَ له مباشرةً، ففي `jidh w` قراءةٌ أصلُها الأصلُ وسلسلتُها
القاعدةُ وقالبُها `k`. -/
theorem jidh_complete_ilal (k : Nat) (hk : k < Wazn.N) (r : Wazn.Root) (hr : ∀ i, (r i).val ≠ 1) (st : Fin 4)
    (ρ : Ilal.Rule) (i : Nat) (w : List SCell) (hi : i ∈ Ilal.positions ρ w.length)
    (hup : Ilal.apply ρ (setLast (Wazn.fill (Sarf.templ k) r) st) i = some w)
    (hlic : Madd.pauseLicensed w = true) (hno : stemSenses w = []) :
    ∃ rd ∈ jidh w, rd.pre = [] ∧ rd.al = .none ∧ rd.stem = w ∧ rd.suf = [] ∧
      rd.asl = setLast (Wazn.fill (Sarf.templ k) r) st ∧ rd.ilal = [(ρ, i)] ∧ k ∈ rd.templates := by
  generalize hs : setLast (Wazn.fill (Sarf.templ k) r) st = u at hup ⊢
  have hku : k ∈ stemSenses u := hs ▸ mem_stemSenses k hk r hr st
  have hwne : w ≠ [] := by
    intro h
    simp only [Ilal.apply, Option.map_eq_some_iff] at hup
    obtain ⟨v, hv, hw⟩ := hup
    have := Ilal.up_length ρ _ v hv
    rw [h] at hw
    have := congrArg List.length hw
    rw [List.length_append] at this
    simp only [List.length_nil] at this; omega
  refine ⟨⟨[], .none, w, [], u, [(ρ, i)], stemSenses u⟩, ?_, rfl, rfl, rfl, rfl, rfl, rfl, hku⟩
  unfold jidh
  simp only [List.mem_filter, List.mem_flatMap]
  refine ⟨⟨[], by simp, [], by simp, .none, by simp, ?_⟩, by simp [Reading.restore, withAl]⟩
  simp only [reduceCtorEq, false_and, ite_false, readingsAt, List.flatten_nil]
  have h1 : peelPrefix [] w = some w := peelPrefix_append [] w
  have h2 : peelSuffix [] w = some w := by simpa using peelSuffix_append [] w
  simp only [h1, h2, dropAl, hwne, hlic, hno, ne_eq, not_false_eq_true, and_self, ite_true,
    not_true_eq_false, ite_false, List.mem_filterMap, List.append_nil]
  refine ⟨([(ρ, i)], u), Ilal.descend_complete ρ u w i w.length hi hup, ?_⟩
  have h3 : peelSuffix [] u = some u := by simpa using peelSuffix_append [] u
  simp [h3, List.ne_nil_of_mem hku]

def walard : List SCell := [c 27 0, c 23 3, c 0 0, c 10 3, c 15 1]                 -- وَلْأَرْضِ (صورةُ الشهادة)
def alard : List SCell := [c 0 0, c 23 3, c 0 0, c 10 3, c 15 2]                   -- أَلْأَرْضُ
def washshams : List SCell := [c 27 0, c 13 3, c 13 0, c 24 3, c 12 1]             -- وَشَّمْسِ
def rabbi : List SCell := [c 10 0, c 2 3, c 2 1]                                    -- رَبِّ
def kadhdhabu : List SCell := [c 22 0, c 9 3, c 9 0, c 2 2, c 27 3]                 -- كَذَّبُو
def tajalu : List SCell := [c 3 0, c 5 3, c 18 0, c 23 2, c 27 3]                   -- تَجْعَلُو
def bikitabihim : List SCell := [c 2 1, c 22 1, c 3 0, c 1 3, c 2 1, c 26 1, c 24 3] -- بِكِتَابِهِمْ
def wajada : List SCell := [c 27 0, c 5 0, c 8 0]                                   -- وَجَدَ
def fariqun : List SCell := [c 20 0, c 10 1, c 28 3, c 21 2, c 25 3]                -- فَرِيقٌ (صورةُ الشهادة)

/-- وَلْأَرْضِ: و + أل موصولةً + أَرْض على فَعْلٍ؛ أَلْأَرْضُ: أل بهمزتها؛ وَشَّمْسِ: أل موصولةٌ شمسيّة. -/
theorem jidh_witnesses_al :
    (jidh walard).map (fun r => (r.pre.length, r.al, r.stem, r.templates)) =
      [(1, .silent, [c 0 0, c 10 3, c 15 1], [29])] ∧
    (jidh alard).map (fun r => (r.pre.length, r.al, r.templates)) = [(0, .full, [29])] ∧
    (jidh washshams).map (fun r => (r.pre.length, r.al, r.stem, r.templates)) =
      [(1, .silent, [c 13 0, c 24 3, c 12 1], [29])] := by
  refine ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩

/-- رَبِّ: مجرورٌ يُقرأ على فَعْلٍ بعد التسوية؛ وَجَدَ: فعلٌ أو مصدرٌ بعد التسوية (0، 36) — التعدّدُ يُقرأ والقرينةُ
تفصل. -/
theorem jidh_witnesses_case :
    (jidh rabbi).map (·.templates) = [[29]] ∧ (jidh wajada).map (·.templates) = [[0, 36]] := by
  refine ⟨by decide +kernel, by decide +kernel⟩

/-- كَذَّبُوا: قراءتان على الخانة بلا إعلال (فَعَّلَ + واو الجماعة، أو كَ + الذَّبُو) وأربعٌ بالإعلال (كَ + الذَّبُ +
واو الجماعة بأصلٍ أجوف أو ناقص) — التعدّدُ يُقرأ والقرينةُ تفصل؛ تَجْعَلُوا: يَفْعَلُ بردّ الصدر + واو؛
بِكِتَابِهِمْ: ب + كِتَاب + هِمْ. -/
theorem jidh_witnesses_affix :
    (jidh kadhdhabu).map (fun r => (r.al, r.suf, r.ilal.length, r.templates)) =
      [(.none, [c 27 3], 0, [12]), (.silent, [], 0, [2]), (.silent, [c 27 3], 2, [0, 36]),
       (.silent, [c 27 3], 2, [0, 36]), (.silent, [c 27 3], 1, [2]), (.silent, [c 27 3], 1, [2])] ∧
    (jidh tajalu).map (fun r => (r.stem, r.suf, r.templates)) =
      [([c 3 0, c 5 3, c 18 0, c 23 2], [c 27 3], [4])] ∧
    (jidh bikitabihim).map (fun r => (r.pre.length, r.suf.length, r.templates)) = [(1, 2, [35, 41, 93])] := by
  refine ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩


def kuntum : List SCell := [c 22 2, c 25 3, c 3 2, c 24 3]   -- كُنْتُمْ
def kana : List SCell := [c 22 0, c 1 3, c 25 0]             -- كَانَ
def daaw : List SCell := [c 8 0, c 18 0, c 27 3]             -- دَعَوْا (صورةُ الشهادة)
def jaa : List SCell := [c 5 0, c 1 3, c 0 0]                -- جَاءَ

/-- الإعلالُ نزولًا: قَالَ وكَانَ وجَاءَ بقلب العين (أصلان: واويٌّ ويائيّ) على فَعَلَ؛ قُلْ وكُنْتُمْ بخطوتين (قلبٌ ثمّ
حذفٌ ملزَم)؛ دَعَا بقلب اللام؛ دَعَوْا بحذف اللام المضمومة قبل واو الجماعة. -/
theorem jidh_witnesses_ilal_qalb :
    (jidh Ilal.qala).map (fun r => (r.asl, r.ilal, r.templates)) =
      [(Ilal.qawala, [(.qalbAyn, 0)], [0, 36]), ([c 21 0, c 28 0, c 23 0], [(.qalbAyn, 0)], [0, 36])] ∧
    (jidh kana).map (fun r => (r.asl, r.ilal)) =
      [([c 22 0, c 27 0, c 25 0], [(.qalbAyn, 0)]), ([c 22 0, c 28 0, c 25 0], [(.qalbAyn, 0)])] ∧
    (jidh jaa).map (fun r => (r.asl, r.templates)) =
      [([c 5 0, c 27 0, c 0 0], [0, 36]), ([c 5 0, c 28 0, c 0 0], [0, 36])] ∧
    (jidh Ilal.daa).map (fun r => (r.asl, r.ilal)) =
      [(Ilal.daawa, [(.qalbLam, 1)]), ([c 8 0, c 18 0, c 28 0], [(.qalbLam, 1)])] := by
  refine ⟨by decide +kernel, by decide +kernel, by decide +kernel, by decide +kernel⟩

theorem jidh_witnesses_ilal_hadhf :
    (jidh Ilal.qul).map (fun r => (r.asl, r.ilal, r.templates)) =
      [(Ilal.qawal, [(.qalbAyn, 0), (.hadhfAynU, 0)], [0, 36]),
       ([c 21 0, c 28 0, c 23 3], [(.qalbAyn, 0), (.hadhfAynU, 0)], [0, 36])] ∧
    (jidh kuntum).map (fun r => (r.stem, r.suf, r.asl, r.ilal)) =
      [([c 22 2, c 25 3], [c 3 2, c 24 3], [c 22 0, c 27 0, c 25 3], [(.qalbAyn, 0), (.hadhfAynU, 0)]),
       ([c 22 2, c 25 3], [c 3 2, c 24 3], [c 22 0, c 28 0, c 25 3], [(.qalbAyn, 0), (.hadhfAynU, 0)])] ∧
    (jidh daaw).map (fun r => (r.stem, r.suf, r.asl, r.ilal)) =
      [([c 8 0, c 18 0, c 27 3], [], [c 8 0, c 18 0, c 27 3], []),
       ([c 8 0, c 18 0], [c 27 3], [c 8 0, c 18 0, c 27 2], [(.hadhfLam, 1)]),
       ([c 8 0, c 18 0], [c 27 3], [c 8 0, c 18 0, c 28 2], [(.hadhfLam, 1)])] := by
  refine ⟨by decide +kernel, by decide +kernel, by decide +kernel⟩

end Slge.Jidh
