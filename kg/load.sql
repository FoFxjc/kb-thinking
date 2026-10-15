-- Load the seed concept graph into PostgreSQL.
-- Run from the repository root:
--   psql -d <db> -f kg/schema.sql
--   psql -d <db> -f kg/load.sql

\copy kg.concept  (concept_id, scheme, pref_zh, pref_en, definition_zh, definition_en, scope_note, jurisdiction, tier, layer, status, version) FROM 'kg/seed/concept.csv'  WITH (FORMAT csv, HEADER true)
\copy kg.label    (label_id, concept_id, text, lang, kind, normalized, layer, status)                                   FROM 'kg/seed/label.csv'    WITH (FORMAT csv, HEADER true)
\copy kg.relation (relation_id, src, rel, dst, polarity, confidence, note, layer, status)                               FROM 'kg/seed/relation.csv' WITH (FORMAT csv, HEADER true)
\copy kg.evidence (evidence_id, target_type, target_id, evidence_type, source_name, locator, lookup_term, verified, doc_id, chunk_id, quote, note, created_by) FROM 'kg/seed/evidence.csv' WITH (FORMAT csv, HEADER true)

SELECT 'concept'  AS t, count(*) FROM kg.concept
UNION ALL SELECT 'label',    count(*) FROM kg.label
UNION ALL SELECT 'relation', count(*) FROM kg.relation
UNION ALL SELECT 'evidence', count(*) FROM kg.evidence;
