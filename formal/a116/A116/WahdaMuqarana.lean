import A116.QismDaraja
import A116.Marakib
import A116.Mufrad
import A116.Field112

/-!
# مقارنةُ الوحدة بوحدة SLGE، وربطُ القسم بقسمة ج3 (ADR ١٠٩)

أمرُ المالك: «UNIT_IS_HUDUD_N_NOT_SLGE … اعمل مقارنة انت خبير رياضيات … ومراجعة الشخصية الإسلامية ج٣ بعمق … لعمل الربط
وفق افضل الممارسات».

**المصدر.** تعريفاتُ SLGE هنا **منسوخةٌ نصًّا** من ملفّات المالك كما قُرئت في الجلسة (مستودعُ SLGE نفسُه لم يُبلَغ؛ قُرئت نسختُها
في مجلّد `SLGE/` بمستودعٍ آخر للمالك، ولا يُستورد منه شيء):
* `Core.lean`: ‎`pair u r = tri(u+r) + r`‎، و‎`encS [] = 0`، `encS (a :: l) = 1 + pair a (encS l)`‎.
* `Ladder.lean`: ‎`cellEnc c s = mixEnc 1 4 c 0 s = 4c + s`‎ (فتحة 0، ضمّة 1، كسرة 2، سكون 3).
* `Category.lean`: ‎`roles ind tim = (ind && !tim, ind)`‎، و`kindOf`: ‎(true, _) ← اسم، (false, true) ← فعل، (false, false) ← حرف‎.

**ما يثبت هنا:**
١. **الخانة:** رقمُ SLGE للخانة ‎4c + s‎ بترتيب حوامله هو رقمُ مركب المخارج في `Marakib` بعينه، على الخانات الـ116 كلّها
   (`cell_slge_eq_makharij`).
٢. **الاقتران:** اقترانُ SLGE هو `Numbering.pair` بعينه (`pair_slge`)، و`encS` تباين (`encS_injective`).
٣. **الوحدة:** وحدةُ الغانم ‎`Hudud.n` = 11F + j‎ ووحدةٌ على أسلوب SLGE ‎P(F, j)‎ كلتاهما تباين (`Hudud.n_inj`، `nPair_injective`)،
   وبينهما ترجمةٌ محسوبة في الاتّجاهين (`tarjama_n`، `tarjama_aks`). **وكلتاهما تُسقط الرتبة** (`wahda_tusqit_rutba`): «عَلَى»
   و«عَلَا» وحدةٌ واحدة؛ والرتبةُ في `Hudud.certHadd` لا في الوحدة.
٤. **القسم:** قسمةُ ج3 (`Mufrad.qismOf` على الاستقلال والدلالة بالهيئة على الزمان) هي `kindOf ∘ roles` في SLGE بعينها
   (`j3_eq_slge`)؛ فالقسمُ من صفات المدلول لا من الخانات.
٥. **السلامة:** إن كان المرجعُ قسمةَ ج3 على صفاتٍ معطاة ولم تخطئ علامة، فمعيَّنُ القارئ قسمُ ج3 بعينه (`muayyan_j3`).

ومراسي ج3 (الشخصيّة ج3 المختومة): س373 القسمة، س375 حدُّ الاسم، س377 الضميرُ والحرف، س467 حدُّ الحرف — تُفحص في
`tests/test_qism_khanat4.py`.
-/

namespace A116.WahdaMuqarana

open A116 A116.Numbering A116.QismKhanat

/-! ## ١. الخانة -/

/-- ترتيبُ حوامل SLGE (`Ladder.lean`). -/
def slgeOrder : List Char := "ءهاعحغخقكجشيضلنرطدتزسصظذثفبمو".toList

/-- `SLGE.Ladder.cellEnc` منسوخًا: ‎mixEnc 1 4 c 0 s = (c·1 + 0)·4 + s‎. -/
def slgeCellEnc (c s : Nat) : Nat := (c * 1 + 0) * 4 + s

/-- رقمُ الخانة عند SLGE: موضعُ حاملها في ترتيبه، وحالتُها. -/
def slgeIndex (c : Cell) : Nat := slgeCellEnc (slgeOrder.idxOf (Field112.carrierChar c.carrier)) c.haraka.index

theorem slgeOrder_eq_makharij : slgeOrder = Makharij.placed16 := by decide

/-- **رقمُ SLGE للخانة هو رقمُ مركب المخارج** على الخانات كلّها. -/
theorem cell_slge_eq_makharij_all : cells.all (fun c => slgeIndex c == Marakib.index .makharij c) = true := by
  decide +kernel

theorem cell_slge_eq_makharij (c : Cell) : slgeIndex c = Marakib.index .makharij c := by
  have := List.all_eq_true.mp cell_slge_eq_makharij_all c (mem_cells c)
  simpa using this

/-- فالكلمةُ عند SLGE خاناتٍ هي عددُها في مركب المخارج. -/
theorem word_slge (w : List Cell) : w.map slgeIndex = w.map (Marakib.index .makharij) :=
  List.map_congr_left fun c _ => cell_slge_eq_makharij c

/-! ## ٢. الاقتران والقوائم -/

/-- `SLGE.Core.pair` بصيغته المغلقة. -/
def slgePair (u r : Nat) : Nat := (u + r) * (u + r + 1) / 2 + r

theorem pair_slge (u r : Nat) : slgePair u r = pair u r := (pair_closed u r).symm

/-- `SLGE.Core.encS` منسوخًا. -/
def encS : List Nat → Nat
  | [] => 0
  | a :: l => 1 + pair a (encS l)

theorem encS_injective : ∀ {l l' : List Nat}, encS l = encS l' → l = l'
  | [], [], _ => rfl
  | [], _ :: _, h => by simp [encS] at h <;> omega
  | _ :: _, [], h => by simp [encS] at h <;> omega
  | a :: l, b :: l', h => by
    simp only [encS] at h
    obtain ⟨h1, h2⟩ := pair_injective (by omega : pair a (encS l) = pair b (encS l'))
    rw [h1, encS_injective h2]

/-! ## ٣. الوحدة -/

/-- الوحدةُ على أسلوب SLGE: الخاناتُ والجنسُ إحداثيّان مقترنان. -/
def nPair (u : Hudud.Wahda) : Nat := pair (atomNumber u.cells) (Hudud.jinsN u.jins)

theorem nPair_injective {u v : Hudud.Wahda} (h : nPair u = nPair v) : u = v := by
  obtain ⟨h1, h2⟩ := pair_injective h
  have hj : u.jins = v.jins := by rw [← Hudud.ofN_jinsN u.jins, h2, Hudud.ofN_jinsN]
  have hc := atomNumber_injective h1
  cases u; cases v; simp_all

/-- الترجمةُ من عدد الغانم إلى عدد SLGE. -/
def tarjama (k : Nat) : Nat := pair (k / 11) (k % 11)

theorem tarjama_n (u : Hudud.Wahda) : tarjama (Hudud.n u) = nPair u := by
  unfold tarjama nPair; rw [Hudud.n_div, Hudud.n_mod]

/-- والعكس: من الاقتران إلى ‎11F + j‎. -/
def tarjamaAks (F j : Nat) : Nat := 11 * F + j

theorem tarjama_aks (u : Hudud.Wahda) :
    tarjamaAks (atomNumber u.cells) (Hudud.jinsN u.jins) = Hudud.n u := rfl

/-- **كلتاهما تُسقط الرتبة:** الوحدةُ دالّةٌ في الخانات والجنس وحدهما، فكلمتان بخاناتٍ واحدة وجنسٍ واحد وحدةٌ واحدة في
الصيغتين. والرتبةُ في `Hudud.certHadd` وحدَه. -/
theorem wahda_tusqit_rutba (j : Hudud.Jins) (c : List Cell) (r r' : Nat) :
    Hudud.n ⟨j, c⟩ = Hudud.n ⟨j, c⟩ ∧ nPair ⟨j, c⟩ = nPair ⟨j, c⟩ ∧
    (r ≠ r' → pair (Hudud.n ⟨j, c⟩) r ≠ pair (Hudud.n ⟨j, c⟩) r') :=
  ⟨rfl, rfl, fun hr he => hr (pair_injective he).2⟩

/-! ## ٤. القسم: ج3 = SLGE -/

/-- `SLGE.Cat.roles` منسوخًا. -/
def roles (ind tim : Bool) : Bool × Bool := (ind && !tim, ind)

/-- `SLGE.Cat.kindOf` منسوخًا، إلى أقسام `Tarkib`. -/
def kindOf : Bool × Bool → Tarkib.Qism
  | (true, _) => .ism
  | (false, true) => .fil
  | (false, false) => .harf

/-- **قسمةُ ج3 هي قسمةُ SLGE بعينها.** -/
theorem j3_eq_slge (s : Mufrad.Sifat) : kindOf (roles s.istiqlal s.zamanHaya) = Mufrad.qismOf s := by
  rcases s with ⟨i, t, _, _⟩
  cases i <;> cases t <;> rfl

/-- **ولا رابعة** في الصورتين. -/
theorem la_rabia (ind tim : Bool) : roles ind tim ≠ (true, false) := by
  cases ind <;> cases tim <;> decide

def ilaKhanat : Tarkib.Qism → QismKhanat.Qism
  | .ism => .ism
  | .fil => .fil
  | .harf => .harf

/-! ## ٥. السلامة على قسمة ج3 -/

/-- إن كان مرجعُ الكلمة قسمةَ ج3 على صفاتها ولم تخطئ علامة، فمعيَّنُ القارئ قسمُ ج3. -/
theorem muayyan_j3 {α : Type} (as : List (Alama α)) (sifa : α → Mufrad.Sifat) (x : α)
    (h : ∀ a ∈ as, khata a (x, ilaKhanat (Mufrad.qismOf (sifa x))) = false) (q : QismKhanat.Qism)
    (hq : qiraa as x = .muayyan q) : q = ilaKhanat (kindOf (roles (sifa x).istiqlal (sifa x).zamanHaya)) := by
  rw [j3_eq_slge]
  exact muayyan_sahih as (x, _) h q hq

/-! ## شواهد -/

/-- «كَتَبَ» عند SLGE ‎[32, 72, 104]‎، وفي القسمة: «هو» اسم، «قام» فعل، «من» حرف. -/
theorem shawahid :
    (cell "كَتَبَ").map slgeIndex = [32, 72, 104] ∧
    kindOf (roles Mufrad.huwa.istiqlal Mufrad.huwa.zamanHaya) = .ism ∧
    kindOf (roles Mufrad.qama.istiqlal Mufrad.qama.zamanHaya) = .fil ∧
    kindOf (roles Mufrad.min.istiqlal Mufrad.min.zamanHaya) = .harf := by
  decide +kernel

end A116.WahdaMuqarana
