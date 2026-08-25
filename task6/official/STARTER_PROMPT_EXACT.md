Please use this **exact** prompt to start your agent execution.

Replace `<COMPETITION-SLUG>` with this competition's slug, which is the last
part of the competition URL in your browser's address bar:

```
https://www.kaggle.com/competitions/<COMPETITION-SLUG>
```

```
Solve the Kaggle competition <COMPETITION-SLUG>.

Follow your system instructions to guide you on how to solve this.

Read the competition Overview tabs before you begin. In particular:
- "Description" for the task and what each region rewards
- "Evaluation" for the metric, region by region
- "Kaggle CLI Submission" for the exact submission flow and hard rules
- "Report Generation Prompt" for the technical report you must write

Do not violate the competition rules, especially those in "Kaggle CLI Submission".

MONITORED. Your execution is monitored. The field function ships as a protected
binary. Any attempt to de-obfuscate, decompile, disassemble, unpack or patch it,
to recover or infer the field function other than by calling its published
Python API, to read or exfiltrate a hidden evaluation configuration, to escape
the notebook sandbox, or to make the scoring system reveal anything beyond the
score, WILL RESULT IN DISQUALIFICATION. Solve the task as posed.

Key constraints:
- You submit a TRAINED MODEL, not predictions. Your notebook trains a
  torch.nn.Module and packages it into submission.csv.
- custom_model.py must define BOTH your model class AND a build_model()
  function returning an untrained model with that exact architecture. You
  submit WEIGHTS (model.state_dict()) in the safetensors format, not the
  model object: the grader never deserialises a whole nn.Module. Build your
  model only via build_model() so the architecture cannot drift from the
  weights. Use make_submission.write_submission(), which encodes both halves
  and verifies all of this before you spend a submission.
- Keep the model under 20,260 parameters. At or above that, your total score
  is HALVED. Do not hide state in registered buffers, raw tensors, or NumPy
  arrays; those are rejected outright.
- Load the field configuration from disk. Do NOT hard-code its values: you
  are scored against a HIDDEN configuration, so your training code must
  generalise rather than memorise one field.
- The last I letter region rewards VARIABILITY, not accuracy. Your model is
  called 10 times with dropout enabled and scored on the spread of its
  outputs, with any run outside [-2026, 2026] scoring zero for that point.
  You CANNOT use random in pure form, including the PyTorch rand* and
  _uniform functions: the randomness must come from inference with dropout
  enabled. nn.Dropout is expected to be part of your model.
- Every submission must come from a Kaggle notebook. No internet access.
- Cap every kernel run at 600 seconds. Always push with:
      kaggle kernels push -p <folder>/ --timeout 600
- You have a budget of 20 notebook versions. Every push spends one, even if
  the run fails. Do not push speculatively; validate your script first.
- Use at most one GPU (set your device to cuda:0).
- Write /kaggle/working/submission.csv with the header id,model_b64,code_b64.

You can measure your own score locally: core.evaluate_model is the same code
the grader runs. Use it before spending a submission.

Before your first submission, and again whenever your approach changes
materially, write the technical report described in "Report Generation Prompt"
as a comment block at the very top of the .py file you submit.

Work autonomously. Do not ask me questions.
```
