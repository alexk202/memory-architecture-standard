# Synthetic Audit Report — red_s1

**Audit date:** 2026-10-27
**System:** synthetic stand (test vector, not a real system)
**Standard version:** MAQS v1.8.1
**Audited version:** commit 3f2a9c11e5b7402d8a6f1c0d94e37b52a81d6f0e (synthetic stand)
**Audit type:** static
**Auditor:** synthetic runner
**Controller:** synthetic
**Warnings:** not collected (a static audit ran nothing)

## Item Verdicts

| Item | Verdict | Evidence |
|------|---------|----------|
| **0.1** | yes | synthetic.md:1 |
| **0.2** | yes | synthetic.md:2 |
| **0.3** | yes | synthetic.md:3 |
| **0.4** | yes | synthetic.md:4 |
| **0.5** | yes | synthetic.md:5 |
| **0.5a** | yes | synthetic.md:6 |
| **0.6** | yes | synthetic.md:7 |
| **0.6a** | yes | synthetic.md:8 |
| **0.7** | yes | synthetic.md:9 |
| **0.8** | yes | synthetic.md:10 |
| **A1** | yes | synthetic.md:11 |
| **A2** | yes | synthetic.md:12 |
| **A3** | yes | synthetic.md:13 |
| **A4** | yes | synthetic.md:14 |
| **A5** | yes | synthetic.md:15 |
| **A6** | yes | synthetic.md:16 |
| **A7** | yes | synthetic.md:17 |
| **B1** | yes | synthetic.md:18 |
| **B2** | yes | synthetic.md:19 |
| **B3** | yes | synthetic.md:20 |
| **B4** | yes | synthetic.md:21 |
| **B5** | yes | synthetic.md:22 |
| **B6** | yes | synthetic.md:23 |
| **C1** | yes | synthetic.md:24 |
| **C2** | yes | synthetic.md:25 |
| **C3** | yes | synthetic.md:26 |
| **C4** | yes | synthetic.md:27 |
| **C5** | yes | synthetic.md:28 |
| **C6** | yes | synthetic.md:29 |
| **C7** | yes | synthetic.md:30 |
| **C8** | yes | synthetic.md:31 |
| **D1** | yes | synthetic.md:32 |
| **D2** | yes | synthetic.md:33 |
| **D3** | yes | synthetic.md:34 |
| **D4** | yes | synthetic.md:35 |
| **D5** | yes | synthetic.md:36 |
| **D6** | yes | synthetic.md:37 |
| **D7** | yes | synthetic.md:38 |
| **D8** | yes | synthetic.md:39 |
| **D9** | yes | synthetic.md:40 |
| **E1** | yes | synthetic.md:41 |
| **E2** | yes | synthetic.md:42 |
| **E3** | yes | synthetic.md:43 |
| **E4** | yes | synthetic.md:44 |
| **E5** | yes | synthetic.md:45 |
| **E6** | yes | synthetic.md:46 |
| **E7** | yes | synthetic.md:47 |
| **E8** | yes | synthetic.md:48 |
| **E9** | yes | synthetic.md:49 |
| **E10** | yes | synthetic.md:50 |
| **E11** | yes | synthetic.md:51 |
| **E12** | yes | synthetic.md:52 |
| **E13** | yes | synthetic.md:53 |
| **F1** | yes | synthetic.md:54 |
| **F2** | yes | synthetic.md:55 |
| **F3** | yes | synthetic.md:56 |
| **F4** | yes | synthetic.md:57 |
| **F5** | yes | synthetic.md:58 |
| **F6** | yes | synthetic.md:59 |
| **F7** | yes | synthetic.md:60 |
| **F8** | yes | synthetic.md:61 |
| **G1** | yes | synthetic.md:62 |
| **G2** | yes | synthetic.md:63 |
| **G3** | yes | synthetic.md:64 |
| **G4** | yes | synthetic.md:65 |
| **G5** | yes | synthetic.md:66 |
| **G6** | yes | synthetic.md:67 |
| **G7** | yes | synthetic.md:68 |
| **H1** | yes | synthetic.md:69 |
| **H2** | yes | synthetic.md:70 |
| **H3** | yes | synthetic.md:71 |
| **H4** | yes | synthetic.md:72 |
| **H5** | yes | synthetic.md:73 |
| **H6** | yes | synthetic.md:74 |
| **I1** | yes | synthetic.md:75 |
| **I2** | yes | synthetic.md:76 |
| **I3** | yes | synthetic.md:77 |
| **I4** | yes | synthetic.md:78 |
| **I5** | yes | synthetic.md:79 |
| **I6** | yes | synthetic.md:80 |
| **I7** | yes | synthetic.md:81 |
| **I8** | yes | synthetic.md:82 |
| **I9** | yes | synthetic.md:83 |
| **I10** | yes | synthetic.md:84 |
| **I11** | yes | synthetic.md:85 |
| **I12** | yes | synthetic.md:86 |
| **I13** | yes | synthetic.md:87 |
| **I14** | yes | synthetic.md:88 |
| **I15** | yes | synthetic.md:89 |
| **I16** | yes | synthetic.md:90 |
| **J1** | yes | synthetic.md:91 |
| **J2** | yes | synthetic.md:92 |
| **J3** | yes | synthetic.md:93 |
| **J4** | yes | synthetic.md:94 |
| **J5** | yes | synthetic.md:95 |
| **J6** | yes | synthetic.md:96 |

## Audit Results

| Section | Items | Yes | Partial | No | N/A | Failed [CRIT] |
|---------|-------|-----|---------|----|-----|----------------|
| 0. System Map | 10 | 10 | 0 | 0 | 0 | 0 |
| A. Input Validation | 7 | 7 | 0 | 0 | 0 | 0 |
| B. Write Integrity | 6 | 6 | 0 | 0 | 0 | 0 |
| C. Growth Management | 8 | 8 | 0 | 0 | 0 | 0 |
| D. Retrieval | 9 | 9 | 0 | 0 | 0 | 0 |
| E. Context Assembly | 13 | 13 | 0 | 0 | 0 | 0 |
| F. Feedback Loop | 8 | 8 | 0 | 0 | 0 | 0 |
| G. Isolation | 7 | 7 | 0 | 0 | 0 | 0 |
| H. Concurrency | 6 | 6 | 0 | 0 | 0 | 0 |
| I. Observability | 16 | 16 | 0 | 0 | 0 | 0 |
| J. Change Management | 6 | 6 | 0 | 0 | 0 | 0 |

## Critical Failures

| Item | Evidence | Impact | Proposed Fix |
|------|----------|--------|-------------|
| | | | |

## Important Failures

| Item | Evidence | Impact | Proposed Fix |
|------|----------|--------|-------------|
| | | | |

## Verdict

- [ ] **DOES NOT PASS** — [CRIT] failures: ___
- [ ] **PASSES WITH CAVEATS** — [CRIT] clean, [IMP] failures: ___
- [x] **CONFORMS** — no [CRIT]/[IMP] failures
