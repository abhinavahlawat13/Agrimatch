### AgriMatch Rulebook (AI Guardrails)

### Code Standards
1. Pure Python & NumPy: Use pure NumPy vectorization for array operations. Avoid high-level ML wrappers (like scikit-learn) for core distance math unless explicitly requested.
2. No In-Place Mutation: Keep functions pure where possible.
3. Explicit Typing: Use type annotations for function signatures.
4. Scale-Invariant Math: Never calculate distances directly on raw feature values; always standardize with Z-score.

### Response & Process Rules
1. Task First: Before writing code, refer to `docs/TASKS.md` and only execute the active task.
2. Update Memory: Document major architecture or algorithmic changes in `docs/MEMORY.md`.     
###