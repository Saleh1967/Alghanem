import Slge.Kulli

/-!
# الوضعُ والمشتركُ والترادف: الوضعُ ملءُ قالبٍ بجذر، والمشتركُ ما قرأته قالبان، والمترادفان صورتان لجذر

* **الوضع** على الخانات: `Wazn.fill t r` — القالبُ (الصورة) والجذرُ (المادّة) يُقرَنان في الكلمة. الوضعُ
  متباينٌ في الجذر: ما مُلئ به قالبٌ واحد مرّتين على صورةٍ واحدة فجذرُه واحد (`wad_injective`: لكلّ قالبٍ
  سليم). والموضوعُ يُستردّ من الموضوع له: القالبُ `k` من معاني `fill (templ k) r` (`sense_of_fill`).
* **المشتركُ اللفظيّ** على الخانات: كلمةٌ يقرؤها أكثرُ من قالب (`senses`). له مرتبتان: **اشتراكُ الوضع** —
  القالبُ الواحد مودَعٌ لأكثر من بابٍ (فُعُولٌ مصدرًا وجمعًا، فِعَالٌ، مِفْعَالٌ، فِعْلَةٌ: ستّةُ أزواجٍ متطابقة
  `duplicate_templates`)؛ و**اشتراكُ الصورة** — قالبان مختلفان يلتقيان في كلمة (اِنْتِشَارٌ: اِنْفِعَالٌ من
  ت‑ش‑ر وافْتِعَالٌ من ن‑ش‑ر؛ مَنْحَةٌ: مَفْعَلٌ من ن‑ح‑ت وفَعْلَةٌ من م‑ن‑ح). الالتقاءُ محصور: لا يلتقي قالبان
  على كلمةٍ لجذرين لا ألفَ فيهما إلّا إذا تساوى طولُهما وحالاتُهما وزوائدُهما المتقابلة ولم يقابل ألفًا زائدةً
  موضعُ أصل (`mayCollide_sound`: لكلّ قالبين ولكلّ جذرين)، وأزواجُ الـ121 التي تستوفي ذلك 42 بعينها
  (`collision_pairs_eq`) — فكلُّ اشتراكِ صورةٍ في المعجم المودَع مجدوَلٌ (`homonymy_is_tabled`).
* **الفهمُ بلا قرينة**: ما قرأه قالبٌ واحد (`unaided`). والميزانُ (ف‑ع‑ل) لا يُشترَك: كلُّ ميزانٍ يُقرأ على صورته
  وحدَها ومعانيه بابُها بعينه (`mizan_unaided`، `mizan_senses`).
* **الترادف** على الخانات: صورتان مختلفتان لجذرٍ واحد في بابٍ واحد (مصادرُ الجذر: ضَرْبٌ/ضِرَابٌ) —
  المترادفان يشتركان في الجذر (`taraduf_same_root`: لكلّ قالبين سليمين ولكلّ جذر) ويختلفان في الصورة إلّا
  ما تطابق قالبُه (`masdar_forms_distinct`).
* القارئُ `wad`: مجدوَلٌ (الجزئيُّ من جدول)، مفردُ الوضع، مشتركُ الوضع (صورةٌ واحدةٌ لأكثر من باب)، مشتركُ
  الصورة (قالبان مختلفان)، أو لا يُقرأ.
ما ليس في الخانة — باسمه: المعنى اللغويّ (عَيْنٌ: ماءٌ أو بصر) ومترادفا الجذرين (قَمَرٌ/هِلَالٌ) والوضعُ
الخاصّ (العلَم) — معلَن؛ و«الوضعُ موضوعُه الذهن» رأيٌ لا خانةَ له. القياسُ على MASAQ في بايثون: توزيعُ عدد
القوالب القارئة على كلمات المرجع المحجوب، ووسمُ المرجع قرينةً تفصل المشترك. الحصرُ المُرسَل: أنواعُه ثلاثُ
كلماتٍ مكتوبةٍ باليد وبرهاناه `rfl` و`cases h` على محمولٍ لا بانيَ له إلّا الذهن، وفحصُه عدٌّ عشوائيّ —
لم يُدخَل منه شيء؛ ودخل معناه على الخانات.
-/

namespace Slge.Wad

open Slge.Categories (c)

/-! ## الوضعُ متباينٌ في الجذر -/

/-- صورةٌ واحدة على قالبٍ سليم لا تُملأ بجذرين: الوضعُ متباينٌ في الجذر. -/
theorem wad_injective (t : Wazn.Template) (ht : Wazn.WF t) (r r' : Wazn.Root)
    (h : Wazn.fill t r = Wazn.fill t r') : r = r' := by
  funext i
  have h1 := Wazn.rootOf_fill t ht r i
  have h2 := Wazn.rootOf_fill t ht r' i
  rw [h] at h1
  rw [h1] at h2
  exact Option.some.inj h2

/-- معاني الكلمة: القوالبُ التي تقرؤها بجذرٍ لا ألفَ فيه (أرقامُها في `Wazn.awzan`). -/
def senses (w : List SCell) : List Nat :=
  (List.range 121).filter fun k => Maqam.onTemplateRoot k w

/-- صورُ الكلمة: معانيها بعد طيّ القوالب المتطابقة إلى أوّلها. -/
def classes (w : List SCell) : List Nat :=
  (senses w).filter fun k => (List.range k).all fun q => Sarf.templ q != Sarf.templ k

/-- الفهمُ بلا قرينة: قالبٌ واحد يقرؤها. -/
def unaided (w : List SCell) : Bool := (senses w).length == 1

/-- الموضوعُ يُستردّ من الموضوع له: القالبُ من معاني ملئه، لكلّ قالبٍ سليم ولكلّ جذرٍ لا ألفَ فيه. -/
theorem sense_of_fill (k : Nat) (hk : k < 121) (hw : Wazn.WF (Sarf.templ k)) (r : Wazn.Root)
    (hr : ∀ i, (r i).val ≠ 1) : k ∈ senses (Wazn.fill (Sarf.templ k) r) := by
  unfold senses
  rw [List.mem_filter]
  refine ⟨List.mem_range.2 hk, ?_⟩
  unfold Maqam.onTemplateRoot
  rw [Sarf.onTemplate_fill _ hw r]
  simp only [Bool.true_and, List.all_cons, List.all_nil, Wazn.rootOf_fill _ hw r, Option.map_some,
    bne_iff_ne, ne_eq, Option.some.injEq, Bool.and_true, Bool.and_eq_true]
  exact ⟨hr 0, hr 1, hr 2⟩

/-! ## اشتراكُ الوضع: القالبُ الواحد لأكثر من باب -/

/-- أزواجُ القوالب المتطابقة في المعجم المودَع (`k < q`). -/
def duplicates : List (Nat × Nat) :=
  (List.range 121).flatMap fun k =>
    ((List.range 121).filter fun q => k < q && Sarf.templ k == Sarf.templ q).map fun q => (k, q)

/-- ستّةُ أزواج: فُعُولٌ (30، 94)، فِعَالٌ (35، 41، 93)، مِفْعَالٌ (51، 60)، فِعْلَةٌ (64، 86) — صورةٌ واحدة
مودَعةٌ لأكثر من باب (مصدرٌ وجمع، مبالغةٌ وآلة). -/
theorem duplicate_templates :
    duplicates = [(30, 94), (35, 41), (35, 93), (41, 93), (51, 60), (64, 86)] := by decide

/-! ## اشتراكُ الصورة: قالبان مختلفان يلتقيان في كلمة -/

/-- رمزان يقبلان خانةً واحدة: زائدان متساويان، أو زائدٌ غيرُ ألفٍ بحالة الموضع، أو موضعان بحالةٍ واحدة. -/
def symCompat : Wazn.Sym → Wazn.Sym → Bool
  | .lit a, .lit b => a == b
  | .lit a, .slot _ s => a.carrier.val != 1 && a.state == s
  | .slot _ s, .lit b => b.carrier.val != 1 && b.state == s
  | .slot _ s, .slot _ s' => s == s'

/-- قالبان قد يلتقيان في كلمة: تساوي الطول، ورمزٌ برمز. -/
def mayCollide : Wazn.Template → Wazn.Template → Bool
  | [], [] => true
  | a :: t, b :: u => symCompat a b && mayCollide t u
  | _, _ => false

/-- لا يلتقي قالبان على كلمةٍ واحدة لجذرين لا ألفَ فيهما إلّا إذا جاز التقاؤهما: لكلّ قالبين ولكلّ جذرين. -/
theorem mayCollide_sound : ∀ (t u : Wazn.Template) (r r' : Wazn.Root),
    (∀ i, (r i).val ≠ 1) → (∀ i, (r' i).val ≠ 1) → Wazn.fill t r = Wazn.fill u r' →
    mayCollide t u = true
  | [], [], _, _, _, _, _ => rfl
  | [], _ :: _, _, _, _, _, h => by simp [Wazn.fill] at h
  | _ :: _, [], _, _, _, _, h => by simp [Wazn.fill] at h
  | a :: t, b :: u, r, r', hr, hr', h => by
    simp only [Wazn.fill, List.map, List.cons.injEq] at h
    obtain ⟨hab, htu⟩ := h
    have ih := mayCollide_sound t u r r' hr hr' htu
    simp only [mayCollide, Bool.and_eq_true]
    refine ⟨?_, ih⟩
    cases a with
    | lit x =>
      cases b with
      | lit y => simp only [Wazn.fillSym] at hab; simp [symCompat, hab]
      | slot j s =>
        simp only [Wazn.fillSym] at hab
        subst hab
        simp only [symCompat, Bool.and_eq_true, bne_iff_ne, ne_eq, beq_iff_eq]
        exact ⟨hr' j, trivial⟩
    | slot i s =>
      cases b with
      | lit y =>
        simp only [Wazn.fillSym] at hab
        subst hab
        simp only [symCompat, Bool.and_eq_true, bne_iff_ne, ne_eq, beq_iff_eq]
        exact ⟨hr i, trivial⟩
      | slot j s' =>
        simp only [Wazn.fillSym, SCell.mk.injEq] at hab
        simp [symCompat, hab.2]

/-- أزواجُ القوالب التي قد تلتقي (`k < q`). -/
def collisionPairs : List (Nat × Nat) :=
  (List.range 121).flatMap fun k =>
    ((List.range 121).filter fun q => k < q && mayCollide (Sarf.templ k) (Sarf.templ q)).map fun q => (k, q)

theorem mem_collisionPairs (k q : Nat) (hk : k < q) (hq : q < 121)
    (h : mayCollide (Sarf.templ k) (Sarf.templ q) = true) : (k, q) ∈ collisionPairs := by
  unfold collisionPairs
  rw [List.mem_flatMap]
  refine ⟨k, List.mem_range.2 (Nat.lt_trans hk hq), ?_⟩
  rw [List.mem_map]
  refine ⟨q, ?_, rfl⟩
  rw [List.mem_filter]
  exact ⟨List.mem_range.2 hq, by simp [hk, h]⟩

/-- كلُّ اشتراكِ صورةٍ في المعجم المودَع مجدوَل: إن التقى قالبان على كلمةٍ لجذرين لا ألفَ فيهما فزوجُهما
في `collisionPairs`. -/
theorem homonymy_is_tabled (k q : Nat) (hk : k < q) (hq : q < 121) (r r' : Wazn.Root)
    (hr : ∀ i, (r i).val ≠ 1) (hr' : ∀ i, (r' i).val ≠ 1)
    (h : Wazn.fill (Sarf.templ k) r = Wazn.fill (Sarf.templ q) r') : (k, q) ∈ collisionPairs :=
  mem_collisionPairs k q hk hq (mayCollide_sound _ _ r r' hr hr' h)

set_option maxRecDepth 100000 in
/-- 42 زوجًا بعينها: ستّةٌ متطابقة (اشتراكُ وضع) و36 مختلفة (اشتراكُ صورة): يَفْعَلُ/فَعْلَةٌ، أَفْعَلَ/فَعَّلَ،
اِنْفَعَلَ/اِفْتَعَلَ، اِنْفِعَالٌ/اِفْتِعَالٌ/اِفْعِلَالٌ، مَفْعَلٌ/فَعْلَةٌ، مِفْعَلٌ/فِعْلَةٌ، مُنْفَعِلٌ/مُفْتَعِلٌ، صيغُ
منتهى الجموع، أَفْعِلْ/فَعِّلْ، اِنْفَعِلْ/اِفْتَعِلْ… -/
theorem collision_pairs_eq : collisionPairs =
    [(4, 63), (7, 96), (11, 12), (16, 17), (25, 26), (30, 94), (35, 41), (35, 93), (38, 97), (41, 93),
     (44, 45), (44, 46), (45, 46), (50, 55), (50, 80), (50, 84), (51, 60), (51, 97), (54, 63), (55, 84),
     (56, 63), (59, 64), (59, 86), (60, 97), (64, 86), (67, 96), (74, 75), (80, 84), (95, 98), (101, 103),
     (101, 104), (101, 111), (102, 112), (103, 104), (103, 105), (104, 105), (104, 111), (105, 111),
     (106, 112), (107, 112), (113, 114), (118, 119)] := by decide

/-- أزواجُ الصورة وحدَها (القالبان مختلفان) 36، وأزواجُ الوضع (المتطابقة) هي `duplicates`. -/
theorem collision_pairs_split :
    (collisionPairs.filter fun p => Sarf.templ p.1 != Sarf.templ p.2).length = 36 ∧
    collisionPairs.filter (fun p => Sarf.templ p.1 == Sarf.templ p.2) = duplicates := by
  rw [collision_pairs_eq, duplicate_templates]; exact ⟨by decide, by decide⟩

/-! ## الميزانُ لا يُشترَك -/

set_option maxRecDepth 100000 in
/-- كلُّ ميزانٍ من الـ121 يُقرأ على صورةٍ واحدة. -/
theorem mizan_unaided :
    ((List.range 121).all fun k => (classes (Wazn.mizan (Sarf.templ k))).length == 1) = true := by decide

set_option maxRecDepth 100000 in
/-- معاني الميزان بابُ قالبه بعينه: القوالبُ المطابقةُ له لا غير. -/
theorem mizan_senses :
    ((List.range 121).all fun k =>
      senses (Wazn.mizan (Sarf.templ k)) == (List.range 121).filter fun q => Sarf.templ q == Sarf.templ k)
      = true := by decide

/-! ## الترادف: صورتان لجذرٍ واحد -/

/-- المترادفان الصرفيّان يشتركان في الجذر: لكلّ قالبين سليمين ولكلّ جذرٍ يُستردّ الجذرُ نفسُه من الصورتين. -/
theorem taraduf_same_root (t u : Wazn.Template) (ht : Wazn.WF t) (hu : Wazn.WF u) (r : Wazn.Root) :
    ∀ i, Wazn.rootOf t (Wazn.fill t r) i = Wazn.rootOf u (Wazn.fill u r) i := by
  intro i
  rw [Wazn.rootOf_fill t ht r i, Wazn.rootOf_fill u hu r i]

/-- مصادرُ الجذر الواحد صورٌ متباينة إلّا ما تطابق قالبُه: على الميزان، لكلّ قالبي مصدر. -/
theorem masdar_forms_distinct :
    (Kulli.masdarTemplates.all fun k => Kulli.masdarTemplates.all fun q =>
      (Wazn.mizan (Sarf.templ k) == Wazn.mizan (Sarf.templ q)) == (Sarf.templ k == Sarf.templ q)) = true := by
  decide

/-! ## القارئ -/

inductive Kind where
  | majdul | mufrad | wadMushtarak | suraMushtarak | unread
  deriving DecidableEq, Repr

/-- الوضعُ من الخانة: مجدوَلٌ (جزئيٌّ من جدول)، أو مفردُ الوضع (قالبٌ واحد)، أو مشتركُ الوضع (صورةٌ واحدةٌ
لأكثر من باب)، أو مشتركُ الصورة (قالبان مختلفان)، أو لا يُقرأ — بعد ردّ التنوين. -/
def wad (w : List SCell) : Kind :=
  if Categories.pronouns.contains w || Jumla.mabniIsm w then .majdul
  else
    let v := Marifa.dropTanwin w
    match (senses v).length, (classes v).length with
    | 0, _ => .unread
    | 1, _ => .mufrad
    | _, 1 => .wadMushtarak
    | _, _ => .suraMushtarak

def intishar : List SCell := [c 0 1, c 25 3, c 3 1, c 13 0, c 1 3, c 10 2, c 25 3]  -- اِنْتِشَارٌ
def manha : List SCell := [c 24 0, c 25 3, c 6 0, c 3 2, c 25 3]                 -- مَنْحَةٌ
def kitab : List SCell := [c 22 1, c 3 0, c 1 3, c 2 2, c 25 3]                  -- كِتَابٌ
def ayn : List SCell := [c 18 0, c 28 3, c 25 2, c 25 3]                         -- عَيْنٌ
def qamar : List SCell := [c 21 0, c 24 0, c 10 2, c 25 3]                       -- قَمَرٌ
def hilal : List SCell := [c 26 1, c 23 0, c 1 3, c 23 2, c 25 3]                -- هِلَالٌ
def amana : List SCell := [c 0 0, c 1 3, c 24 0, c 25 0]                         -- آمَنَ

/-- اِنْتِشَارٌ مشتركُ الصورة (اِنْفِعَالٌ من ت‑ش‑ر وافْتِعَالٌ من ن‑ش‑ر)، ومَنْحَةٌ (مَفْعَلٌ من ن‑ح‑ت وفَعْلَةٌ
من م‑ن‑ح)؛ كِتَابٌ وهِلَالٌ مشتركا الوضع (فِعَالٌ مصدرًا وجمعًا)؛ عَيْنٌ وقَمَرٌ وكَاتِبٌ ويَكْتُبُ مفردةُ الوضع
بالخانة — واشتراكُ عَيْنٍ معنًى لا صورة؛ وآمَنَ مفردُ الوضع بالخانة (فَاعَلَ من ء‑م‑ن؛ وأَفْعَلَ تقتضي ألفًا في
الجذر فتُردّ — وأصلُها أَأْمَنَ بالإبدال: معلَن)؛ هُوَ وهَذَا مجدوَلان؛ ولَا لا تُقرأ. -/
theorem wad_witnesses :
    wad intishar = .suraMushtarak ∧ wad manha = .suraMushtarak ∧ wad kitab = .wadMushtarak ∧
    wad hilal = .wadMushtarak ∧ wad ayn = .mufrad ∧ wad qamar = .mufrad ∧ wad Kulli.katib = .mufrad ∧
    wad Jiha.yaktubu = .mufrad ∧ wad amana = .mufrad ∧ wad Maqam.huwa = .majdul ∧ wad Kulli.hadha = .majdul ∧
    wad Uslub.la = .unread := by decide

/-- اِنْتِشَارٌ بعينها: ملءُ اِنْفِعَالٍ بـ(ت، ش، ر) وملءُ افْتِعَالٍ بـ(ن، ش، ر) صورةٌ واحدة، وزوجُهما مجدوَل. -/
theorem intishar_two_roots :
    Wazn.fill (Sarf.templ 44) (fun i => if i = 0 then ⟨3, by decide⟩ else if i = 1 then ⟨13, by decide⟩
      else ⟨10, by decide⟩) = Marifa.dropTanwin intishar ∧
    Wazn.fill (Sarf.templ 45) (fun i => if i = 0 then ⟨25, by decide⟩ else if i = 1 then ⟨13, by decide⟩
      else ⟨10, by decide⟩) = Marifa.dropTanwin intishar ∧ (44, 45) ∈ collisionPairs := by
  exact ⟨by decide, by decide, mem_collisionPairs 44 45 (by decide) (by decide) (by decide)⟩

end Slge.Wad
