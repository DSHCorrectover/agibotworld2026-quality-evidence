# agibotworld2026-quality-evidence

**Independent, replayable quality-evidence receipt for the public embodied-AI dataset
[`agibot-world/AgiBotWorld2026`](https://huggingface.co/datasets/agibot-world/AgiBotWorld2026).**

We do not score the dataset. We make the observable facts **third-party verifiable**:
a full structural census (17.5 TB / 804,554 files / 10,088 dirs, crawled 2026-11-25 at revision
`95b159a10305a0385f369aba5d4b16242526d17b`), cross-checked against the publisher's own internal
build receipt, signed with Ed25519, and replayable end-to-end from public endpoints.

Mapped to the machine-verifiable subset of China's industry standard **YD/T 6771-2026**
(《具身智能数据集质量要求及评估方法》, effective 2026-11-01) — see `check.py` docstring for the
per-dimension mapping. Dimensions that require content judgment are **held, never promoted**.

## Verify in one line (no trust in us required)

```bash
python3 verify.py
```

`SIGNATURE VALID` proves `evidence/evidence.json` is byte-identical to what we signed with the
published `evidence/pubkey.pem`. Then re-run the whole check yourself:

```bash
python3 check.py   # fresh full crawl (~815 pages, ~25 min) + sample fetches + cross-check + sign
```

## What the receipt says (as published)

**Cross-check (the anchor):** the publisher's internal build receipt
(`PhysicalReasoning/.dataset_build/snapshot/_datahub_export/verification.json`, sha256
`f9c0a69a…`) claims `completedEpisodes: 8146 + preservedEpisodes: 126 = 8272`; our independent
crawl observed **exactly 8,272 parquet files**. Publisher-internal ledger == external observation.

**Findings (named, not scored):**
1. **Category skew** — 99.9% of tree entries sit under `PhysicalReasoning`; the five other
   declared categories are thin shells. A structural-diversity fact the dataset card does not surface.
2. **Hidden internal build dirs published** — `.dataset_build` (incl. the verification receipt
   itself) and `.denseprompt_merge` ship inside the open dataset.
3. **Dual dated snapshots** — `opensourcev4-20261001` / `opensourcev4-20261003` with task-id
   overlap stated in the receipt.
4. **HF siblings API silently truncates at 100,000 entries** — the true tree is 814,642 paths.
   Metadata consumers relying on `siblings` see a quarter of the iceberg in a dataset of this size
   (and 99.94% of it is one category, so the truncation is invisible in shape).

**Held (never promoted):** trajectory content quality, perceptual diversity, usability beyond
documented structure — these need content judgment or training runs we did not perform.

## Method notes (disclosed)

- Crawl source: `hf-mirror.com` (huggingface.co was unreachable from our egress; both endpoints
  serve the same repo; revision sha + lastModified pinned in the receipt). CI re-crawls fresh.
- The tree census is deduplicated by path; every number in the receipt is recomputed by `check.py`
  from the crawl — nothing hand-typed.
- Samples: 2 small files fetched, sha256'd, archived under `evidence/samples/`.
- Key hygiene: a fresh Ed25519 keypair is generated per evidence run; the private key is deleted
  after signing (see `check.py`), the public key is published in-repo.

## Why this exists

China's embodied-AI data standards (YD/T 6771 effective 2026-11-01; national standards program
launched 2026-11-22 by the National Data Administration) push dataset quality evaluation toward
"一次测评、全国互认" and data-asset capitalization. Evaluation *conclusions* are only as good as
their evidence. This receipt is a working specimen of the evidence layer: conclusions → signed,
replayable, offline-verifiable facts that don't require trusting the party that produced them.

Contact: Guigui Wang <wangguigui@correctover.com> — Correctover · AI Reliability
