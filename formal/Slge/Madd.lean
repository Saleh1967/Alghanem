import Slge.Tabayun
import A116.Ternary

/-!
# المدود: المدُّ خانةٌ ساكنةٌ بعد حركتها، وأحكامُه من الخانة التالية والحدّ

* **حرفُ المدّ** على الخانات: ألفٌ ساكنةٌ بعد فتح، أو واوٌ ساكنةٌ بعد ضمّ، أو ياءٌ ساكنةٌ بعد كسر — وهو صنفُ `v`
  في التقطيع الثلاثيّ (`A116.Stages.K`): `kinds` تُسقط الخانات على `cv/v/c` كما تفعل البوّابة (`gate.licence.kind_of`)
  وتُطابَق بجدولها. فلا مدَّ في صدر كلمة (`kinds_head_not_v`) ولا مدّان متجاوران (`no_adjacent_madd`) — لكلّ كلمة.
* **الترخيصُ الثنائيُّ هو `binOK` على الأصناف** (`licensed_eq_binOK`: لكلّ كلمة)، و**المدُّ اللازم** (مدٌّ ثمّ ساكنٌ
  أصليّ) هو بالضبط ما يفصل الترخيصَ الثلاثيَّ عن الثنائيّ: كلمةٌ مرخَّصةٌ وصلًا فيها مدٌّ لازمٌ ⇔ ليست مرخَّصةً
  ثنائيًّا (`lazim_iff_not_binary`: لكلّ كلمة) — فالخمسُ والستّون صورةً «ثلاثيّةً فقط» في المصحف هي صورُ المدّ اللازم.
* **الأحكامُ من الخانة التالية والحدّ**: بعد المدّ همزةٌ في الكلمة ⇒ متّصل؛ ساكنٌ ⇒ لازم (مثقَّلٌ إن كان أوّلَ
  مضعَّف، مخفَّفٌ وإلّا)؛ المدُّ آخرَ الكلمة وبعدها كلمةٌ صدرُها همزة ⇒ منفصل (وصلًا)؛ قبل الخانة الأخيرة وقفًا ⇒
  عارضٌ للسكون (`arid_iff_pause`: الكلمةُ نفسُها طبيعيٌّ وصلًا وعارضٌ وقفًا)؛ وإلّا طبيعيّ. واللينُ واوٌ أو ياءٌ ساكنةٌ بعد
  فتحٍ قبل الأخيرة وقفًا. والصلةُ هاءٌ آخرَ الكلمة مضمومةٌ أو مكسورةٌ بين متحرّكين: كبرى إن صدرُ التالية همزة، وإلّا
  صغرى — تُقرأ من الهاء لا من حرفٍ مكتوب (صلةُ المصحف المختوم غيرُ مرسومة).
* **الحظرُ بالجدول**: الواوُ الساقطةُ لفظًا (أُولَئِكَ، أُولُو، أُولِي، أُولَاءِ، أُولَات) تُقرأ مدًّا بالخانة وليست مدًّا؛ الجدولُ
  يحجبها (`silent_waw_tabled`) — صفرُ المصحف المستدير لا خانةَ له.
ما ليس في الخانة — باسمه: المقادير (حركتان/أربع/ستّ) معلَنةٌ لا تُقرأ؛ الألفُ الخنجريّة والحروفُ الصغيرة ليست في
المدوّنة المختومة (ذَلِكَ بلا مدٍّ على الخانة)؛ مدُّ العوض (ألفُ التنوين بقيّةُ رسمٍ تُردّ في الغانم) ومدُّ البدل
(تسميةٌ للطبيعيّ بعد همزة — يُقرأ طبيعيًّا)؛ فواتحُ السور غيرُ مشكولةٍ فلا تدخل. القياسُ على مودَع المصحف في بايثون.
الحصرُ المُرسَل: شجرةٌ نصّيّة وعلاماتُ ضبطٍ عثمانيّة لا خانةَ لها — لم يُدخَل منه شيء؛ ودخل معناه على الخانات.
-/

namespace Slge.Madd

open Slge.Categories (c)
open A116.Stages (K Syl Lead)

/-! ## الأصنافُ الثلاثة على الخانات -/

/-- صنفُ الخانة بعد سابقتها: متحرّكٌ `cv`؛ مدٌّ `v` (ألفٌ بعد فتحٍ، واوٌ بعد ضمٍّ، ياءٌ بعد كسرٍ — ساكنةً)؛ وإلّا ساكنٌ `c`. -/
def isMaddAfter (q x : SCell) : Bool :=
  (x.carrier.val == 1 && q.state.val == 0) || (x.carrier.val == 27 && q.state.val == 2) ||
    (x.carrier.val == 28 && q.state.val == 1)

def kindOf (p : Option SCell) (x : SCell) : K :=
  if x.state.val = 3 then
    match p with
    | none => K.c
    | some q => if isMaddAfter q x then K.v else K.c
  else K.cv

def kindsAux : Option SCell → List SCell → List K
  | _, [] => []
  | p, x :: t => kindOf p x :: kindsAux (some x) t

/-- أصنافُ الكلمة (مرآةُ `gate.licence.kind_of`). -/
def kinds (w : List SCell) : List K := kindsAux none w

def continueLicensed (w : List SCell) : Bool := A116.Ternary.continueB (kinds w)
def pauseLicensed (w : List SCell) : Bool := A116.Ternary.pauseB (kinds w)

theorem kindOf_cv (p : Option SCell) (x : SCell) : (kindOf p x == K.cv) = !x.isSukun := by
  unfold kindOf SCell.isSukun
  by_cases h : x.state.val = 3
  · simp only [h, ite_true, beq_self_eq_true, Bool.not_true]
    cases p with
    | none => rfl
    | some q => cases hm : isMaddAfter q x <;> simp [hm]
  · simp [h]

/-- لا مدَّ في صدر كلمة: الصدرُ متحرّكٌ أو ساكنٌ لا مدّ. -/
theorem kinds_head_not_v (w : List SCell) : (kinds w).head? ≠ some K.v := by
  cases w with
  | nil => simp [kinds, kindsAux]
  | cons x t =>
    simp only [kinds, kindsAux, List.head?_cons, ne_eq, Option.some.injEq]
    unfold kindOf
    split <;> simp

def noVV : List K → Bool
  | K.v :: K.v :: _ => false
  | _ :: t => noVV t
  | [] => true

theorem kindOf_v_sukun {p : Option SCell} {x : SCell} (h : kindOf p x = K.v) : x.state.val = 3 := by
  unfold kindOf at h
  by_cases hx : x.state.val = 3
  · exact hx
  · simp only [hx, ite_false] at h; exact absurd h (by decide)

theorem isMaddAfter_sukun {x y : SCell} (hx : x.state.val = 3) : isMaddAfter x y = false := by
  unfold isMaddAfter
  simp [hx]

theorem kindOf_after_sukun {x y : SCell} (hx : x.state.val = 3) : kindOf (some x) y ≠ K.v := by
  unfold kindOf
  split
  · simp [isMaddAfter_sukun hx]
  · simp

theorem noVV_kindsAux : ∀ (p : Option SCell) (w : List SCell), noVV (kindsAux p w) = true
  | _, [] => rfl
  | p, [x] => by simp only [kindsAux]; cases kindOf p x <;> rfl
  | p, x :: y :: t => by
    have ih := noVV_kindsAux (some x) (y :: t)
    simp only [kindsAux] at ih ⊢
    cases hk : kindOf p x with
    | v =>
      have hx := kindOf_v_sukun hk
      have hy := kindOf_after_sukun (y := y) hx
      cases hk2 : kindOf (some x) y with
      | v => exact absurd hk2 hy
      | cv => simpa [noVV, hk2] using ih
      | c => simpa [noVV, hk2] using ih
    | cv => simpa [noVV] using ih
    | c => simpa [noVV] using ih

/-- لا مدّان متجاوران: المدُّ ساكنٌ، والمدُّ بعده يطلب حركةً قبله — لكلّ كلمة. -/
theorem no_adjacent_madd (w : List SCell) : noVV (kinds w) = true := noVV_kindsAux none w

/-! ## الثنائيُّ `binOK` على الأصناف، واللازمُ فاصلُه عن الثلاثيّ -/

theorem noPair_kindsAux : ∀ (p : Option SCell) (w : List SCell),
    A116.Ternary.noPair (kindsAux p w) = Slge.noAdj w
  | _, [] => rfl
  | _, [_] => rfl
  | p, x :: y :: t => by
    have ih := noPair_kindsAux (some x) (y :: t)
    simp only [kindsAux] at ih ⊢
    simp only [A116.Ternary.noPair, Slge.noAdj, kindOf_cv, ih]
    cases x.isSukun <;> cases y.isSukun <;> rfl

/-- الترخيصُ الثنائيُّ هو `binOK` على الأصناف: لكلّ كلمة. -/
theorem licensed_eq_binOK (w : List SCell) : Slge.licensed w = A116.Ternary.binOK (kinds w) := by
  cases w with
  | nil => rfl
  | cons x t =>
    simp only [Slge.licensed, kinds, kindsAux, A116.Ternary.binOK, kindOf_cv]
    rw [← noPair_kindsAux none (x :: t)]
    simp [kindsAux]

/-- مدٌّ ثمّ ساكن: المدُّ اللازم على الأصناف. -/
def hasVC : List K → Bool
  | K.v :: K.c :: _ => true
  | _ :: t => hasVC t
  | [] => false

/-- على الأصناف: في سلسلةٍ مرخَّصةٍ وصلًا، مدٌّ ثمّ ساكن ⇔ ليست مقبولةً ثنائيًّا. -/
theorem hasVC_iff_not_binOK (k : List K) (h : A116.Ternary.continueB k = true) :
    hasVC k = true ↔ A116.Ternary.binOK k = false := by
  unfold A116.Ternary.continueB at h
  split at h
  · rename_i l ss hp
    simp only [List.all_eq_true, Bool.not_eq_true'] at h
    have hss := h
    have hflat := A116.Stages.flat_parse hp
    rw [← hflat]
    simp only [A116.Stages.flat, A116.Stages.Lead.atoms, List.nil_append]
    clear hp hflat
    induction ss with
    | nil => simp [hasVC, A116.Ternary.binOK]
    | cons s t ih =>
      have hs := hss s (List.mem_cons_self ..)
      have ht : ∀ x ∈ t, A116.Ternary.pauseOnly x = false :=
        fun x hx => hss x (List.mem_cons_of_mem _ hx)
      have ih' := ih ht
      cases t with
      | nil => cases s <;> simp_all [A116.Stages.Syl.atoms, A116.Stages.Syl.coda, hasVC,
          A116.Ternary.binOK, A116.Ternary.noPair, A116.Ternary.pauseOnly]
      | cons s' t' =>
        have hs' := ht s' (List.mem_cons_self ..)
        cases s <;> cases s' <;> simp_all [A116.Stages.Syl.atoms, A116.Stages.Syl.coda, hasVC,
          A116.Ternary.binOK, A116.Ternary.noPair, A116.Ternary.pauseOnly]
  · simp at h

/-- اللازمُ فاصلُ الثلاثيّ عن الثنائيّ: في كلمةٍ مرخَّصةٍ وصلًا، مدٌّ لازمٌ ⇔ غيرُ مرخَّصةٍ ثنائيًّا — لكلّ كلمة. -/
theorem lazim_iff_not_binary (w : List SCell) (h : continueLicensed w = true) :
    hasVC (kinds w) = true ↔ Slge.licensed w = false := by
  rw [licensed_eq_binOK]
  exact hasVC_iff_not_binOK (kinds w) h

/-! ## القارئ -/

inductive Kind where
  | tabii | muttasil | munfasil | lazimThaqil | lazimKhafif | arid | lin | silaSughra | silaKubra | silent
  deriving DecidableEq, Repr

def nextHamza (next : List SCell) : Bool :=
  match next.head? with
  | some x => x.carrier.val == 0
  | none => false

/-- حكمُ حرف المدّ في الموضع `i` من الخانة التالية والحدّ: `pause` وقفٌ على الكلمة، و`next` الكلمةُ التالية وصلًا. -/
def maddAt (w : List SCell) (i : Nat) (next : List SCell) (pause : Bool) : Option Kind :=
  if (kinds w)[i]? ≠ some K.v then none
  else match w[i + 1]? with
    | none => some (if nextHamza next && !pause then .munfasil else .tabii)
    | some x =>
      if x.carrier.val = 0 then some .muttasil
      else if x.state.val = 3 then
        some (match w[i + 2]? with
          | some y => if y.carrier = x.carrier then .lazimThaqil else .lazimKhafif
          | none => .lazimKhafif)
      else if pause && i + 2 = w.length then some .arid
      else some .tabii

/-- اللين: واوٌ أو ياءٌ ساكنةٌ بعد فتحٍ قبل الأخيرة وقفًا. -/
def linAt (w : List SCell) (i : Nat) (pause : Bool) : Bool :=
  pause && i + 2 == w.length && (match w[i]?, (if i = 0 then none else w[i - 1]?) with
    | some x, some p => (x.carrier.val == 27 || x.carrier.val == 28) && x.state.val == 3 && p.state.val == 0
    | _, _ => false)

/-- الصلة: هاءٌ آخرَ الكلمة مضمومةٌ أو مكسورةٌ بعد متحرّكٍ، وبعدها كلمة: كبرى إن صدرُها همزة. -/
def sila (w next : List SCell) : Option Kind :=
  match w.reverse with
  | h :: p :: _ =>
    if h.carrier.val = 26 && (h.state.val = 2 || h.state.val = 1) && p.state.val ≠ 3 && next ≠ [] then
      some (if nextHamza next then .silaKubra else .silaSughra)
    else none
  | _ => none

/-- الواوُ الساقطةُ لفظًا: أُولَئِكَ، أُولُو، أُولِي، أُولَاءِ، أُولَات (الصورُ القانونيّة بلا الفارقة). -/
def silentWaw : List (List SCell) := [
  [c 0 2, c 27 3, c 23 0, c 0 1, c 22 0],          -- أُولَئِكَ
  [c 0 2, c 27 3, c 23 2, c 27 3],                 -- أُولُو
  [c 0 2, c 27 3, c 23 1, c 28 3],                 -- أُولِي
  [c 0 2, c 27 3, c 23 0, c 1 3, c 0 1],           -- أُولَاءِ
  [c 0 2, c 27 3, c 23 0, c 1 3, c 3 2]]           -- أُولَاتُ

/-- مدودُ الكلمة: (الموضع، الحكم) — وقفًا يُردّ التنوين؛ والواوُ الساقطةُ محجوبةٌ بالجدول، واللينُ والصلةُ ملحقان. -/
def madd (w₀ next : List SCell) (pause : Bool) : List (Nat × Kind) :=
  let w := if pause then Marifa.dropTanwin w₀ else w₀
  let hits := (List.range w.length).filterMap fun i =>
    if silentWaw.contains w && i = 1 then some (i, Kind.silent)
    else match maddAt w i next pause with
      | some k => some (i, k)
      | none => if linAt w i pause then some (i, .lin) else none
  match sila w next with
  | some k => hits ++ [(w.length - 1, k)]
  | none => hits

/-- الكلمةُ نفسُها: طبيعيٌّ وصلًا وعارضٌ وقفًا — لكلّ كلمةٍ مدُّها قبل الأخيرة وآخرُها متحرّكٌ غيرُ همزة. -/
theorem arid_iff_pause (w : List SCell) (i : Nat) (hv : (kinds w)[i]? = some K.v) (x : SCell)
    (hx : w[i + 1]? = some x) (hlast : i + 2 = w.length) (hh : x.carrier.val ≠ 0) (hs : x.state.val ≠ 3)
    (next : List SCell) :
    maddAt w i next true = some .arid ∧ maddAt w i next false = some .tabii := by
  unfold maddAt
  simp [hv, hx, hh, hs, hlast]

/-- المنفصلُ من صدر التالية: المدُّ آخرَ الكلمة منفصلٌ وصلًا ⇔ التاليةُ صدرُها همزة — لكلّ كلمة. -/
theorem munfasil_iff_next_hamza (w next : List SCell) (i : Nat) (hv : (kinds w)[i]? = some K.v)
    (hlast : w[i + 1]? = none) :
    maddAt w i next false = some .munfasil ↔ nextHamza next = true := by
  unfold maddAt
  simp only [hv, hlast, ne_eq, not_true_eq_false, ite_false, Bool.not_false, Bool.and_true,
    Option.some.injEq]
  cases nextHamza next <;> simp

theorem silent_waw_tabled : silentWaw.all (fun w => (kinds w)[1]? == some K.v) = true := by decide

def qalu : List SCell := [c 21 0, c 1 3, c 23 2, c 27 3]                         -- قَالُو (بلا الفارقة)
def assama : List SCell := [c 0 0, c 12 3, c 12 0, c 24 0, c 1 3, c 0 1]        -- اَسَّمَاءِ
def addallin : List SCell :=
  [c 0 0, c 15 3, c 15 0, c 1 3, c 23 3, c 23 1, c 28 3, c 25 0]                 -- اَضَّالِّينَ
def alan : List SCell := [c 0 0, c 1 3, c 23 3, c 0 0, c 1 3, c 25 0]            -- ءَالْءَانَ
def alamin : List SCell :=
  [c 0 0, c 23 3, c 18 0, c 1 3, c 23 0, c 24 1, c 28 3, c 25 0]                 -- اَلْعَالَمِينَ
def khawf : List SCell := [c 7 0, c 27 3, c 20 2, c 25 3]                        -- خَوْفٌ
def innahu : List SCell := [c 0 1, c 25 3, c 25 0, c 26 2]                       -- إِنَّهُ
def kana : List SCell := [c 22 0, c 1 3, c 25 0]                                 -- كَانَ
def illa : List SCell := [c 0 1, c 23 3, c 23 0, c 1 3]                          -- إِلَّا
def bima : List SCell := [c 2 1, c 24 0, c 1 3]                                  -- بِمَا
def unzila : List SCell := [c 0 2, c 25 3, c 11 1, c 23 0]                       -- أُنْزِلَ
def amanu : List SCell := [c 0 0, c 1 3, c 24 0, c 25 2, c 27 3]                 -- ءَامَنُو
def ulaika : List SCell := [c 0 2, c 27 3, c 23 0, c 0 1, c 22 0]                -- أُولَئِكَ

/-- قَالُوا طبيعيّان؛ السَّمَاءِ متّصل؛ الضَّالِّينَ لازمٌ مثقَّل؛ ءَالْءَانَ لازمٌ مخفَّف؛ الْعَالَمِينَ وقفًا عارضٌ
ووصلًا طبيعيّ؛ خَوْفٌ وقفًا لين؛ إِنَّهُ كَانَ صلةٌ صغرى، إِنَّهُ إِلَّا كبرى؛ بِمَا أُنْزِلَ منفصل؛ ءَامَنُوا طبيعيّان (البدلُ
تسمية)؛ أُولَئِكَ واوُها محجوبة. والصورُ الثلاثيّةُ فقط (الضَّالِّينَ) مرخَّصةٌ وصلًا لا ثنائيًّا. -/
theorem madd_witnesses :
    madd qalu [] false = [(1, .tabii), (3, .tabii)] ∧ madd assama [] false = [(4, .muttasil)] ∧
    madd addallin [] false = [(3, .lazimThaqil), (6, .tabii)] ∧ madd alan [] false = [(1, .lazimKhafif), (4, .tabii)] ∧
    madd alamin [] true = [(3, .tabii), (6, .arid)] ∧ madd alamin [] false = [(3, .tabii), (6, .tabii)] ∧
    madd khawf [] true = [(1, .lin)] ∧ madd khawf [] false = [] ∧
    madd innahu kana false = [(3, .silaSughra)] ∧ madd innahu illa false = [(3, .silaKubra)] ∧
    madd bima unzila false = [(2, .munfasil)] ∧ madd bima kana false = [(2, .tabii)] ∧
    madd amanu [] false = [(1, .tabii), (4, .tabii)] ∧ madd ulaika [] false = [(1, .silent)] ∧
    Slge.licensed addallin = false ∧ hasVC (kinds addallin) = true ∧ Slge.licensed qalu = true := by decide

/-- الضَّالِّينَ مرخَّصةٌ وصلًا (ثلاثيًّا) وليست ثنائيًّا: صورةُ «الثلاثيّ فقط» هي صورةُ اللازم. -/
theorem addallin_ternary_only : continueLicensed addallin = true ∧ continueLicensed qalu = true := by
  constructor <;> decide +kernel

end Slge.Madd
