-- =====================================================================
-- Finance investment concept graph · PostgreSQL schema (v0.1)
--
-- Five tables:
--   kg.concept     概念：金融投资概念（不含具体公司、证券、持仓）
--   kg.label       标签：中英文首选名、别名、缩写、隐藏词（术语识别用）
--   kg.relation    关系：固定类型的有向关系
--   kg.evidence    证据：概念 / 标签 / 关系的出处与来源
--   kg.call_audit  调用审计：Agent / Portal 对图谱工具的每一次调用
--
-- Modelling follows W3C SKOS semantics for labels and hierarchy
-- (prefLabel / altLabel / hiddenLabel, broader), extended with a small,
-- fixed set of domain relations for investment reasoning.
-- =====================================================================

CREATE SCHEMA IF NOT EXISTS kg;
CREATE EXTENSION IF NOT EXISTS pg_trgm;   -- fuzzy term matching

-- ---------------------------------------------------------------------
-- 1. concept
-- ---------------------------------------------------------------------
CREATE TABLE kg.concept (
  concept_id     text PRIMARY KEY,               -- e.g. 'risk.interest_rate'
  scheme         text NOT NULL CHECK (scheme IN (
                   'asset_class','instrument','risk','metric','strategy',
                   'macro','market','suitability','behavioral')),
  pref_zh        text NOT NULL,
  pref_en        text NOT NULL,
  definition_zh  text NOT NULL,
  definition_en  text NOT NULL,
  scope_note     text,                           -- usage notes, caveats
  layer          text NOT NULL DEFAULT 'base'
                   CHECK (layer IN ('base','doc')),
  status         text NOT NULL DEFAULT 'draft'
                   CHECK (status IN ('draft','confirmed','pending','rejected','deprecated')),
  version        int  NOT NULL DEFAULT 1,
  created_at     timestamptz NOT NULL DEFAULT now(),
  updated_at     timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX ON kg.concept (scheme);

-- ---------------------------------------------------------------------
-- 2. label
-- ---------------------------------------------------------------------
CREATE TABLE kg.label (
  label_id     text PRIMARY KEY,                 -- e.g. 'lb-000123'
  concept_id   text NOT NULL REFERENCES kg.concept ON DELETE CASCADE,
  text         text NOT NULL,
  lang         text NOT NULL CHECK (lang IN ('zh','en')),
  kind         text NOT NULL CHECK (kind IN ('pref','alt','abbr','hidden')),
  normalized   text NOT NULL,                    -- lower-case, trimmed, punctuation-light
  layer        text NOT NULL DEFAULT 'base' CHECK (layer IN ('base','doc')),
  status       text NOT NULL DEFAULT 'draft'
                 CHECK (status IN ('draft','confirmed','pending','rejected')),
  UNIQUE (concept_id, lang, normalized)
);
CREATE INDEX ON kg.label (normalized);
CREATE INDEX ON kg.label USING gin (normalized gin_trgm_ops);
-- Exactly one pref label per (concept, lang)
CREATE UNIQUE INDEX label_one_pref ON kg.label (concept_id, lang) WHERE kind = 'pref';

-- ---------------------------------------------------------------------
-- 3. relation
-- ---------------------------------------------------------------------
CREATE TABLE kg.relation (
  relation_id  text PRIMARY KEY,                 -- e.g. 'rl-000045'
  src          text NOT NULL REFERENCES kg.concept,
  rel          text NOT NULL CHECK (rel IN (
                 'is_a',          -- src is a kind of dst (SKOS broader)
                 'part_of',       -- src is a component of dst
                 'measures',      -- metric src quantifies dst
                 'affects',       -- driver src moves dst; see polarity
                 'mitigates',     -- strategy/instrument src reduces risk dst
                 'exposed_to',    -- asset/instrument src carries risk dst
                 'suitable_for',  -- product src indicatively fits investor type dst
                 'opposite_of',   -- symmetric contrast
                 'related')),     -- symmetric weak association
  dst          text NOT NULL REFERENCES kg.concept,
  polarity     smallint CHECK (polarity IN (-1, 1)),   -- only for 'affects'; NULL = depends
  confidence   real NOT NULL DEFAULT 1.0 CHECK (confidence BETWEEN 0 AND 1),
  note         text,
  layer        text NOT NULL DEFAULT 'base' CHECK (layer IN ('base','doc')),
  status       text NOT NULL DEFAULT 'draft'
                 CHECK (status IN ('draft','confirmed','pending','rejected')),
  CHECK (src <> dst),
  CHECK (polarity IS NULL OR rel = 'affects'),
  UNIQUE (src, rel, dst)
);
CREATE INDEX ON kg.relation (dst, rel);

-- ---------------------------------------------------------------------
-- 4. evidence
-- ---------------------------------------------------------------------
CREATE TABLE kg.evidence (
  evidence_id    text PRIMARY KEY,               -- e.g. 'ev-000789'
  target_type    text NOT NULL CHECK (target_type IN ('concept','label','relation')),
  target_id      text NOT NULL,                  -- concept_id / label_id / relation_id
  evidence_type  text NOT NULL CHECK (evidence_type IN (
                   'authoring',      -- who/what created it (seed, LLM draft, expert)
                   'reference',      -- external authoritative source to verify against
                   'doc_chunk',      -- extracted from an indexed document chunk
                   'expert_review')),-- reviewer decision
  source_name    text NOT NULL,
  locator        text,                           -- URL, Ozone URI or internal ref
  lookup_term    text,                           -- term to look up at the locator
  verified       boolean NOT NULL DEFAULT false, -- has a human checked it?
  doc_id         text,                           -- for doc_chunk
  chunk_id       text,                           -- for doc_chunk (ES chunk id)
  quote          text,                           -- short excerpt (doc_chunk only)
  note           text,
  created_by     text NOT NULL,
  created_at     timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX ON kg.evidence (target_type, target_id);
CREATE INDEX ON kg.evidence (doc_id) WHERE doc_id IS NOT NULL;

-- ---------------------------------------------------------------------
-- 5. call_audit
-- ---------------------------------------------------------------------
CREATE TABLE kg.call_audit (
  call_id               text PRIMARY KEY,        -- uuid
  called_at             timestamptz NOT NULL DEFAULT now(),
  trace_id              text,                    -- end-to-end request trace
  session_id            text,                    -- agent / chat session
  caller_type           text NOT NULL CHECK (caller_type IN ('agent','user','service')),
  caller_id             text NOT NULL,           -- agent id / service account / user
  on_behalf_of          text,                    -- end user the agent acts for
  channel               text CHECK (channel IN ('mcp','portal','api')),
  tool                  text NOT NULL CHECK (tool IN (
                          'resolve_terms','get_concept','explain_path',
                          'expand_query','search_concepts')),
  request               jsonb NOT NULL,          -- tool input
  response_concept_ids  text[],                  -- concepts returned
  response_relation_ids text[],                  -- relations returned (paths)
  graph_version         text NOT NULL,           -- seed / release tag served
  status                text NOT NULL CHECK (status IN ('ok','empty','error','denied')),
  latency_ms            int,
  error                 text
);
CREATE INDEX ON kg.call_audit (called_at);
CREATE INDEX ON kg.call_audit (caller_id, called_at);
CREATE INDEX ON kg.call_audit USING gin (response_concept_ids);
