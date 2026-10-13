import Slge.Haja

/-!
# قانونُ التمام: الحاجةُ مرفوعةً من الخانة إلى الكلم — صدارةٌ وإغلاقٌ ووصل (ADR ٥٧)

قانونُ الحاجة في الغانم (`A116.Hajah`، بنصّ المالك «ويحكمها قانونُ الابتداء وقانونُ الوصل وقانونُ الوقف … وفق قانون
الاستنفاد بالحدّ الأدنى المكتمل») يقول على الخانات: الساكنُ يحتاج متحرّكًا قبله في مقطعه، والمقطعُ حدٌّ أدنى مكتمل،
والوصلُ وراثةٌ من حالةٍ واحدة. وهنا **رفعُه درجةً** إلى الكلم بتوقيع الحاجة (`Haja.needs`، مرسًى في ج3 والكتاب):

* **الحالة** (`St`): مكدَّسُ مجموعاتٍ من الحاجات المفتوحة بعدُ (كلُّ مجموعةٍ حاجاتُ كلمةٍ واحدة، غيرُ مرتَّبةٍ بينها:
  «تنصب الاسم وترفع الخبر» لا يقول أيُّهما أوّلًا)، وأقسامُ ما رُئي منذ أوّل الوحدة.
* **الخطوة** (`stepAll`): الكلمةُ تقضي حتمًا حاجةً من المجموعة العليا إن قدرت (الاسمُ والمضمرُ يقضيان «اسمًا»،
  والفعلُ «فعلًا»، وكلُّ كلمةٍ تبدأ «جزءَ كلام»؛ والجنسُ بعينه قبل «الجزء»: `pick`)؛ ثمّ حاجاتُها «قبل» تُقضى بما رُئي،
  و«بعد» تُفتح مجموعةً. فالحالةُ من كلّ قراءةٍ واحدة، والتعدّدُ من القراءات وحدَها.
* **الصدارة** (= الابتداءُ مرفوعًا؛ «ليس صلةً لما قبله» س9213): الشرطُ والاستفهامُ لا يقعان إلّا وقد أُغلق ما قبلهما،
  ولا يرى ما بعدهما ما قبلهما (`sadr_needs_closed`، `sadr_forgets`، `sadr_fresh`).
* **الإغلاق** (= الوقفُ مرفوعًا): الوحدةُ تامّةٌ إذا بلغ طريقٌ مكدَّسًا فارغًا (`tamm`)؛ وهو الإفادةُ التي جعلتها السلسلةُ
  شرطَ عدم الهذيان.
* **الوصل** (= وراثةٌ): ترخيصُ `a ++ b` هو ترخيصُ `b` من حالات `a` (`runAll_append`)، وما قبل الحدّ لا يصل إلى ما بعده
  إلّا عبر حالاته (`before_after`).
* **الحدُّ الأدنى المكتمل**: الكلمةُ الواحدةُ تامّةٌ إذا وفقط إذا لم تكن لها حاجةٌ «قبل» أو «بعد» (`minimal_complete`) — فالحرفُ وحده
  لا يتمّ أبدًا (`harf_alone_incomplete`).

المبرهَنُ خواصُّ هذا القانون على توقيعٍ منقول، لا اللغة؛ والقياسُ على المودَع في `TAMAM_INDEX.md`.
-/

namespace Slge.Tamam

open Haja

structure Tok where
  leaf : Mufrad
  bab : Bab
  deriving DecidableEq, Repr

structure St where
  stack : List (List Mahjuj)
  seen : List Mufrad
  deriving DecidableEq, Repr

def start : St := ⟨[], []⟩

/-- ما تقضيه الكلمة. -/
def fills (t : Tok) : Mahjuj → Bool
  | .ism => t.leaf == .ism || t.leaf == .mudmar
  | .fil => t.leaf == .fil
  | .juz => true

/-- الحاجةُ «قبل» تُقضى بما رُئي منذ أوّل الوحدة. -/
def qablOK (seen : List Mufrad) : Mahjuj → Bool
  | .ism => seen.contains .ism || seen.contains .mudmar
  | .fil => seen.contains .fil
  | .juz => !seen.isEmpty

def eraseAt : List Mahjuj → Nat → List Mahjuj
  | [], _ => []
  | _ :: xs, 0 => xs
  | x :: xs, n + 1 => x :: eraseAt xs n

/-- أيُّ حاجةٍ من المجموعة العليا تقضيها الكلمة: ما كان من جنسها بعينه (اسمٌ أو فعل) أوّلًا، ثمّ «جزءُ الكلام». -/
def pick (g : List Mahjuj) (t : Tok) : Option Nat :=
  match (List.range g.length).find? (fun i => g.getD i .juz != .juz && fills t (g.getD i .juz)) with
  | some i => some i
  | none => (List.range g.length).find? (fun i => fills t (g.getD i .juz))

/-- القضاءُ حتمًا لا اختيارًا: تقضي الكلمةُ ما تقدر عليه من المجموعة العليا (وتُرفع المجموعةُ إن فرغت)، وإلّا بقي
المكدَّس. -/
def fill (stack : List (List Mahjuj)) (t : Tok) : List (List Mahjuj) :=
  match stack with
  | [] => []
  | g :: rest =>
    match pick g t with
    | none => stack
    | some i =>
      let g' := eraseAt g i
      if g'.isEmpty then rest else g' :: rest

/-- ما رُئي مجموعةٌ بترتيبٍ ثابت (حرف، مضمر، فعل، اسم). -/
def addSeen (l : Mufrad) (seen : List Mufrad) : List Mufrad :=
  [Mufrad.harf, .mudmar, .fil, .ism].filter fun x => x == l || seen.contains x

/-- ما تفتحه الكلمة: حاجاتُها «بعد». وحاجةُ «أيٍّ» (المفسِّر، المتعلَّق، المشروط) لا يُلزمها القانونُ هنا: قد تُقضى
قبلُ أو بعدُ أو بمقدَّر — دَينٌ مسمًّى `AYY_NEEDS_NOT_ENFORCED`. -/
def opens (_seen : List Mufrad) (t : Tok) : List Mahjuj :=
  ((needs t.bab).filter fun h => h.jiha == .bad).map (·.ma)

def finish (seen0 : List Mufrad) (stack1 : List (List Mahjuj)) (t : Tok) : Option St :=
  if sadr t.bab && !stack1.isEmpty then none else
  let seen := if sadr t.bab then [] else seen0
  if !((needs t.bab).all fun h => h.jiha != .qabl || qablOK seen h.ma) then none else
  let o := opens seen t
  some ⟨if o.isEmpty then stack1 else o :: stack1, addSeen t.leaf seen⟩

/-- ذو الصدارة لا يقضي حاجةً قبله (ليس صلةً لما قبله)، وغيرُه يقضي ما يقدر عليه. -/
def stepAll (s : St) (t : Tok) : List St :=
  (finish s.seen (if sadr t.bab then s.stack else fill s.stack t) t).toList

/-- الكلمةُ بقراءاتها: الحالاتُ من كلّ حالةٍ بكلّ قراءة، بلا تكرار. -/
def stepSet (S : List St) (ts : List Tok) : List St :=
  (S.flatMap fun s => ts.flatMap fun t => stepAll s t).eraseDups

def runAll (S : List St) : List (List Tok) → List St
  | [] => S
  | w :: ws => runAll (stepSet S w) ws

def tamm (S : List St) : Bool := S.any (·.stack.isEmpty)

/-- الوصل: ترخيصُ `a ++ b` هو ترخيصُ `b` من حالات `a`. -/
theorem runAll_append (S : List St) (a b : List (List Tok)) :
    runAll S (a ++ b) = runAll (runAll S a) b := by
  induction a generalizing S with
  | nil => rfl
  | cons w ws ih => exact ih (stepSet S w)

/-- ما قبل الحدّ لا يصل إلى ما بعده إلّا عبر حالاته. -/
theorem before_after (a a' b : List (List Tok)) (S : List St) (h : runAll S a = runAll S a') :
    runAll S (a ++ b) = runAll S (a' ++ b) := by
  rw [runAll_append, runAll_append, h]

def Mufrad.all : List Mufrad := [.harf, .mudmar, .fil, .ism]

def toks : List Tok := Bab.all.flatMap fun b => Mufrad.all.map fun l => ⟨l, b⟩

/-- الحدُّ الأدنى المكتمل: الكلمةُ الواحدةُ (بقراءةٍ واحدة) تامّةٌ من الابتداء إذا وفقط إذا لم تكن لبابها حاجةٌ «قبل»
أو «بعد». -/
theorem minimal_complete :
    toks.all (fun t => tamm (runAll [start] [[t]]) == (needs t.bab).all (·.jiha == .ayy)) = true := by
  decide

/-- الحرفُ وحده لا يتمّ أبدًا. -/
theorem harf_alone_incomplete :
    toks.all (fun t => !t.bab.harf || !tamm (runAll [start] [[t]])) = true := by decide

/-- الصدارة: لا يقع الشرطُ أو الاستفهامُ وما قبله مفتوح؛ وبعده لا يُرى ما قبله. -/
theorem sadr_needs_closed (s : St) (t : Tok) (hs : sadr t.bab = true) (hne : s.stack ≠ []) :
    stepAll s t = [] := by
  cases s with
  | mk stack seen0 =>
    cases stack with
    | nil => exact absurd rfl hne
    | cons g rest => simp [stepAll, hs, finish]

/-- وبعده لا يُرى ما قبله: ما رُئي قبله لا أثرَ له. -/
theorem sadr_forgets (seen0 : List Mufrad) (t : Tok) (hs : sadr t.bab = true) :
    stepAll ⟨[], seen0⟩ t = stepAll start t := by
  simp [stepAll, hs, finish, start]

theorem sadr_fresh :
    toks.all (fun t => !sadr t.bab || (stepAll start t).all (fun s' => s'.seen == [t.leaf])) = true := by
  decide

/-- شواهدُ بأسماء أبوابها: «إنّ اسمٌ اسمٌ» تامّة؛ «إنّ اسمٌ» لا؛ «إنّ حرفُ جرٍّ اسمٌ اسمٌ» تامّة (الخبرُ مقدَّمًا)؛
والاستفهامُ بعد «إنّ اسمٌ» مرفوض؛ وحرفُ الجرّ وحده لا يتمّ، وبعد فعلٍ تامّ باسمه. -/
theorem witnesses :
    let inna : Tok := ⟨.harf, .mushabbaha⟩
    let ism : Tok := ⟨.ism, .mustaqill⟩
    let fil : Tok := ⟨.fil, .mustaqill⟩
    let jarr : Tok := ⟨.harf, .jarr⟩
    let hal : Tok := ⟨.harf, .istifham⟩
    tamm (runAll [start] [[inna], [ism], [ism]]) = true ∧
    tamm (runAll [start] [[inna], [ism]]) = false ∧
    tamm (runAll [start] [[inna], [jarr], [ism], [ism]]) = true ∧
    runAll [start] [[inna], [ism], [hal]] = [] ∧
    tamm (runAll [start] [[jarr]]) = false ∧
    tamm (runAll [start] [[fil], [jarr], [ism]]) = true := by decide

end Slge.Tamam
