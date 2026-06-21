-- PAYMENTS ICP — Query 2d: ICP tiering with payer-diversity checks.
-- Goal: drop single-source / noise workspaces from Q2c and classify the rest into tiers by confidence.
--
-- Adds to Q2c:
--   unique_payer_cedulas   -- distinct V/E cedulas extracted from descriptions
--   top10_cedula_pct       -- % of confirmed individual volume concentrated in top 10 cedulas (disguise signal)
--   icp_tier               -- 1 (high-confidence), 2 (medium), 3 (speculative)
--
-- ICP tier logic (all 4 conditions must hold):
--   Tier 1 — individual_concentration_pct >= 15  AND  identity_coverage_pct >= 50
--            AND unique_cedulas >= 100            AND  top10_cedula_pct <= 50
--   Tier 2 — individual_concentration_pct >= 10  AND  identity_coverage_pct >= 30
--            AND unique_cedulas >= 30             AND  top10_cedula_pct <= 70
--   Tier 3 — everything else.
--
-- Cedula extraction: greedy match of [VE][0-9]{7,10} (covers Venezuelan cedula formats).
-- BBVA's compressed TRAV...0000 format may produce slightly-truncated cedulas — diversity count is approximate there.

 
