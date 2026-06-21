-- SANITY CHECK — workspace name → id resolution
-- Run this FIRST to confirm each input name maps to exactly one (active) workspace.
-- Red flags:
--   * NULL workspace_id row     = pattern matched nothing (need to relax pattern)
--   * Multiple rows per input   = pattern is ambiguous (need to narrow / add exclude)
--   * is_discarded = true row   = workspace exists but is churned (decide if you still want it)

WITH inputs(input_name, pattern, exclude) AS (
  VALUES
    ('Procesadora Marsoca',         '%marsoca%',                    NULL::text),
    ('Molinos Carabobo SA',         '%molinos%carabobo%',           NULL),
    ('Molinos Nacionales CA',       '%molinos%nacionales%',         NULL),
    ('AVICOLA LAS TUNAS',           '%avicola%tunas%',              NULL),
    ('Grupo Maralac',               '%maralac%',                    NULL),
    ('Casa Franceschi',             '%franceschi%',                 NULL),
    ('CAMOR INTERNACIONAL',         '%camor%',                      NULL),
    ('PASTCA',                      '%pastca%',                     NULL),
    ('ALMACENADORA ASOPORTUGUESA',  '%almacenadora%asoportuguesa%', NULL),
    ('ALIMENTOS LPRADO',            '%lprado%',                     NULL),
    ('alimentosmunchy',             '%munchy%',                     NULL),
    ('ALIMENTOS DOÑA EMILIA',       '%emilia%',                     NULL),
    ('Asoportuguesa',               '%asoportuguesa%',              '%almacenadora%'),
    ('Capitalfoods',                '%capital%foods%',              NULL),
    ('suvica',                      '%suvica%',                     NULL),
    ('Alimentos Global',            '%alimentos%global%',           NULL),
    ('Casagri de Lara',             '%casagri%',                    NULL),
    ('Grupo Mimesa',                '%mimesa%',                     NULL),
    ('Alimentos Alvarigua, c.a.',   '%alvarigua%',                  NULL),
    ('TORONDOY',                    '%torondoy%',                   NULL),
    ('Corporación JSL, C.A.',       '%jsl%',                        NULL),
    ('ARAWAK',                      '%arawak%',                     NULL),
    ('ASOPRODUCTOS',                '%asoproductos%',               NULL),
    ('Protinal',                    '%protinal%',                   NULL)
)
SELECT
  i.input_name,
  w.id                                AS workspace_id,
  w.name                              AS matched_name,
  (w.discarded_at IS NOT NULL)        AS is_discarded,
  COUNT(*) OVER (PARTITION BY i.input_name) AS match_count
FROM inputs i
LEFT JOIN workspaces w
  ON w.name ILIKE i.pattern
 AND (i.exclude IS NULL OR w.name NOT ILIKE i.exclude)
ORDER BY i.input_name, matched_name;
