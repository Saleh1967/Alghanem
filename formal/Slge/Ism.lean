import Slge.Wasl

/-!
# الاسم: بنيتُه حالاتٌ على خاناتٍ، وتحويلاتُه عمليّات، وبناؤه العارضُ حالةٌ ثابتةٌ في الآخر

الماهيةُ (الجوهرُ الثابت) معلَنة؛ وعلى الخانات:
* **المجرّدُ الثلاثيّ عشرةٌ = 3 × 4 − 2**: حركةُ الفاء (فتح/ضم/كسر) في حالة العين (فتح/ضم/كسر/سكون)
  اثنا عشرَ قالبًا، يسقط منها فُعُل وفِعُل (الحصرُ يسمّي «فُعِل» ساقطةً ثمّ يعدّها في العشرة بدُئِل؛ والجدولُ
  يفصل: الساقطان فُعُل وفِعُل). العشرةُ كلُّها مرخَّصةٌ لكلّ جذر (`thulathi_licensed`)، وتُقرأ من الخانتين
  الأُوليين (`thulathi_read`)، وعددُها عشرة (`thulathi_ten`).
* **الرباعيُّ والخماسيّ**: قوالبُ `Wazn` ثلاثيّةُ الجذر؛ فالرباعيُّ والخماسيُّ **أشكالُ حالات** على أربعِ
  خاناتٍ وخمس (`shape`). الحصرُ يعدّ الرباعيَّ ستّةً ويسمّي فَعْلَل مرّتين (جَعْفَر، طَحْلَب): الأشكالُ
  خمسة (`rubai_shapes`)؛ والخماسيُّ أربعة (`khumasi_shapes`). كلُّها مرخَّصة.
* **التصغير** ثلاثُ عمليّات: فُعَيْل، فُعَيْعِل، فُعَيْعِيل — تحفظ الترخيص لكلّ جذر (`tasghir_licensed`)،
  ويقرؤها القارئُ من ضمٍّ ففتحٍ فياءٍ ساكنة (`tasghir_read`)؛ بُنَيَّ شاهدُ بوّابة.
* **النسب** عمليّةٌ واحدة (كسرٌ فياءٌ مشدّدة) بعد تهيئةٍ مسمّاة: حذفُ التاء، قلبُ الألف الثالثة واوًا، حذفُ
  الرابعة، وقلبُ ياء المنقوص الثالثة واوًا وفتحُ ما قبلها، وحذفُ الرابعة — كلُّها تحفظ الترخيص
  (`nisba_licensed`) وتُقرأ (`nisba_read`)؛ عَرَبِيٌّ شاهدُ بوّابة.
* **البناءُ العارض** حالةٌ ثابتةٌ في الآخر بعمليّةٍ مودَعةٍ في بابها: المنادى (`Nida.damm_is_bina`)، اسمُ لا
  (`Nawasikh.laJins`)، الظرفُ المقطوع (`Zuruf.hukm_qat`)، والعددُ المركّب (`Adad.compound_both_fatha`) —
  `arid_bina` يجمعها؛ واللازمُ جداولُ صورٍ مودَعة (`lazim_deposited`).
مسألةُ الكحل وعملُ اسم الفاعل: تيار. القياسُ على MASAQ (أسماءُ المصحف بشهادات البوّابة) في بايثون.
-/

namespace Slge.Ism

open Slge.Categories (c)
open Slge.Zuruf (setLast)

/-! ## المجرّدُ الثلاثيّ -/

/-- القالبُ بحركة الفاء وحالة العين (واللامُ بحالة الإعراب). -/
def thulathi (f ayn : Fin 4) : Wazn.Template := [.slot 0 f, .slot 1 ayn, .slot 2 2]

/-- الاثنا عشر: الفاءُ متحرّكةٌ ثلاثًا والعينُ أربعًا. -/
def twelve : List (Fin 4 × Fin 4) :=
  ([0, 2, 1] : List (Fin 4)).flatMap (fun f => ([0, 2, 1, 3] : List (Fin 4)).map (fun a => (f, a)))

/-- الساقطان لثقلهما: فُعُل وفِعُل. -/
def dropped : List (Fin 4 × Fin 4) := [(2, 2), (1, 2)]

def ten : List (Fin 4 × Fin 4) := twelve.filter (· ∉ dropped)

theorem thulathi_ten : twelve.length = 12 ∧ ten.length = 10 ∧ ten.Nodup := by decide

theorem thulathi_wf : ten.all (fun p => decide (Wazn.WF (thulathi p.1 p.2))) = true := by decide

/-- العشرةُ مرخَّصةٌ لكلّ جذر: الحالاتُ ثابتةٌ لا ساكنَ في الأوّل ولا ساكنان. -/
theorem thulathi_licensed (r : Wazn.Root) (f ayn : Fin 4) (hf : f.val ≠ 3) :
    licensed (Wazn.fill (thulathi f ayn) r) = true := by
  simp [Wazn.fill, thulathi, Wazn.fillSym, licensed, noAdj, SCell.isSukun, hf]

/-- القراءة: (حركةُ الفاء، حالةُ العين) من الخانتين الأُوليين. -/
def readThulathi (w : List SCell) : Option (Fin 4 × Fin 4) :=
  match w with
  | [a, b, _] => some (a.state, b.state)
  | _ => none

theorem thulathi_read (r : Wazn.Root) (f ayn : Fin 4) :
    readThulathi (Wazn.fill (thulathi f ayn) r) = some (f, ayn) := by
  simp [Wazn.fill, thulathi, Wazn.fillSym, readThulathi]

/-- شواهدُ الحصر العشرة (رَجُل بشهادة البوّابة: فَعُل). -/
def witnesses : List (String × List SCell × (Fin 4 × Fin 4)) := [
  ("شَمْس", [c 13 0, c 24 3, c 12 2], (0, 3)), ("قَمَر", [c 21 0, c 24 0, c 10 2], (0, 0)),
  ("كَتِف", [c 22 0, c 3 1, c 20 2], (0, 1)), ("عَضُد", [c 18 0, c 15 2, c 8 2], (0, 2)),
  ("قُفْل", [c 21 2, c 20 3, c 23 2], (2, 3)), ("صُرَد", [c 14 2, c 10 0, c 8 2], (2, 0)),
  ("دُئِل", [c 8 2, c 0 1, c 23 2], (2, 1)), ("حِمْل", [c 6 1, c 24 3, c 23 2], (1, 3)),
  ("عِنَب", [c 18 1, c 25 0, c 2 2], (1, 0)), ("إِبِل", [c 0 1, c 2 1, c 23 2], (1, 1)),
  ("رَجُل", [c 10 0, c 5 2, c 23 2], (0, 2))
]

theorem witnesses_read :
    witnesses.all (fun w => readThulathi w.2.1 == some w.2.2 && licensed w.2.1 &&
      decide (w.2.2 ∈ ten)) = true := by decide

/-! ## الرباعيُّ والخماسيّ: أشكالُ حالات -/

/-- شكلُ الكلمة: حالاتُ خاناتها قبل الأخيرة. -/
def shape (w : List SCell) : List (Fin 4) := (Afal.initOf w).map SCell.state

def rubai : List (String × List SCell) := [
  ("جَعْفَر", [c 5 0, c 18 3, c 20 0, c 10 2]), ("زِبْرِج", [c 11 1, c 2 3, c 10 1, c 5 2]),
  ("بُرْقُع", [c 2 2, c 10 3, c 21 2, c 18 2]), ("دِرْهَم", [c 8 1, c 10 3, c 26 0, c 24 2]),
  ("قِمَطْر", [c 21 1, c 24 0, c 16 3, c 10 2]), ("طَحْلَب", [c 16 0, c 6 3, c 23 0, c 2 2])
]

def khumasi : List (String × List SCell) := [
  ("سَفَرْجَل", [c 12 0, c 20 0, c 10 3, c 5 0, c 23 2]),
  ("جَحْمَرِش", [c 5 0, c 6 3, c 24 0, c 10 1, c 13 2]),
  ("قِرْطَعْب", [c 21 1, c 10 3, c 16 0, c 18 3, c 2 2]),
  ("خُذَاعِر", [c 7 2, c 9 0, c 1 3, c 18 1, c 10 2])
]

/-- الحصرُ يعدّ ستّةً ويسمّي فَعْلَل مرّتين: الأشكالُ خمسة. -/
theorem rubai_shapes :
    rubai.all (fun p => licensed p.2 && p.2.length == 4) = true ∧
    (rubai.map (fun p => shape p.2)).eraseDups.length = 5 ∧
    shape (rubai.getD 0 ("", [])).2 = shape (rubai.getD 5 ("", [])).2 := by decide

theorem khumasi_shapes :
    khumasi.all (fun p => licensed p.2 && p.2.length == 5) = true ∧
    (khumasi.map (fun p => shape p.2)).Nodup := by decide

/-! ## التصغير: ثلاثُ عمليّات -/

def ya : SCell := c 28 3

/-- فُعَيْل. -/
def saghir3 (a b d : Fin 29) (st : Fin 4) : List SCell := [⟨a, 2⟩, ⟨b, 0⟩, ya, ⟨d, st⟩]
/-- فُعَيْعِل. -/
def saghir4 (a b d e : Fin 29) (st : Fin 4) : List SCell :=
  [⟨a, 2⟩, ⟨b, 0⟩, ya, ⟨d, 1⟩, ⟨e, st⟩]
/-- فُعَيْعِيل (الخماسيُّ الذي قبل آخره مدّ). -/
def saghir5 (a b d e : Fin 29) (st : Fin 4) : List SCell :=
  [⟨a, 2⟩, ⟨b, 0⟩, ya, ⟨d, 1⟩, c 28 3, ⟨e, st⟩]

theorem tasghir_licensed (a b d e : Fin 29) (st : Fin 4) (hst : st.val ≠ 3) :
    licensed (saghir3 a b d st) = true ∧ licensed (saghir4 a b d e st) = true ∧
    licensed (saghir5 a b d e st) = true := by
  refine ⟨?_, ?_, ?_⟩ <;> simp [saghir3, saghir4, saghir5, ya, licensed, noAdj, SCell.isSukun, c, hst]

/-- القارئ: ضمٌّ ففتحٌ فياءٌ ساكنة. -/
def isTasghir (w : List SCell) : Bool :=
  match w with
  | a :: b :: y :: _ => a.state.val == 2 && b.state.val == 0 && y.carrier.val == 28 && y.state.val == 3
  | _ => false

theorem tasghir_read (a b d e : Fin 29) (st : Fin 4) :
    isTasghir (saghir3 a b d st) = true ∧ isTasghir (saghir4 a b d e st) = true ∧
    isTasghir (saghir5 a b d e st) = true := by
  refine ⟨?_, ?_, ?_⟩ <;> rfl

/-- رُجَيْل من رَجُل، دُرَيْهِم من دِرْهَم، عُصَيْفِير من عُصْفُور؛ وبُنَيَّ (بوّابة) بياءٍ مشدّدة: ياءُ التصغير
فياءُ المتكلّم مدغمةً. -/
theorem tasghir_witnesses :
    saghir3 10 5 23 2 = [c 10 2, c 5 0, c 28 3, c 23 2] ∧
    saghir4 8 10 26 24 2 = [c 8 2, c 10 0, c 28 3, c 26 1, c 24 2] ∧
    saghir5 18 14 20 10 2 = [c 18 2, c 14 0, c 28 3, c 20 1, c 28 3, c 10 2] ∧
    isTasghir [c 2 2, c 25 0, c 28 3, c 28 0] = true := by decide

/-! ## النسب: عمليّةٌ واحدةٌ بعد تهيئة -/

/-- ياءٌ مشدّدةٌ مكسورٌ ما قبلها. -/
def nisba (w : List SCell) (st : Fin 4) : List SCell := setLast w 1 ++ [c 28 3, ⟨⟨28, by decide⟩, st⟩]

/-- التهيئة: حذفُ تاء التأنيث؛ المقصورُ الثالثُ يُقلب واوًا والرابعُ يُحذف؛ المنقوصُ الثالثُ يُقلب واوًا
ويُفتح ما قبله والرابعُ يُحذف. -/
inductive Prep where
  | none | dropTa | maqsur3 | maqsur4 | manqus3 | manqus4
  deriving DecidableEq, Repr

def prepare : Prep → List SCell → List SCell
  | .none, w => w
  | .dropTa, w => Afal.initOf w
  | .maqsur3, w => Afal.initOf w ++ [c 27 0]
  | .maqsur4, w => Afal.initOf w
  | .manqus3, w => setLast (Afal.initOf w) 0 ++ [c 27 0]
  | .manqus4, w => Afal.initOf w

/-- النسبُ بعد التهيئة يحفظ الترخيص إذا كان المهيَّأُ مرخَّصًا وآخرُه متحرّكًا. -/
theorem nisba_licensed (w : List SCell) (st : Fin 4) (hst : st.val ≠ 3) (hw : licensed w = true)
    (hne : w ≠ []) (hlast : ∀ x, Afal.lastOf w = some x → x.state.val ≠ 3) :
    licensed (nisba w st) = true := by
  obtain ⟨i, k, hi⟩ := Nawasikh.setLast_eq_append w 1 hne
  have h1 : licensed (setLast w 1) = true := by
    rw [Zuruf.setLast_licensed w 1 (by decide) hlast]; exact hw
  unfold nisba; rw [hi] at h1 ⊢
  exact Damair.attach_licensed _ [c 28 3, ⟨⟨28, by decide⟩, st⟩] h1
    (by simp [noAdj, SCell.isSukun, c, hst]) (by simp)
    (fun x y hx hy => by
      simp at hx; subst hx
      simp only [List.head?_cons, Option.some.injEq] at hy; subst hy; rfl)

/-- القراءة: كسرٌ فياءٌ ساكنةٌ فياء. -/
def isNisba (w : List SCell) : Bool :=
  match w.reverse with
  | y2 :: y1 :: k :: _ => y2.carrier.val == 28 && y1.carrier.val == 28 && y1.state.val == 3 &&
      k.state.val == 1
  | _ => false

theorem nisba_read (w : List SCell) (st : Fin 4) (hne : w ≠ []) : isNisba (nisba w st) = true := by
  obtain ⟨i, k, hi⟩ := Nawasikh.setLast_eq_append w 1 hne
  unfold nisba; rw [hi]; unfold isNisba
  simp only [List.append_assoc, List.reverse_append, List.reverse_cons, List.reverse_nil,
    List.nil_append, List.cons_append]
  simp [c, Ishara.v28, Ishara.s3]

/-- شواهد: مِصْرِيّ (مِصْرَ بوّابة)، مَكِّيّ، عَصَوِيّ، مُصْطَفِيّ، عَمَوِيّ، قَاضِيّ؛ وعَرَبِيٌّ بشهادة البوّابة. -/
theorem nisba_witnesses :
    nisba [c 24 1, c 14 3, c 10 0] 2 = [c 24 1, c 14 3, c 10 1, c 28 3, c 28 2] ∧
    nisba (prepare .dropTa [c 24 0, c 22 3, c 22 0, c 3 2]) 2 =
      [c 24 0, c 22 3, c 22 1, c 28 3, c 28 2] ∧
    nisba (prepare .maqsur3 [c 18 0, c 14 0, c 1 3]) 2 = [c 18 0, c 14 0, c 27 1, c 28 3, c 28 2] ∧
    nisba (prepare .maqsur4 [c 24 2, c 14 3, c 16 0, c 20 0, c 1 3]) 2 =
      [c 24 2, c 14 3, c 16 0, c 20 1, c 28 3, c 28 2] ∧
    nisba (prepare .manqus3 [c 18 0, c 24 1, c 28 3]) 2 = [c 18 0, c 24 0, c 27 1, c 28 3, c 28 2] ∧
    nisba (prepare .manqus4 [c 21 0, c 1 3, c 15 1, c 28 3]) 2 = [c 21 0, c 1 3, c 15 1, c 28 3, c 28 2] ∧
    isNisba [c 18 0, c 10 0, c 2 1, c 28 3, c 28 2] = true ∧
    nisba [c 18 0, c 10 0, c 2 0] 2 ++ [c 25 3] = [c 18 0, c 10 0, c 2 1, c 28 3, c 28 2, c 25 3] := by
  decide

/-! ## البناءُ العارض: حالةٌ ثابتةٌ في الآخر -/

/-- الأربعةُ عمليّاتٌ على الآخر بحالةٍ ثابتة: ضمُّ المنادى، فتحُ اسم لا، ضمُّ المقطوع، فتحُ المركّب. -/
theorem arid_bina (w : List SCell) (hne : w ≠ []) (k : Fin 29) (hk : k.val ≠ 25) (m : Bool) :
    Nida.IsBina (Nida.hukm (Afal.initOf w ++ [⟨k, 2⟩])) = true ∧
    (∃ k', Afal.lastOf (Nawasikh.laJins.1 w) = some ⟨k', 0⟩) ∧
    Zuruf.hukm (Zuruf.qat w) = .maqtu ∧
    (Afal.lastOf (Adad.compound w m)).map SCell.state = some 0 := by
  refine ⟨?_, Zuruf.lastOf_setLast w 0 hne, Zuruf.hukm_qat w hne, (Adad.compound_both_fatha w m hne).2⟩
  have := Nida.damm_is_bina (Afal.initOf w) k hk
  exact this

/-- اللازمُ: جداولُ صورٍ مودَعةٍ (الضمائر، الإشارة، الاستفهام، الشرط) لا عمليّةَ على آخرها. -/
theorem lazim_deposited :
    (Categories.pronouns ++ Ishara.forms.map (·.2) ++ Istifham.forms.map (·.2) ++
      Jazm.shartJazim.map (·.2)).all licensed = true ∧
    Categories.pronouns.length + Ishara.forms.length + Istifham.forms.length +
      Jazm.shartJazim.length = 71 := by decide

end Slge.Ism
