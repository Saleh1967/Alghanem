import Slge.Bridge

/-!
# الأقانيم: الصنفُ مجموعةُ أعدادٍ بعضويّةٍ قابلةٍ للفصل

«SLGE الضمائر» و«SLGE الإشارة» و… ليست طبقاتٍ صوتيّة؛ كلٌّ منها **أقنوم** ‎χ : List SCell → Bool‎
يحقّق ثلاثة: (أ) **السلامة**: كلُّ ما يقبله مرخَّص (`Sound`)، (ب) **الاحتواء** في أقنومٍ أعلى
(`Sub`)، (ج) **المانعيّة** بين أقنومين (`Exclusive`). والاكتمالُ على شريحة MASAQ **قياسٌ** يُطبع
في بايثون لا يُبرهَن هنا.

الأقنومُ الأوّل المودَع: **الضمائر المنفصلة** الاثنا عشر، خاناتُها مأخوذةٌ من شهادات بوّابة الغانم
(لا مكتوبةً باليد)، ومبرهَنٌ عليها بالحساب: مرخَّصةٌ كلُّها (`pronoun_sound`)، أعدادُها متباينة
(`pronoun_numbers_nodup`)، وهي أقنومٌ تحت المرخَّص (`pronoun_sub_licensed`).
-/

namespace Slge.Categories

/-- الأقنوم: عضويّةٌ قابلةٌ للفصل. -/
abbrev Aqnum := List SCell → Bool

/-- السلامة: لا يقبل إلّا مرخَّصًا. -/
def Sound (χ : Aqnum) : Prop := ∀ w, χ w = true → licensed w = true

/-- الاحتواء. -/
def Sub (χ ψ : Aqnum) : Prop := ∀ w, χ w = true → ψ w = true

/-- المانعيّة: لا كلمةَ في الأقنومين معًا. -/
def Exclusive (χ ψ : Aqnum) : Prop := ∀ w, χ w = true → ψ w = false

theorem sub_refl (χ : Aqnum) : Sub χ χ := fun _ h => h

theorem sub_trans {χ ψ ω : Aqnum} (h1 : Sub χ ψ) (h2 : Sub ψ ω) : Sub χ ω :=
  fun w h => h2 w (h1 w h)

theorem sound_of_sub {χ ψ : Aqnum} (h : Sub χ ψ) (hs : Sound ψ) : Sound χ :=
  fun w hw => hs w (h w hw)

/-- أقنومٌ من قائمةٍ منتهية. -/
def ofList (l : List (List SCell)) : Aqnum := fun w => l.contains w

theorem ofList_sound (l : List (List SCell)) (h : ∀ w ∈ l, licensed w = true) :
    Sound (ofList l) := by
  intro w hw
  simp only [ofList, List.contains_iff_mem] at hw
  exact h w hw

/-! ## الأقنومُ الأوّل: الضمائر المنفصلة -/

/-- خانةٌ من موضعَي SLGE. -/
def c (k s : Nat) (hk : k < 29 := by decide) (hs : s < 4 := by decide) : SCell := ⟨⟨k, hk⟩, ⟨s, hs⟩⟩

/-- الاثنا عشر: أَنَا، نَحْنُ، أَنْتَ، أَنْتِ، أَنْتُمَا، أَنْتُمْ، أَنْتُنَّ، هُوَ، هِيَ، هُمَا، هُمْ، هُنَّ
(خاناتُها من `gate.enter` في الغانم، 2026-10-06). -/
def pronouns : List (List SCell) := [
  [c 0 0, c 25 0, c 1 3],                       -- أَنَا
  [c 25 0, c 6 3, c 25 2],                      -- نَحْنُ
  [c 0 0, c 25 3, c 3 0],                       -- أَنْتَ
  [c 0 0, c 25 3, c 3 1],                       -- أَنْتِ
  [c 0 0, c 25 3, c 3 2, c 24 0, c 1 3],        -- أَنْتُمَا
  [c 0 0, c 25 3, c 3 2, c 24 3],               -- أَنْتُمْ
  [c 0 0, c 25 3, c 3 2, c 25 3, c 25 0],       -- أَنْتُنَّ
  [c 26 2, c 27 0],                             -- هُوَ
  [c 26 1, c 28 0],                             -- هِيَ
  [c 26 2, c 24 0, c 1 3],                      -- هُمَا
  [c 26 2, c 24 3],                             -- هُمْ
  [c 26 2, c 25 3, c 25 0]                      -- هُنَّ
]

def pronoun : Aqnum := ofList pronouns

theorem pronouns_licensed : ∀ w ∈ pronouns, licensed w = true := by decide

theorem pronoun_sound : Sound pronoun := ofList_sound pronouns pronouns_licensed

theorem pronoun_sub_licensed : Sub pronoun (fun w => licensed w) := pronoun_sound

/-- أعدادُ الضمائر بطيّها متباينة: لكلٍّ بصمتُه. -/
theorem pronoun_numbers_nodup : (pronouns.map slgeFold).Nodup := by decide

/-- وأشكالُها ليست بصمة: هُوَ وهِيَ تتابعُ سكونٍ واحدٌ وكلمتان مختلفتان. -/
theorem pronoun_shape_not_fingerprint :
    (pronouns.getD 7 []).map SCell.isSukun = (pronouns.getD 8 []).map SCell.isSukun ∧
    pronouns.getD 7 [] ≠ pronouns.getD 8 [] := by decide

end Slge.Categories
