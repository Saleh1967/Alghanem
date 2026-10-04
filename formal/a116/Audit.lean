import A116

/-!
تدقيقُ المسلّمات: لا يُقبَل برهانٌ يستند إلى `sorryAx` أو إلى مسلّمةٍ غيرِ
المسلّمات القياسيّة في Lean (`propext`، `Classical.choice`، `Quot.sound`).
ويفحص CI هذا المخرَج ويسقط إن ظهر فيه `sorryAx` أو `Lean.ofReduceBool`
(أثرُ `native_decide`، وهو ثقةٌ بالمترجِم لا بالنواة).
-/

#print axioms A116.mem_cells
#print axioms A116.cells_nodup
#print axioms A116.cells_length
#print axioms A116.cells_split
#print axioms A116.step_depends_only_on_sukun
#print axioms A116.run_fellOut
#print axioms A116.saturation_rungs
#print axioms A116.Sstar_closed
#print axioms A116.run_mem_Sstar
#print axioms A116.Sstar_complete
#print axioms A116.run_ne_fellOut_iff
#print axioms A116.run_eq_fellOut_iff
#print axioms A116.Fold.T_succ_succ
#print axioms A116.Fold.fold_lt
#print axioms A116.Fold.unfold_fold
#print axioms A116.Fold.unfold_spec
#print axioms A116.Fold.fold_injective
#print axioms A116.Fold.foldAny_injective
#print axioms A116.Fold.foldAny_surjective
#print axioms A116.admissible_iff_valid
#print axioms A116.run_ne_fellOut_iff_valid
#print axioms A116.cellFold_lt
#print axioms A116.cellFold_injective
#print axioms A116.cellFold_surjective
#print axioms A116.U_succ_succ
#print axioms A116.U_values
#print axioms A116.hamil_ladder
#print axioms A116.Fiber.decode_encode
#print axioms A116.Fiber.encode_injective
#print axioms A116.Fiber.decode_sound
#print axioms A116.Fiber.rank_lt
#print axioms A116.Fiber.fiber_length_le
#print axioms A116.Fiber.fiber_length_le_two_pow
#print axioms A116.Fiber.nodup_fin_length_le
#print axioms A116.Numbering.valid_zero_iff
#print axioms A116.Numbering.fold_zero_eq_digits
#print axioms A116.Numbering.foldAny_zero_closed
#print axioms A116.Numbering.bridgeCell_bridgeIndex
#print axioms A116.Numbering.bridgeIndex_bridgeCell
#print axioms A116.Numbering.orders_differ_only_in_two_rows
#print axioms A116.Numbering.atomNumber_closed
#print axioms A116.Numbering.atomNumber_injective
#print axioms A116.Numbering.atomNumber_surjective
#print axioms A116.Numbering.pair_injective
#print axioms A116.Numbering.pair_surjective
#print axioms A116.Numbering.pair_closed
