-- PAYMENTS ICP — Query 2c: full-volume individual-payer estimate per workspace.
-- Goal: size the ICP prize. For each top-20 workspace from Q2b, show total VES inbound across
-- ALL 19 banks (not just identity-exposing 5). Use the concentration ratio observed on identity-exposing
-- banks to estimate the individual-payer volume hiding in the dark banks.
--
-- Output columns (per workspace):
--   total_tx / total_ves                 -- every VES inbound row in Q1 2026
--   identity_bank_tx / identity_bank_ves -- activity on the 5 identity-exposing banks (BDV, Exterior, BFC, Banesco, BBVA)
--   confirmed_individual_tx / _ves       -- rows that match the Q2b individual filter
--   individual_concentration_pct         -- confirmed_individual_ves / identity_bank_ves × 100
--   dark_bank_tx / dark_bank_ves         -- activity on the 14 dark banks (Bancamiga, Mercantil, BNC, etc.)
--   dark_individual_ves_estimate         -- dark_bank_ves × individual_concentration_pct
--   total_individual_ves_estimate        -- confirmed + dark estimate (the "prize")
--
-- Note on assumption: we extrapolate the concentration ratio from identity-exposing banks to dark banks.
-- Validity depends on the premise that the payer population is the same regardless of rail — reasonable
-- for a given workspace's customer base, but refine if per-bank rail-mix biases individuals vs B2B.

 
