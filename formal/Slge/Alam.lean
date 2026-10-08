import Slge.Jidh
import Slge.Sarf
import Slge.AlamTable

/-!
# العلمُ ولفظُ الجلالة — لفظٌ منفردٌ بلا قياس (بتوقيع المالك)

لا قالبَ ولا قياس: الاسمُ علمٌ موسومٌ بعينه من المودَع الموقَّع (`AlamTable`)، يُقرأ بسوابقه (من
`Jidh.proclitics`) وحالةِ آخره، ويُردّ بعينه (`ilm_restores`). لفظُ الجلالة صورُه ثلاثٌ مسمّاة لكلّ حالة —
ابتداءً بهمزة الوصل، وبعد سابقةٍ بلا همزة، ومدًّا بعد تاء القسم أو همزة الاستفهام — واللهمّ لفظٌ منفرد
(`jalalaForms`، عشرٌ: `jalala_forms_count`). الحالةُ من الآخر (`caseOf`): الممنوعُ جرُّه بالفتح فالفتحُ
«نصب/جرّ» — وهو جرُّ `Sarf.mamnuJarr` بعينه (`mamnu_jarr_is_fatha`)؛ والمنصرفُ بالتنوين؛ والمقصورُ لا تُقرأ
حالتُه. شواهدُ على المودَع بـ`decide`.
-/

namespace Slge.Alam

open Slge.Categories (c)

/-- الحالاتُ المقروءة: 0 رفع، 1 نصب، 2 جرّ، 3 نصب/جرّ، 4 لا تقرؤه الخانة. -/
abbrev Case := Nat

/-- الصرف: 0 ممنوع، 1 منصرف، 2 مقصور، 3 غيرُ مشهود الجرّ. -/
def caseOf (sarf lastState : Nat) (tanwin : Bool) : Case :=
  if sarf == 2 || lastState == 3 then 4
  else if lastState == 2 then 0
  else if lastState == 1 then 2
  else if sarf == 0 || (sarf == 3 && !tanwin) then 3
  else 1

/-- جرُّ الممنوع بالفتح هو صورتُه المنصوبة بعينها (`Sarf.mamnuJarr = setLast 0`)؛ فقراءةُ الفتح «نصب/جرّ». -/
theorem setLast_append_single : ∀ (h : List SCell) (x : SCell) (st : Fin 4),
    Zuruf.setLast (h ++ [x]) st = h ++ [⟨x.carrier, st⟩]
  | [], _, _ => rfl
  | [_], _, _ => rfl
  | _ :: z :: t, x, st => by
    simp only [List.cons_append, Zuruf.setLast]
    exact congrArg _ (setLast_append_single (z :: t) x st)

theorem mamnu_jarr_is_fatha (h : List SCell) (k : Fin 29) :
    Sarf.mamnuJarr (h ++ [⟨k, ⟨0, by decide⟩⟩]) = h ++ [⟨k, ⟨0, by decide⟩⟩] ∧
    caseOf 0 0 false = 3 :=
  ⟨setLast_append_single h _ _, rfl⟩

/-- صورُ لفظ الجلالة: (اسمُ الصورة، الخانات). 0 ابتداءً، 1 بعد سابقة، 2 مدًّا، 3 اللهمّ. -/
def jalalaForms : List (Nat × List SCell) :=
  ([2, 0, 1].flatMap fun st =>
    let base := AlamTable.jalalaHead ++ [⟨⟨AlamTable.jalalaLast, by decide⟩, ⟨st % 4, Nat.mod_lt _ (by decide)⟩⟩]
    [(0, AlamTable.jalalaInitial ++ base), (1, base), (2, AlamTable.jalalaMadd ++ base)]) ++
  [(3, AlamTable.lahumma)]

theorem jalala_forms_count : jalalaForms.length = 10 := by decide

/-- قراءةُ علم: السوابقُ، رقمُ الصفّ في الجدول (أو 1000+ لصور الجلالة)، الصورةُ، الحالة. -/
structure Ilm where
  pre : List (List SCell)
  item : Nat
  surface : List SCell
  case : Case
  deriving DecidableEq, Repr

def restore (m : Ilm) : List SCell := m.pre.flatten ++ m.surface

/-- السوابقُ: سوابقُ الجذع وتاءُ القسم (`Rawabit.particles` المتّصلة: تَاللهِ). -/
def proclitics : List (List SCell) := Jidh.proclitics ++ [[c 3 0]]

def pres : List (List (List SCell)) :=
  [[]] ++ proclitics.map ([·]) ++ (proclitics.flatMap fun p => proclitics.map fun q => [p, q])

def isTa (pre : List (List SCell)) : Bool :=
  match pre.getLast? with
  | some [x] => x.carrier.val == 3 || x.carrier.val == 0
  | _ => false

def isHamza (pre : List (List SCell)) : Bool :=
  match pre.getLast? with
  | some [x] => x.carrier.val == 0
  | _ => false

/-- لفظُ الجلالة في موضعه: الهمزةُ ابتداءً فقط، والحذفُ بعد سابقةٍ غيرِ الهمزة، والمدُّ بعد تاء القسم أو الهمزة.
يعيد (رقمَ الصورة، الحالة). -/
def jalalaRead (pre : List (List SCell)) (rest : List SCell) : List (Nat × Case) :=
  jalalaForms.filterMap fun (form, cells) =>
    if cells != rest then none
    else if form == 0 && !pre.isEmpty then none
    else if form == 1 && (pre.isEmpty || isHamza pre) then none
    else if form == 2 && !isTa pre then none
    else some (1000 + form,
      if form == 3 then 4 else caseOf 1 ((rest.getLast?.map (·.state.val)).getD 3) false)

/-- العلمُ في موضعه: الرأسُ ثمّ الآخرُ بحالةٍ تُقرأ، والتنوينُ للمنصرف وحدَه. يعيد (رقمَ الصفّ، الحالة). -/
def alamRead (rest : List SCell) : List (Nat × Case) :=
  (List.range AlamTable.table.length).filterMap fun i =>
    match AlamTable.table[i]? with
    | none => none
    | some (head, last, fixed, _, sarf) =>
      let n := head.length + 1
      let tanwin := rest.length == n + 1 && rest.getLast? == some (c 25 3)
      let body := if tanwin then rest.take n else rest
      if body.length != n || body.take (n - 1) != head then none
      else match body.getLast? with
        | none => none
        | some x =>
          if x.carrier.val != last then none
          else if fixed != 4 && x.state.val != fixed then none
          else if tanwin && (sarf == 0 || sarf == 2) then none
          else some (i, caseOf sarf x.state.val tanwin)

/-- قراءاتُ الكلمة علمًا أو لفظَ جلالة: ما بعد السوابق صورةٌ موقَّعة. -/
def ilm (w : List SCell) : List Ilm :=
  (pres.filter (fun pre => pre.flatten.isPrefixOf w && pre.flatten.length < w.length)).flatMap fun pre =>
    (jalalaRead pre (w.drop pre.flatten.length) ++ alamRead (w.drop pre.flatten.length)).map
      fun (it, cs) => ⟨pre, it, w.drop pre.flatten.length, cs⟩

/-- كلُّ قراءةٍ تُردّ إلى الكلمة بعينها. -/
theorem ilm_restores {w : List SCell} {m : Ilm} (h : m ∈ ilm w) : restore m = w := by
  unfold ilm at h
  obtain ⟨pre, hpre, h⟩ := List.mem_flatMap.1 h
  have hp := (List.mem_filter.1 hpre).2
  simp only [Bool.and_eq_true, decide_eq_true_eq] at hp
  obtain ⟨⟨it, cs⟩, _, hm⟩ := List.mem_map.1 h
  subst hm
  unfold restore
  simp only
  exact List.prefix_iff_eq_append.1 (List.isPrefixOf_iff_prefix.1 hp.1)

/-! ## شواهد على المودَع -/

def allahu : List SCell := [c 0 0, c 23 3, c 23 0, c 26 2]            -- ءَلْلَهُ
def billahi : List SCell := [c 2 1, c 23 3, c 23 0, c 26 1]           -- بِلْلَهِ
def tallahi : List SCell := [c 3 0, c 1 3, c 23 3, c 23 0, c 26 1]    -- تَاْلْلَهِ
def ibrahima : List SCell := [c 0 1, c 2 3, c 10 0, c 1 3, c 26 1, c 28 3, c 24 0]  -- ءِبْرَاْهِيْمَ
def lutin : List SCell := [c 23 2, c 27 3, c 16 1, c 25 3]            -- لُوْطِنْ
def kataba : List SCell := [c 22 0, c 3 0, c 2 0]                      -- كَتَبَ

/-- ءَلْلَهُ قراءةٌ واحدة: ابتداءً، رفعًا؛ بِلْلَهِ بعد سابقةٍ جرًّا؛ تَاْلْلَهِ مدًّا بعد تاء القسم؛ اللهمّ لفظٌ منفرد. -/
theorem witness_jalala :
    ilm allahu = [⟨[], 1000, allahu, 0⟩] ∧
    (ilm billahi).any (fun m => m.pre == [[c 2 1]] && m.item == 1001 && m.case == 2) = true ∧
    (ilm tallahi).any (fun m => m.pre == [[c 3 0]] && m.item == 1002) = true ∧
    (ilm AlamTable.lahumma).any (fun m => m.item == 1003 && m.case == 4) = true := by decide +kernel

/-- إِبْرَاهِيمَ ممنوعٌ: الفتحُ نصبٌ أو جرّ؛ لُوطٍ منصرفٌ بالتنوين جرًّا؛ وكَتَبَ ليس علمًا. -/
theorem witness_alam :
    (ilm ibrahima).any (fun m => m.pre == [] && m.case == 3) = true ∧
    (ilm lutin).any (fun m => m.pre == [] && m.case == 2) = true ∧
    ilm kataba = [] := by decide +kernel

end Slge.Alam
