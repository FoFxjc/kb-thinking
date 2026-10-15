-- Reference queries behind the agent tools (illustrative, parameterised with psql variables).
-- Each tool call should also write one row to kg.call_audit (see the last example).

-- ---------------------------------------------------------------------
-- resolve_terms: map free text to concepts (exact label match, then fuzzy)
--   \set q '久期'
-- ---------------------------------------------------------------------
SELECT c.concept_id, c.pref_zh, c.pref_en, l.text AS matched, l.kind,
       similarity(l.normalized, lower(:'q')) AS score
FROM kg.label l
JOIN kg.concept c USING (concept_id)
WHERE l.normalized = lower(:'q')
   OR l.normalized % lower(:'q')            -- pg_trgm similarity
ORDER BY (l.normalized = lower(:'q')) DESC, score DESC
LIMIT 5;

-- ---------------------------------------------------------------------
-- get_concept: definition + direct relations in both directions
--   \set id 'risk.interest_rate'
-- ---------------------------------------------------------------------
SELECT c.concept_id, c.pref_zh, c.pref_en, c.definition_zh,
       r.rel, r.polarity,
       CASE WHEN r.src = c.concept_id THEN 'out' ELSE 'in' END AS direction,
       o.concept_id AS other_id, o.pref_zh AS other_zh
FROM kg.concept c
LEFT JOIN kg.relation r ON c.concept_id IN (r.src, r.dst)
LEFT JOIN kg.concept o  ON o.concept_id = CASE WHEN r.src = c.concept_id THEN r.dst ELSE r.src END
WHERE c.concept_id = :'id'
ORDER BY direction, r.rel;

-- ---------------------------------------------------------------------
-- explain_path: shortest relation path between two concepts (<= 3 hops,
-- traversing edges in both directions)
--   \set a 'macro.rate_hike'
--   \set b 'metric.duration'
-- ---------------------------------------------------------------------
WITH RECURSIVE edges AS (
  SELECT relation_id, src AS f, dst AS t FROM kg.relation WHERE status <> 'rejected'
  UNION ALL
  SELECT relation_id, dst, src FROM kg.relation WHERE status <> 'rejected'
), walk AS (
  SELECT t AS node, ARRAY[f, t] AS path, ARRAY[relation_id] AS rels, 1 AS depth
  FROM edges WHERE f = :'a'
  UNION ALL
  SELECT e.t, w.path || e.t, w.rels || e.relation_id, w.depth + 1
  FROM walk w JOIN edges e ON e.f = w.node
  WHERE w.depth < 3 AND NOT e.t = ANY (w.path)
)
SELECT path, rels, depth FROM walk WHERE node = :'b' ORDER BY depth LIMIT 3;

-- ---------------------------------------------------------------------
-- expand_query: labels of a concept, its narrower concepts and related
-- measures / mitigations, for ES query expansion
-- ---------------------------------------------------------------------
WITH targets AS (
  SELECT :'id'::text AS concept_id
  UNION
  SELECT src FROM kg.relation WHERE dst = :'id' AND rel IN ('is_a','measures','mitigates')
)
SELECT DISTINCT l.text, l.lang
FROM targets t JOIN kg.label l USING (concept_id)
WHERE l.kind IN ('pref','alt','abbr');

-- ---------------------------------------------------------------------
-- call_audit: one row per tool call
-- ---------------------------------------------------------------------
INSERT INTO kg.call_audit (call_id, trace_id, session_id, caller_type, caller_id, on_behalf_of,
                           channel, tool, request, response_concept_ids, response_relation_ids,
                           graph_version, status, latency_ms)
VALUES (gen_random_uuid()::text, 'trace-123', 'sess-456', 'agent', 'advisor-agent', 'user:alice',
        'mcp', 'explain_path', '{"a":"macro.rate_hike","b":"metric.duration"}',
        ARRAY['macro.rate_hike','market.bond_price','metric.duration'], ARRAY['rl-000099'],
        'seed-v0.1', 'ok', 12);
