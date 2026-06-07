<!-- generated-by: qa-workflow-toolkit -->
<!-- wiki-name: [[wiki_name]] -->
<!-- wiki-type: [[wiki_type]] -->

# [[wiki_name]] Test Viewpoint Wiki

This repository is a Markdown knowledge base maintained by LLM agents. Its goal is to accumulate **test viewpoints** (テスト観点) derived from existing test cases, so the same product's future test design and test strategy can build on durable, evidence-backed knowledge instead of re-deriving it every time.

The raw evidence is existing test cases. From them, the wiki keeps three layers of knowledge: summaries of the source test cases, reusable test viewpoints extracted from them, and product-specific glossary terms.

## Structure

- `raw/`: Converted or collected source test cases. Treat them as immutable evidence by default.
- `.temp/`: Temporary staging area for files before conversion into `raw/`.
- `wiki/`: Knowledge pages created and updated by LLM agents. New pages must go into one of the subfolders below.
- `wiki/testcases/`: Summaries of source test cases. Use one page per primary source, and keep the page focused on what that source actually tests.
- `wiki/viewpoints/`: Reusable test viewpoints extracted from the sources. Use these for viewpoints, perspectives, and check angles that can be reused for other features or future test design.
- `wiki/glossary/`: Product-specific terms, names, and conventions learned from the sources.
- `index.md`: Content index for the whole wiki. Check it first before ingest or query work.
- `log.md`: Append-only chronological log for ingest, query, lint, and convert operations.
- Agent-specific commands: Slash commands for wiki operations.

## Core Policies

- **No speculation. This is the most important rule.** For test viewpoints, adding information that is not a fact is fatal. Never invent, guess, or infer viewpoints, conditions, expected results, requirements, relationships, dates, or numbers that the source test cases do not state or directly demonstrate.
- Every viewpoint, summary, and glossary entry must be traceable to a specific source under `raw/` or to an existing wiki page. If a statement has no evidence, do not write it.
- A test viewpoint is generalized from what a test case concretely verifies. Generalizing the angle of a real test case (for example, "boundary value on the input length field") is allowed and expected. Adding a viewpoint that no source test case supports is not allowed.
- When something is unknown, missing, or ambiguous, record it explicitly under Open Questions instead of filling the gap with a plausible guess.
- Do not modify `raw/` content without explicit user instruction. Normal edits should target `wiki/`, `index.md`, and `log.md`.
- Make contradictions, possibly outdated test cases, and insufficient evidence explicit rather than silently resolving them.
- Do not leave reusable knowledge only in a one-off answer. When useful, create or update a page under `wiki/`.

## Page Placement Rules

- Create or update `wiki/testcases/<source-slug>.md` when summarizing a single source test case or test case set. Do not mix unrelated sources into the same page.
- Create or update `wiki/viewpoints/<viewpoint-slug>.md` when a viewpoint is reusable beyond the source it came from, or when multiple source test cases share the same testing angle.
- Create or update `wiki/glossary/<term-slug>.md` when you learn a product-specific term, feature name, role, state, or convention worth reusing.
- If a page could fit multiple folders, choose by purpose: a record of what a source tests goes to `testcases`, a reusable testing angle goes to `viewpoints`, and a term definition goes to `glossary`.
- Keep filenames short, lowercase, hyphen-separated, and stable. Rename only when the current name is misleading.

## Operations

- `/convert`: Convert files in `.temp/` to Markdown with `markitdown` and place them in `raw/`.
- `/ingest`: Read source test cases in `raw/`, summarize them into `wiki/testcases/`, extract reusable test viewpoints into `wiki/viewpoints/`, and record product-specific terms into `wiki/glossary/`.
- `/query`: Answer from `index.md` and related pages to support future test design or test strategy, then reflect durable findings back into the wiki.
- `/lint`: Check contradictions, orphan pages, missing index entries, unsupported (speculative) content, and missed updates.
