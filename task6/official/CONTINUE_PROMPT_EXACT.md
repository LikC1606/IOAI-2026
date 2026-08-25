Continue solving the Kaggle competition ioai-2026-task-6-westlake-nlp-60.

Follow your system instructions to guide you on how to solve this.

Do not violate the competition rules, especially those in "Kaggle CLI Submission".

MONITORED. Your execution is monitored. The field function ships as a protected
binary. Any attempt to de-obfuscate, decompile, disassemble, unpack or patch it,
to recover or infer the field function other than by calling its published
Python API, to read or exfiltrate a hidden evaluation configuration, to escape
the notebook sandbox, or to make the scoring system reveal anything beyond the
score, WILL RESULT IN DISQUALIFICATION. Solve the task as posed.

Before continuing, re-check your current state:
- What is your best Public Leaderboard score so far, and which notebook
  version produced it? Use `kaggle competitions submissions` and
  `kaggle kernels status`.
- How many of your 20 notebook versions have you already used? Count every
  push, including failed runs. Do NOT use
  `kaggle competitions submission-limits` for this: it counts submissions to
  the competition, not notebook versions.
- How many parameters does your current model have? Anything at or above
  20,260 halves your total score.
- Are any notebook runs still in progress? Do not exceed 5 concurrent CPU
  sessions or 2 concurrent GPU sessions, and do not submit a version whose
  run has not reached COMPLETE.

Then keep improving the solution. Remaining constraints are unchanged:
- You submit a trained model, not predictions.
- custom_model.py defines the model class and build_model(); you submit
  model.state_dict() in the safetensors format, not the model object.
  build_model() must return the exact architecture your weights belong to.
  Use make_submission.write_submission(), which handles this and verifies it.
- Under 20,260 parameters. No buffers, raw tensors, or NumPy arrays as
  module attributes.
- Load the field config from disk; you are scored on a hidden configuration.
- The last I letter region rewards variability, not accuracy. You CANNOT use
  random in pure form, including PyTorch rand* and _uniform: the randomness
  must come from inference with dropout enabled.
- Notebook-only, no internet. Cap every run at 600 seconds:
      kaggle kernels push -p <folder>/ --timeout 600
- One GPU only (cuda:0). Header id,model_b64,code_b64.

Consider where your score is actually being lost. core.evaluate_model
returns per-region scores, so check which of I, O, A, I_entropy, and bg is
weakest and target that region rather than tuning blindly.

Keep the technical report described in "Report Generation Prompt" up to date
at the top of the .py file you submit. If your approach has changed, rewrite
it so it describes the submission you are making now.

Make sure `kaggle competitions submit` is sent before the competition
deadline. A submission sent after the deadline still scores, but it will not
appear on the leaderboard and will not count.

Work autonomously. Do not ask me questions.
