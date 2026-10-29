---
tags: [fde]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

We're leaving a defence-sector client in two weeks. We deployed a document-search agent: Llama-based model on vLLM, a Qdrant vector store, and a nightly ingest job, all inside an air-gapped enclave. Model updates come in on signed media once a quarter. Their ops team are not ML people. Write the handoff runbook their on-call will actually use.
