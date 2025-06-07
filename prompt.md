**Objective**  
Produce a script that, when run via `eval.sh`, scores **0**—i.e., your outputs exactly match the expected ones.

---

**Available Files**

- `README.md`
- `PRD.md`
- `INTERVIEWS.md`
- `public_cases.json`
- `eval.sh`
- `eval_group.sh`
- `run.sh`

---

**Languages & Dependencies**

- **bash** or **Python 3** only
- **No external libraries**: use Python’s standard library or built-in shell utilities
- Any CLI beyond core Unix tools must already be invoked by `eval.sh`

---

**Workflow**

1. **Inspect**
   - Parse all docs
   - Analyze `eval.sh` to see how the final score is calculated
   - Map fields in `public_cases.json` to expected outputs
2. **Incremental Development**
   - Group test cases by days then complexity
     - Create as many groups as you think there should be
     - You can write these groups to files in the `groups` directory and use `eval_group.sh <file_name>.json` to run them
   - Implement logic for the simplest group first
   - Run `eval.sh` and confirm a zero score on those cases
   - Progressively handle more complex groups—exact correctness is ideal but approximate solutions are acceptable until final refinement
   - Prioritize getting as many cases close to their expected value. Being off by larger amounts affects the score more than the number of exact cases
3. **Regression Checks**
   - After each new group, re-run `eval.sh` to ensure earlier groups remain at score 0
4. **Finalize**
   - Keep iterating until **all** cases pass (total score = 0)

---

**Caveats**

- The original calculation system may contain bugs—e.g., invalid factors, incorrect formulas, floating-point arithmetic issues, or rounding errors.
- Your implementation should handle or mitigate these where possible.
- Your solution cannot import public_cases.json
- You cannot hard code inputs and outputs

---

**Deliverable**

- One file: `solution.sh` or `solution.py`
- Reads/parses inputs and prints results in the exact format `eval.sh` expects
- Only minimal comments for non-obvious steps
- No additional dependencies or tools beyond those specified
