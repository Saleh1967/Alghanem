import Slge.Wazn

/-!
# شبكةُ الأوزان: الترخيصُ الجبريُّ التدريجيُّ من المصدر

على القالب ثلاثُ عمليّات (`Step`): إدخالُ رمز، حذفُ رمزٍ **بشرط بقاء مواضع الأصل**، وتغييرُ
حالة. المبرهَن:

* `wf_step`، `wf_run`: كلُّ عمليّةٍ وكلُّ تتابعٍ يحفظ سلامةَ القالب (الأصلُ يبقى مستردًّا).
  فالصعودُ درجةً درجةً لا يُفقد الفاءَ والعينَ واللام، والحكمُ بعد كلّ درجةٍ على القالب وحدَه
  (`Wazn.licensed_fill_indep`).
* `edges_apply`: شبكةُ البصريّين المودَعة (120 حافّة): الابنُ = الأبُ بعد عمليّاتِه، بالحساب.
* `network_rooted`: كلُّ وزنٍ يبلغ الجذرَ (المصدرُ المجرّد فَعْل، الرقم 29) في أقلّ من 121 خطوة.
* `network_wf`: ومن ذلك سلامةُ كلّ وزنٍ في الشبكة من سلامة الجذر وحدَها.

الترتيبُ نفسُه (مَن أبو مَن) **معلن** من البصريّين؛ وأنّه ليس أقلَّ الأشجار كلفةً **مقيس** في بايثون
(`slge.shabaka.agreement`)، لا مبرهَن هنا.
-/

namespace Slge.Shabaka

open Slge.Wazn

/-- عمليّةٌ على القالب. -/
inductive Step where
  | ins : Nat → Sym → Step
  | del : Nat → Step
  | set : Nat → Fin 4 → Step
  deriving DecidableEq, Repr

def withState : Sym → Fin 4 → Sym
  | .lit c, st => .lit ⟨c.carrier, st⟩
  | .slot i _, st => .slot i st

def ins : Nat → Sym → Template → Template
  | 0, s, t => s :: t
  | _ + 1, s, [] => [s]
  | n + 1, s, x :: t => x :: ins n s t

def del : Nat → Template → Template
  | _, [] => []
  | 0, _ :: t => t
  | n + 1, x :: t => x :: del n t

def setSt : Nat → Fin 4 → Template → Template
  | _, _, [] => []
  | 0, st, x :: t => withState x st :: t
  | n + 1, st, x :: t => x :: setSt n st t

/-- الحذفُ جائزٌ إن بقيت مواضعُ الأصل كلُّها. -/
def delOk (n : Nat) (t : Template) : Bool := (slots t).all fun i => (slots (del n t)).contains i

def step (t : Template) : Step → Template
  | .ins n s => ins n s t
  | .del n => if delOk n t then del n t else t
  | .set n st => setSt n st t

def run (es : List Step) (t : Template) : Template := es.foldl step t

theorem mem_slots_ins (i : Fin 3) (s : Sym) : ∀ (n : Nat) (t : Template),
    i ∈ slots t → i ∈ slots (ins n s t)
  | 0, t, h => by cases s <;> simp [ins, slots, h]
  | _ + 1, [], h => by simp [slots] at h
  | n + 1, x :: t, h => by
    cases x with
    | lit c => simp only [ins, slots] at h ⊢; exact mem_slots_ins i s n t h
    | slot j st =>
      simp only [ins, slots, List.mem_cons] at h ⊢
      rcases h with h | h
      · exact Or.inl h
      · exact Or.inr (mem_slots_ins i s n t h)

theorem slots_setSt : ∀ (n : Nat) (st : Fin 4) (t : Template), slots (setSt n st t) = slots t
  | n, _, [] => by cases n <;> rfl
  | 0, st, x :: t => by cases x <;> simp [setSt, withState, slots]
  | n + 1, st, x :: t => by cases x <;> simp [setSt, slots, slots_setSt n st t]

theorem wf_of_sub {t t' : Template} (h : ∀ i, i ∈ slots t → i ∈ slots t') (w : WF t) : WF t' :=
  ⟨h 0 w.1, h 1 w.2.1, h 2 w.2.2⟩

/-- كلُّ عمليّةٍ تحفظ السلامة. -/
theorem wf_step (t : Template) (e : Step) (w : WF t) : WF (step t e) := by
  cases e with
  | ins n s => exact wf_of_sub (fun i h => mem_slots_ins i s n t h) w
  | set n st =>
    show WF (setSt n st t)
    exact wf_of_sub (fun i h => by rw [slots_setSt]; exact h) w
  | del n =>
    show WF (if delOk n t then del n t else t)
    by_cases hok : delOk n t = true
    · rw [ite_eq_left hok]
      refine wf_of_sub (fun i hi => ?_) w
      exact List.contains_iff_mem.1 (List.all_eq_true.1 hok i hi)
    · rw [ite_eq_right hok]; exact w

/-- وكلُّ تتابعٍ. -/
theorem wf_run (es : List Step) : ∀ t, WF t → WF (run es t) := by
  induction es with
  | nil => intro t w; exact w
  | cons e es ih => intro t w; exact ih (step t e) (wf_step t e w)

/-! ## الشبكةُ المودَعة -/

/-- (الابن، الأب، عمليّاتُ الأب إلى الابن) بأرقام `awzan`. -/
def edges : List (Nat × Nat × List Step) := [
  (0, 29, [.set 2 0, .set 1 0]),  -- فَعْلٌ → فَعَلَ
  (1, 29, [.set 2 0, .set 1 1]),  -- فَعْلٌ → فَعِلَ
  (2, 29, [.set 2 0, .set 1 2]),  -- فَعْلٌ → فَعُلَ
  (30, 29, [.ins 2 (l 27 3), .set 1 2, .set 0 2]),  -- فَعْلٌ → فُعُولٌ
  (31, 29, [.ins 3 (l 3 2), .set 2 0, .ins 2 (l 1 3), .set 1 0]),  -- فَعْلٌ → فَعَالَةٌ
  (32, 29, [.ins 3 (l 3 2), .set 2 0, .ins 2 (l 27 3), .set 1 2, .set 0 2]),  -- فَعْلٌ → فُعُولَةٌ
  (33, 29, [.ins 3 (l 25 2), .ins 3 (l 1 3), .set 2 0, .set 1 0]),  -- فَعْلٌ → فَعَلَانٌ
  (34, 29, [.ins 2 (l 1 3), .set 1 0, .set 0 2]),  -- فَعْلٌ → فُعَالٌ
  (35, 29, [.ins 2 (l 1 3), .set 1 0, .set 0 1]),  -- فَعْلٌ → فِعَالٌ
  (36, 29, [.set 1 0]),  -- فَعْلٌ → فَعَلٌ
  (37, 29, [.ins 3 (l 3 2), .set 2 0, .ins 2 (l 1 3), .set 1 0, .set 0 1]),  -- فَعْلٌ → فِعَالَةٌ
  (3, 0, [.set 1 1, .set 0 2]),  -- فَعَلَ → فُعِلَ
  (4, 1, [.set 2 2, .set 1 0, .set 0 3, .ins 0 (l 28 0)]),  -- فَعِلَ → يَفْعَلُ
  (5, 0, [.set 2 2, .set 1 1, .set 0 3, .ins 0 (l 28 0)]),  -- فَعَلَ → يَفْعِلُ
  (6, 2, [.set 2 2, .set 0 3, .ins 0 (l 28 0)]),  -- فَعُلَ → يَفْعُلُ
  (7, 3, [.set 2 2, .set 1 0, .set 0 3, .ins 0 (l 28 2)]),  -- فُعِلَ → يُفْعَلُ
  (8, 4, [.set 3 3, .del 0, .ins 0 (l 0 1)]),  -- يَفْعَلُ → اِفْعَلْ
  (9, 5, [.set 3 3, .del 0, .ins 0 (l 0 1)]),  -- يَفْعِلُ → اِفْعِلْ
  (10, 6, [.set 3 3, .del 0, .ins 0 (l 0 2)]),  -- يَفْعُلُ → اُفْعُلْ
  (48, 0, [.set 2 2, .set 1 1, .ins 1 (l 1 3)]),  -- فَعَلَ → فَاعِلٌ
  (49, 0, [.set 2 2, .ins 2 (l 27 3), .set 1 2, .set 0 3, .ins 0 (l 24 0)]),  -- فَعَلَ → مَفْعُولٌ
  (50, 48, [.ins 3 (l 1 3), .ins 3 (r 1 0), .set 2 3, .del 1]),  -- فَاعِلٌ → فَعَّالٌ
  (51, 48, [.ins 3 (l 1 3), .set 2 0, .del 1, .set 0 3, .ins 0 (l 24 1)]),  -- فَاعِلٌ → مِفْعَالٌ
  (52, 48, [.ins 3 (l 27 3), .set 2 2, .del 1]),  -- فَاعِلٌ → فَعُولٌ
  (53, 2, [.set 2 2, .ins 2 (l 28 3), .set 1 1]),  -- فَعُلَ → فَعِيلٌ
  (54, 1, [.set 2 2, .set 1 0, .set 0 3, .ins 0 (l 0 0)]),  -- فَعِلَ → أَفْعَلُ
  (55, 1, [.ins 3 (l 25 2), .ins 3 (l 1 3), .set 1 3]),  -- فَعِلَ → فَعْلَانُ
  (56, 4, [.del 0, .ins 0 (l 24 0)]),  -- يَفْعَلُ → مَفْعَلٌ
  (57, 5, [.del 0, .ins 0 (l 24 0)]),  -- يَفْعِلُ → مَفْعِلٌ
  (58, 56, [.ins 4 (l 3 2), .set 3 0]),  -- مَفْعَلٌ → مَفْعَلَةٌ
  (59, 0, [.set 2 2, .set 0 3, .ins 0 (l 24 1)]),  -- فَعَلَ → مِفْعَلٌ
  (60, 59, [.ins 3 (l 1 3)]),  -- مِفْعَلٌ → مِفْعَالٌ (آلة)
  (61, 59, [.ins 4 (l 3 2), .set 3 0]),  -- مِفْعَلٌ → مِفْعَلَةٌ
  (62, 50, [.ins 5 (l 3 2), .set 4 0]),  -- فَعَّالٌ → فَعَّالَةٌ
  (63, 29, [.ins 3 (l 3 2), .set 2 0]),  -- فَعْلٌ → فَعْلَةٌ
  (64, 29, [.ins 3 (l 3 2), .set 2 0, .set 0 1]),  -- فَعْلٌ → فِعْلَةٌ
  (65, 29, [.ins 3 (l 3 2), .ins 3 (l 28 0), .ins 3 (l 28 3), .set 2 1]),  -- فَعْلٌ → فَعْلِيَّةٌ
  (11, 0, [.set 0 3, .ins 0 (l 0 0)]),  -- فَعَلَ → أَفْعَلَ
  (12, 0, [.ins 2 (r 1 0), .set 1 3]),  -- فَعَلَ → فَعَّلَ
  (13, 0, [.ins 1 (l 1 3)]),  -- فَعَلَ → فَاعَلَ
  (14, 12, [.ins 0 (l 3 0)]),  -- فَعَّلَ → تَفَعَّلَ
  (15, 13, [.ins 0 (l 3 0)]),  -- فَاعَلَ → تَفَاعَلَ
  (16, 0, [.ins 0 (l 25 3), .ins 0 (l 0 1)]),  -- فَعَلَ → اِنْفَعَلَ
  (17, 0, [.ins 1 (l 3 0), .set 0 3, .ins 0 (l 0 1)]),  -- فَعَلَ → اِفْتَعَلَ
  (18, 1, [.ins 3 (r 2 0), .set 2 3, .set 1 0, .set 0 3, .ins 0 (l 0 1)]),  -- فَعِلَ → اِفْعَلَّ
  (19, 0, [.set 0 3, .ins 0 (l 3 0), .ins 0 (l 12 3), .ins 0 (l 0 1)]),  -- فَعَلَ → اِسْتَفْعَلَ
  (20, 11, [.set 3 2, .set 2 1, .del 0, .ins 0 (l 28 2)]),  -- أَفْعَلَ → يُفْعِلُ
  (21, 12, [.set 3 2, .set 2 1, .ins 0 (l 28 2)]),  -- فَعَّلَ → يُفَعِّلُ
  (22, 13, [.set 3 2, .set 2 1, .ins 0 (l 28 2)]),  -- فَاعَلَ → يُفَاعِلُ
  (23, 14, [.set 4 2, .ins 0 (l 28 0)]),  -- تَفَعَّلَ → يَتَفَعَّلُ
  (24, 15, [.set 4 2, .ins 0 (l 28 0)]),  -- تَفَاعَلَ → يَتَفَاعَلُ
  (25, 16, [.set 4 2, .set 3 1, .del 0, .ins 0 (l 28 0)]),  -- اِنْفَعَلَ → يَنْفَعِلُ
  (26, 17, [.set 4 2, .set 3 1, .del 0, .ins 0 (l 28 0)]),  -- اِفْتَعَلَ → يَفْتَعِلُ
  (27, 18, [.set 4 2, .del 0, .ins 0 (l 28 0)]),  -- اِفْعَلَّ → يَفْعَلُّ
  (28, 19, [.set 5 2, .set 4 1, .del 0, .ins 0 (l 28 0)]),  -- اِسْتَفْعَلَ → يَسْتَفْعِلُ
  (38, 11, [.set 3 2, .ins 3 (l 1 3), .set 0 1]),  -- أَفْعَلَ → إِفْعَالٌ
  (39, 12, [.set 3 2, .del 2, .ins 2 (l 28 3), .set 1 1, .set 0 3, .ins 0 (l 3 0)]),  -- فَعَّلَ → تَفْعِيلٌ
  (40, 13, [.ins 4 (l 3 2), .ins 0 (l 24 2)]),  -- فَاعَلَ → مُفَاعَلَةٌ
  (41, 13, [.set 3 2, .ins 3 (l 1 3), .del 1, .set 0 1]),  -- فَاعَلَ → فِعَالٌ (مفاعلة)
  (42, 14, [.set 4 2, .set 3 2]),  -- تَفَعَّلَ → تَفَعُّلٌ
  (43, 15, [.set 4 2, .set 3 2]),  -- تَفَاعَلَ → تَفَاعُلٌ
  (44, 16, [.set 4 2, .ins 4 (l 1 3), .set 2 1]),  -- اِنْفَعَلَ → اِنْفِعَالٌ
  (45, 17, [.set 4 2, .ins 4 (l 1 3), .set 2 1]),  -- اِفْتَعَلَ → اِفْتِعَالٌ
  (46, 18, [.set 4 2, .ins 4 (l 1 3), .set 3 0, .set 2 1]),  -- اِفْعَلَّ → اِفْعِلَالٌ
  (47, 19, [.set 5 2, .ins 5 (l 1 3), .set 2 1]),  -- اِسْتَفْعَلَ → اِسْتِفْعَالٌ
  (66, 20, [.del 0, .ins 0 (l 24 2)]),  -- يُفْعِلُ → مُفْعِلٌ
  (67, 66, [.set 2 0]),  -- مُفْعِلٌ → مُفْعَلٌ
  (68, 21, [.del 0, .ins 0 (l 24 2)]),  -- يُفَعِّلُ → مُفَعِّلٌ
  (69, 68, [.set 3 0]),  -- مُفَعِّلٌ → مُفَعَّلٌ
  (70, 22, [.del 0, .ins 0 (l 24 2)]),  -- يُفَاعِلُ → مُفَاعِلٌ
  (71, 70, [.set 3 0]),  -- مُفَاعِلٌ → مُفَاعَلٌ
  (72, 23, [.set 4 1, .del 0, .ins 0 (l 24 2)]),  -- يَتَفَعَّلُ → مُتَفَعِّلٌ
  (73, 24, [.set 4 1, .del 0, .ins 0 (l 24 2)]),  -- يَتَفَاعَلُ → مُتَفَاعِلٌ
  (74, 25, [.del 0, .ins 0 (l 24 2)]),  -- يَنْفَعِلُ → مُنْفَعِلٌ
  (75, 26, [.del 0, .ins 0 (l 24 2)]),  -- يَفْتَعِلُ → مُفْتَعِلٌ
  (76, 75, [.set 3 0]),  -- مُفْتَعِلٌ → مُفْتَعَلٌ
  (77, 28, [.del 0, .ins 0 (l 24 2)]),  -- يَسْتَفْعِلُ → مُسْتَفْعِلٌ
  (78, 77, [.set 4 0]),  -- مُسْتَفْعِلٌ → مُسْتَفْعَلٌ
  (79, 48, [.ins 4 (l 3 2), .set 3 0]),  -- فَاعِلٌ → فَاعِلَةٌ
  (80, 54, [.ins 4 (l 0 2), .ins 4 (l 1 3), .set 3 0, .set 2 3, .set 1 0, .del 0]),  -- أَفْعَلُ → فَعْلَاءُ
  (81, 55, [.del 4]),  -- فَعْلَانُ → فَعْلَى
  (82, 54, [.ins 4 (l 1 3), .set 3 0, .set 2 3, .set 1 2, .del 0]),  -- أَفْعَلُ → فُعْلَى
  (83, 29, [.set 1 2, .set 0 3, .ins 0 (l 0 0)]),  -- فَعْلٌ → أَفْعُلٌ
  (84, 29, [.ins 2 (l 1 3), .set 1 0, .set 0 3, .ins 0 (l 0 0)]),  -- فَعْلٌ → أَفْعَالٌ
  (85, 35, [.ins 4 (l 3 2), .set 3 0, .del 2, .set 1 1, .set 0 3, .ins 0 (l 0 0)]),  -- فِعَالٌ → أَفْعِلَةٌ
  (86, 29, [.ins 3 (l 3 2), .set 2 0, .set 0 1]),  -- فَعْلٌ → فِعْلَةٌ (جمع)
  (87, 54, [.set 2 3, .set 1 2, .del 0]),  -- أَفْعَلُ → فُعْلٌ
  (88, 35, [.del 2, .set 1 2, .set 0 2]),  -- فِعَالٌ → فُعُلٌ
  (89, 29, [.set 1 0, .set 0 2]),  -- فَعْلٌ → فُعَلٌ
  (90, 64, [.del 3, .set 2 2, .set 1 0]),  -- فِعْلَةٌ → فِعَلٌ
  (91, 48, [.ins 4 (l 3 2), .set 3 0, .set 2 0, .del 1]),  -- فَاعِلٌ → فَعَلَةٌ
  (92, 48, [.ins 4 (l 3 2), .set 3 0, .set 2 0, .del 1, .set 0 2]),  -- فَاعِلٌ → فُعَلَةٌ
  (93, 29, [.ins 2 (l 1 3), .set 1 0, .set 0 1]),  -- فَعْلٌ → فِعَالٌ (جمع)
  (94, 29, [.ins 2 (l 27 3), .set 1 2, .set 0 2]),  -- فَعْلٌ → فُعُولٌ (جمع)
  (95, 48, [.ins 3 (l 1 3), .ins 3 (r 1 0), .set 2 3, .del 1, .set 0 2]),  -- فَاعِلٌ → فُعَّالٌ
  (96, 48, [.ins 3 (r 1 0), .set 2 3, .del 1, .set 0 2]),  -- فَاعِلٌ → فُعَّلٌ
  (97, 29, [.ins 3 (l 25 2), .ins 3 (l 1 3), .set 2 0, .set 0 1]),  -- فَعْلٌ → فِعْلَانٌ
  (98, 29, [.ins 3 (l 25 2), .ins 3 (l 1 3), .set 2 0, .set 0 2]),  -- فَعْلٌ → فُعْلَانٌ
  (99, 53, [.ins 4 (l 0 2), .ins 4 (l 1 3), .set 3 0, .del 2, .set 1 0, .set 0 2]),  -- فَعِيلٌ → فُعَلَاءُ
  (100, 53, [.ins 4 (l 0 2), .ins 4 (l 1 3), .set 3 0, .del 2, .set 0 3, .ins 0 (l 0 0)]),  -- فَعِيلٌ → أَفْعِلَاءُ
  (101, 56, [.set 2 1, .ins 2 (l 1 3), .set 1 0]),  -- مَفْعَلٌ → مَفَاعِلُ
  (102, 49, [.del 3, .ins 3 (l 28 3), .set 2 1, .ins 2 (l 1 3), .set 1 0]),  -- مَفْعُولٌ → مَفَاعِيلُ
  (103, 48, [.ins 1 (l 27 0)]),  -- فَاعِلٌ → فَوَاعِلُ
  (104, 53, [.del 2, .ins 2 (l 0 1), .ins 2 (l 1 3), .set 1 0]),  -- فَعِيلٌ → فَعَائِلُ
  (105, 54, [.set 2 1, .ins 2 (l 1 3), .set 1 0]),  -- أَفْعَلُ → أَفَاعِلُ
  (106, 38, [.del 3, .ins 3 (l 28 3), .set 2 1, .ins 2 (l 1 3), .set 1 0, .set 0 0]),  -- إِفْعَالٌ → أَفَاعِيلُ
  (107, 39, [.ins 2 (l 1 3), .set 1 0]),  -- تَفْعِيلٌ → تَفَاعِيلُ
  (108, 81, [.del 3, .ins 3 (l 28 3), .set 2 1, .ins 2 (l 1 3), .set 1 0]),  -- فَعْلَى → فَعَالِي
  (109, 81, [.ins 2 (l 1 3), .set 1 0]),  -- فَعْلَى → فَعَالَى
  (110, 82, [.ins 2 (l 1 3), .set 1 0]),  -- فُعْلَى → فُعَالَى
  (111, 48, [.ins 1 (l 28 0)]),  -- فَاعِلٌ → فَيَاعِلُ
  (112, 50, [.ins 4 (l 28 3), .ins 4 (r 1 1), .del 2, .set 1 0]),  -- فَعَّالٌ → فَعَاعِيلُ
  -- أمرُ المزيد من مضارعه (كأمر المجرّد)
  (113, 20, [.set 3 3, .del 0, .ins 0 (l 0 0)]),  -- يُفْعِلُ → أَفْعِلْ
  (114, 21, [.set 4 3, .del 0]),  -- يُفَعِّلُ → فَعِّلْ
  (115, 22, [.set 4 3, .del 0]),  -- يُفَاعِلُ → فَاعِلْ
  (116, 23, [.set 5 3, .del 0]),  -- يَتَفَعَّلُ → تَفَعَّلْ
  (117, 24, [.set 5 3, .del 0]),  -- يَتَفَاعَلُ → تَفَاعَلْ
  (118, 25, [.set 4 3, .del 0, .ins 0 (l 0 1)]),  -- يَنْفَعِلُ → اِنْفَعِلْ
  (119, 26, [.set 4 3, .del 0, .ins 0 (l 0 1)]),  -- يَفْتَعِلُ → اِفْتَعِلْ
  (120, 28, [.set 5 3, .del 0, .ins 0 (l 0 1)])  -- يَسْتَفْعِلُ → اِسْتَفْعِلْ
]

def root : Nat := 29

def getT (k : Nat) : Template := awzan.getD k []

/-- الابنُ هو الأبُ بعد عمليّاته، لكلّ حافّة. -/
theorem edges_apply :
    edges.all (fun e => run e.2.2 (getT e.2.1) == getT e.1) = true := by decide

/-- أبو الوزن في الشبكة. -/
def parentOf (k : Nat) : Option Nat := (edges.find? fun e => e.1 == k).map fun e => e.2.1

/-- أيبلغ الجذرَ في ‎n‎ خطوة؟ -/
def reaches : Nat → Nat → Bool
  | _, 0 => false
  | k, n + 1 => if k == root then true else match parentOf k with
    | some p => reaches p n
    | none => false

theorem edges_count : edges.length = 120 := by rfl

/-- كلُّ وزنٍ يبلغ الجذر. -/
theorem network_rooted : (List.range 121).all (fun k => reaches k 121) = true := by decide

theorem run_edge_wf (c p : Nat) (es : List Step) (h : (c, p, es) ∈ edges) (w : WF (getT p)) :
    WF (getT c) := by
  have hall := List.all_eq_true.1 edges_apply (c, p, es) h
  have : run es (getT p) = getT c := by simpa using hall
  rw [← this]; exact wf_run es (getT p) w

end Slge.Shabaka
