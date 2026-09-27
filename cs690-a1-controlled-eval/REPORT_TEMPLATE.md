# CS 690 Assignment 1 Report: Replicating a Controlled Evaluation

Name: Abraham Eapen

Repo Link: https://github.com/AbrahamEapen/CS690_Assignment1

Results SHA: 8c5031b

## Part 1. Verification evidence

Command:

```text
python -m harness.verify
```
Paste the five `OK` lines here. Keep `results/verification.json` in your repository.

OK: loaded 20 frozen tasks

OK: dataset sha256 5d84176547cb679f4145676d1f4dfd5061bf3b9600904911da8e5700e82eee3b

OK: generated Python executed in Docker sandbox

OK: candidate network probe was blocked

OK: model/configuration metadata written to results/verification.json

## Part 2. Tests and code questions

Paste the final summary line of `pytest -q` here.

20 passed in 1.71s

Answer each question in your own words, in about 75 to 150 words. Base every answer on the code in this repository, and name the files and functions you describe.

### Q1. The path of one attempt

One attempt means one task, run once, for one model. First, load_tasks in tasks.py loads the 20 fixed problems and checks they haven't changed. Then runner.py builds the prompt by inserting the task's description into a fixed template, and saves it under prompts/. provider.py's OpenAIProvider.generate sends that prompt to the model and gets back the answer text, along with which model version replied and how many tokens were used. extract_python in grader.py pulls the plain code out of the answer, in case it's wrapped in Markdown. That code is then run against the task's tests inside a locked-down Docker container (sandbox.py), which reports pass or fail. Finally, runner.py saves everything — the answer, the verdict, and all the metadata — as one line in raw_results.jsonl

### Q2. What is sent and what comes back

Provider.py's OpenAIProvider.generate sends the request. It includes which model to use, the full prompt text as input, a cap of 800 tokens on the answer's length, and temperature=1.0 so the model isn't fully deterministic. It also sends reasoning effort: none, meaning the model skips any hidden reasoning step. top_p and seed are left out entirely, since both are set to null in conditions.json. What comes back is packed into a Generation object: text is the actual answer, returned_model is the specific version string the API says actually replied (which can be more detailed than the name requested), input_tokens/output_tokens say how much was used, and stop_reason says whether the answer finished normally or got cut off for hitting the token limit.

### Q3. Same prompt, different answers

Every sample for a task uses the exact same prompt — runner.py builds it once per task and reuses it for all 3 samples. So any difference between samples comes from the model itself, not the input. In conditions.json, temperature is set to 1.0 and seed is null; provider.py sends both settings to the API unchanged. Temperature controls how much randomness the model uses when picking each next word: at 1.0, it doesn't always pick the most likely word, it picks randomly among likely ones. With no seed, that randomness isn't repeatable, so identical prompts can produce different code. 

### Q4. pass@k by hand

Show your work for pass@1 and pass@2 with n = 3 and c = 1, the values `pass_at_k` returned, and the shortcut `1 - (1 - c/n) ** k` for k = 2.

With n = 3 attempts and c = 1 correct:
1. pass@1 = c/n = 1/3 ≈ 0.333 
   pass_at_k(3, 1, 1) = 1 − C(2,1)/C(3,1) = 1 − 2/3 = 1/3.
   --> matches

2. pass@2 = 1 − 1/3 = 2/3 ≈ 0.667, matching 
   pass_at_k(3, 1, 2) = 0.667
   --> matches

3. The shortcut: 
    1 − (1 − c/n)^2 = 1 − (2/3)² = 5/9 ≈ 0.556 

### Q5. Why whole problems are redrawn

The 3 attempts on the same task are dependent as they all come from the same problem, so if a task is easy, most of its attempts pass together, and if it's hard, most fail together. The confidence interval  of one task done 3 times is correlated to measure the similarity of the task, and therefore if the task fails, the problem has to be redrawn. If the confidence interval of the 3 attempts are done independent of each other, it shower high confidence, however would represent a false positive of real problem. 

## Part 3. Replication

Part 3 has no written section. Its evidence is the committed `results/experiment/` and `prompts/` folders, and the dollars you spent, which go in the Part 4 table.

## Part 4. Results

Take every number from `results/experiment/summary_A.json` and `results/experiment/summary_B.json`, not from the console. Dollars spent come from the Usage page of your OpenAI account. If your account does not show them, write `not available`. If it shows only one total for the whole run, write the total in row A and `included in A` in row B.

| Condition | Requested model | Returned model version | Attempts per task | Total attempts | pass@1 | 95 percent CI for pass@1 | pass@2 | Input tokens | Output tokens | Dollars spent |
| --- | --- | --- | ---: | ---: | ---: | --- | ---: | ---: | ---: | --- |
| A | gpt-5.6-luna | gpt-5.6-luna | 3 | 60 | 0.9667 | [0.90, 1.00] | 0.9833 | 7146 | 3814 | $0.07 |
| B | gpt-5.6-terra | gpt-5.6-terra | 3 | 60 | 1.0000 | [1.00, 1.00] | 1.0000 | 7146 | 4323 | included in A |

### Memo, no more than 500 words, not counting the table

Address all five items:

1. State the observed ranking by pass@1 point estimate.
   
        B (gpt-5.6-terra, 1.0) ranks above A (gpt-5.6-luna, 0.9667).

2. State whether the uncertainty evidence supports ranking the two conditions.
   
        No, the intervals do not cleanly seperate, as they overlap at 1.00.
        A's CI is [0.90, 1.00] and B's is [1.00, 1.00]
        The evidence does not support a ranking.

3. If it does not, include the exact sentence: `The evidence does not support a ranking.`
   
        The evidence does not support a ranking.

4. State one external-validity limitation specific to `CS690-Eval20`.
   
        
        
        One limitation is that evaluation is contained to 20 functions. Evaluation will not show how models compare to larger codebases or real world datasets.

5. State one likely source of variance specific to this experiment, and explain why a rerun, or a classmate's run, gives somewhat different numbers.

        The model is set to temperature=1.0 with no fixed seed so each attempt picks its next word randomly instead of always picking the same one. That means even the exact same prompt can produce a different answer each time it's run. If someone reran this experiment, or a classmate ran it with the same setup, some of these close-call tasks could easily flip from pass to fail or fail to pass, especially for condition A, which isn't sitting at a perfect score.

Overlapping intervals are not a formal significance test, and you are not asked to run one.

## Part 5. Reading a published score, 300 to 400 words

Benchmark chosen (HumanEval, MBPP, LiveCodeBench, or SWE-bench):

Use the benchmark's primary paper or its official documentation for the task definition. Cite evidence for any contamination, saturation, or current-status claim, and date any current-status source.

### 1. What does it measure?

HumanEval measures functional correctness on 164 hand-written, standalone Python programming problems (Chen et al., 2021, "Evaluating Large Language Models Trained on Code," arXiv:2107.03374). Each problem gives a function signature and docstring; the model completes the function body, and correctness is judged by hidden unit tests, scored with pass@k over independently sampled completions — the same pass@k estimator your harness implements.

### 2. What does it not measure that a software project may depend on?

Every problem is a single, self-contained function with no existing codebase, no external dependencies, and no ambiguity in the spec. It says nothing about a model's ability to navigate or modify a large existing repository, use unfamiliar libraries correctly, resolve conflicting or underspecified requirements, review or refactor someone else's code, or collaborate across multiple files and commits — all things real software work depends on daily.

### 3. How can a reported score rise without the underlying model becoming better?

A score can rise from training-data contamination rather than genuine improvement: a 2024 study found every HumanEval prompt appears at least 43 times on public GitHub, with a median of 99 occurrences, often as near-exact copies of the dataset itself (Matton et al., "On Leakage of Code Generation Evaluation Datasets," arXiv:2407.07565, EMNLP Findings 2024). A model trained on a fresh GitHub crawl can memorize solutions without any real coding-capability gain. Scores can also rise from more samples per problem, better answer-extraction scaffolding, or benchmark-specific fine-tuning.

### 4. Could the model have seen the answers already?

Very plausibly yes. Given that same leakage study's finding — a median of 99 public copies per prompt — any model trained on a broad web/GitHub crawl has a realistic chance of having encountered HumanEval's exact problems and solutions during pretraining, not just problems similar to them. As of 2026, industry write-ups note HumanEval scores have saturated near 95–98% among frontier models and the benchmark has largely moved to appendix tables rather than headline comparisons (e.g., futureagi.com, "HumanEval Benchmark Explained," 2026), consistent with contamination and ceiling effects rather than continued genuine progress.

End with at least one sentence explaining why the published score is not interchangeable with your `CS690-Eval20` result.

Published HumanEval scores are not interchangeable with the CS690-Eval20 result because CS690-Eval20's result reflects one specific frozen prompt template and sampling configuration rather than a widely-reported, potentially contamination-inflated number.

## References

Chen, M., et al. (2021). Evaluating Large Language Models Trained on Code. arXiv:2107.03374.


Matton, A., et al. (2024). On Leakage of Code Generation Evaluation Datasets. EMNLP Findings 2024 / arXiv:2407.07565.