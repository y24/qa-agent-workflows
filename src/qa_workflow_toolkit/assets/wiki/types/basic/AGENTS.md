<!-- generated-by: qa-workflow-toolkit -->
<!-- wiki-name: [[wiki_name]] -->
<!-- wiki-type: [[wiki_type]] -->

# [[wiki_name]] LLM Wiki

This repository is a Markdown knowledge base maintained by LLM agents. Treat it as a durable working memory: every update should be traceable to evidence, easy to re-read later, and placed where future agents can find it quickly.

## Structure

- `raw/`: Converted or collected primary sources. Treat them as immutable evidence by default.
- `.temp/`: Temporary staging area for files before conversion into `raw/`.
- `wiki/`: Knowledge pages created and updated by LLM agents. New pages must go into one of the subfolders below.
- `wiki/articles/`: Source summary pages. Use one page per primary source, and keep the page focused on what that source says.
- `wiki/concepts/`: Synthesis pages. Use these for concepts, methods, domains, entities, or research areas that require evidence from more than one source.
- `wiki/queries/`: Filed answers. Use these for answers to concrete user questions when the answer should be kept for future reuse.
- `index.md`: Content index for the whole wiki. Check it first before ingest or query work.
- `log.md`: Append-only chronological log for ingest, query, lint, and convert operations.
- Agent-specific commands: Slash commands for wiki operations.

## Core Policies

- Do not invent unsupported facts, requirements, relationships, dates, or numbers. If evidence is missing, say what is missing.
- Separate facts, inferences, assumptions, unverified items, and proposals. Do not let inferred conclusions look like source facts.
- Add references to files under `raw/` or pages under `wiki/` for important statements. Prefer stable relative paths such as `raw/source-name.md` or `wiki/concepts/topic.md`.
- Do not modify `raw/` content without explicit user instruction. Normal edits should target `wiki/`, `index.md`, and `log.md`.
- Do not leave reusable knowledge only in a one-off answer. When useful, create a page under `wiki/` or integrate it into an existing page.
- Make contradictions, possibly outdated statements, insufficient evidence, and unresolved assumptions explicit.

## Page Placement Rules

- Create or update `wiki/articles/<source-slug>.md` when summarizing a single primary source. Do not mix unrelated source summaries into the same article page.
- Create or update `wiki/concepts/<concept-slug>.md` when combining evidence from multiple sources or when extracting a reusable concept, method, taxonomy, entity, or research area.
- Create or update `wiki/queries/<question-slug>.md` when preserving a question answer, especially if the answer required synthesis or will likely be asked again.
- If a page could fit multiple folders, choose by purpose: source summary goes to `articles`, reusable synthesized knowledge goes to `concepts`, and answer records go to `queries`.
- Keep filenames short, lowercase, hyphen-separated, and stable. Rename only when the current name is misleading.

## Operations

- `/convert`: Convert files in `.temp/` to Markdown with `markitdown` and place them in `raw/`.
- `/ingest`: Read sources in `raw/` and integrate summaries, entities, concepts, and relationships into `wiki/`.
- `/query`: Answer from `index.md` and related pages, then identify findings that should be reflected back into the wiki.
- `/lint`: Check contradictions, orphan pages, missing index entries, insufficient evidence, and missed updates.
