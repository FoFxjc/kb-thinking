#!/usr/bin/env python3
"""Validate the concept graph seed CSVs (kg/seed/*.csv).

Checks
  1. Every concept has scheme, zh/en pref labels and definitions.
  2. Labels reference existing concepts; exactly one pref label per (concept, lang).
  3. Relations use the fixed relation set; endpoints exist; no self-loops;
     polarity only on 'affects'; no duplicate symmetric pairs; is_a stays
     within one scheme; no suitable_for in the base layer.
  4. 'is_a' and 'part_of' hierarchies are acyclic.
  5. Evidence targets exist; every concept and relation has authoring evidence.
  6. Reports labels shared by several concepts (ambiguity the tagger must resolve).

Usage: python3 kg/tools/validate.py [seed_dir]
Exit code 1 if any error is found; ambiguity is reported as a warning.
"""
import csv
import os
import sys
from collections import defaultdict

SCHEMES = {"asset_class", "instrument", "risk", "metric", "strategy",
           "macro", "market", "suitability", "behavioral", "terms"}
RELS = {"is_a", "part_of", "input_of", "belongs_to", "measures", "affects", "mitigates",
        "exposed_to", "suitable_for", "opposite_of", "related"}
SYMMETRIC = {"opposite_of", "related"}
HIERARCHICAL = {"is_a", "part_of", "input_of"}


def load(seed, name):
    with open(os.path.join(seed, name), encoding="utf-8") as f:
        return list(csv.DictReader(f))


def find_cycle(edges):
    graph = defaultdict(list)
    for a, b in edges:
        graph[a].append(b)
    state = {}

    def dfs(n, path):
        state[n] = 1
        for m in graph[n]:
            if state.get(m) == 1:
                return path + [n, m]
            if m not in state:
                cyc = dfs(m, path + [n])
                if cyc:
                    return cyc
        state[n] = 2
        return None

    for n in list(graph):
        if n not in state:
            cyc = dfs(n, [])
            if cyc:
                return cyc
    return None


def main():
    seed = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "seed")
    concepts = load(seed, "concept.csv")
    labels = load(seed, "label.csv")
    relations = load(seed, "relation.csv")
    evidence = load(seed, "evidence.csv")
    errors, warnings = [], []

    ids = {c["concept_id"] for c in concepts}
    if len(ids) != len(concepts):
        errors.append("duplicate concept_id")
    for c in concepts:
        if c["scheme"] not in SCHEMES:
            errors.append(f"{c['concept_id']}: bad scheme {c['scheme']}")
        for k in ("pref_zh", "pref_en", "definition_zh", "definition_en"):
            if not c[k].strip():
                errors.append(f"{c['concept_id']}: missing {k}")

    prefs = defaultdict(int)
    by_norm = defaultdict(set)
    for l in labels:
        if l["concept_id"] not in ids:
            errors.append(f"{l['label_id']}: unknown concept {l['concept_id']}")
        if l["kind"] == "pref":
            prefs[(l["concept_id"], l["lang"])] += 1
        by_norm[(l["lang"], l["normalized"])].add(l["concept_id"])
    for cid in ids:
        for lang in ("zh", "en"):
            if prefs[(cid, lang)] != 1:
                errors.append(f"{cid}: {prefs[(cid, lang)]} pref labels for {lang}")
    for (lang, text), cids in sorted(by_norm.items()):
        if len(cids) > 1:
            warnings.append(f"ambiguous label [{lang}] '{text}' -> {', '.join(sorted(cids))}")

    rel_ids = set()
    sym_pairs = set()
    hier = defaultdict(list)
    for r in relations:
        rel_ids.add(r["relation_id"])
        if r["rel"] not in RELS:
            errors.append(f"{r['relation_id']}: bad rel {r['rel']}")
        for end in ("src", "dst"):
            if r[end] not in ids:
                errors.append(f"{r['relation_id']}: unknown {end} {r[end]}")
        if r["src"] == r["dst"]:
            errors.append(f"{r['relation_id']}: self-loop")
        if r["rel"] == "suitable_for" and r["layer"] == "base":
            errors.append(f"{r['relation_id']}: suitable_for is not allowed in the base layer")
        if r["rel"] == "is_a":
            sc = {c["concept_id"]: c["scheme"] for c in concepts}
            if sc.get(r["src"]) != sc.get(r["dst"]):
                errors.append(f"{r['relation_id']}: is_a across schemes {sc.get(r['src'])} -> {sc.get(r['dst'])}")
        if r["polarity"] and r["rel"] != "affects":
            errors.append(f"{r['relation_id']}: polarity on {r['rel']}")
        if r["rel"] in SYMMETRIC:
            key = (r["rel"], frozenset((r["src"], r["dst"])))
            if key in sym_pairs:
                errors.append(f"{r['relation_id']}: duplicate symmetric {r['rel']} {r['src']}~{r['dst']}")
            sym_pairs.add(key)
        if r["rel"] in HIERARCHICAL:
            hier[r["rel"]].append((r["src"], r["dst"]))
    for rel, edges in hier.items():
        cyc = find_cycle(edges)
        if cyc:
            errors.append(f"cycle in {rel}: {' -> '.join(cyc)}")

    label_ids = {l["label_id"] for l in labels}
    targets = {"concept": ids, "relation": rel_ids, "label": label_ids}
    authored = defaultdict(set)
    for e in evidence:
        if e["target_id"] not in targets.get(e["target_type"], set()):
            errors.append(f"{e['evidence_id']}: unknown target {e['target_type']}:{e['target_id']}")
        if e["evidence_type"] == "authoring":
            authored[e["target_type"]].add(e["target_id"])
    for cid in ids - authored["concept"]:
        errors.append(f"{cid}: no authoring evidence")
    for rid in rel_ids - authored["relation"]:
        errors.append(f"{rid}: no authoring evidence")

    # summary
    per_scheme = defaultdict(int)
    for c in concepts:
        per_scheme[c["scheme"]] += 1
    per_rel = defaultdict(int)
    for r in relations:
        per_rel[r["rel"]] += 1
    linked = {r["src"] for r in relations} | {r["dst"] for r in relations}
    isolated = sorted(ids - linked)

    print(f"concepts {len(concepts)} · labels {len(labels)} · relations {len(relations)} · evidence {len(evidence)}")
    print("by scheme  : " + ", ".join(f"{k} {v}" for k, v in sorted(per_scheme.items())))
    print("by relation: " + ", ".join(f"{k} {v}" for k, v in sorted(per_rel.items())))
    if isolated:
        warnings.append(f"isolated concepts (no relations): {', '.join(isolated)}")
    for w in warnings:
        print("WARN  " + w)
    for e in errors:
        print("ERROR " + e)
    print("OK" if not errors else f"{len(errors)} error(s)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
