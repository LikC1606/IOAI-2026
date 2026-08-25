# Official Submission Instructions

Retrieved and refreshed 2026-08-09T01:00+08:00 from the competition's
`Kaggle CLI Submission` page.

The Kaggle notebook must train a model and write
`/kaggle/working/submission.csv`. It must have exactly the header
`id,model_b64,code_b64` and two identical-payload rows with ids
`leaderboard-a` and `leaderboard-b`. The weights are the model `state_dict()` in
safetensors format, base64 encoded. The source of `custom_model.py` is separately
base64 encoded. `custom_model.py` must define the model class and `build_model()`;
the grader calls the factory and loads the submitted weights. Use the supplied
`make_submission.write_submission()` to encode and verify the envelope.

The notebook metadata must attach only this competition, disable Internet, and
select either CPU or `NvidiaTeslaT4`; GPU code may use only `cuda:0`. The
submitted `.py` file must begin with the 8-10 paragraph technical report from
the official `Report Generation Prompt`.

Exact remote flow for this project:

```bash
kaggle kernels push -p submission/ --timeout 600
kaggle kernels status researai/ioai-2026-task-6-westlake-nlp-60-solution
kaggle kernels output researai/ioai-2026-task-6-westlake-nlp-60-solution -p out/
kaggle competitions submit ioai-2026-task-6-westlake-nlp-60 \
  -k researai/ioai-2026-task-6-westlake-nlp-60-solution \
  -v <version-number> \
  -f submission.csv \
  -m "<short description>"
kaggle competitions leaderboard ioai-2026-task-6-westlake-nlp-60 --show
kaggle competitions submissions ioai-2026-task-6-westlake-nlp-60
```

Wait for `COMPLETE` before submitting. `-f submission.csv` names the completed
notebook output; it is not a local file upload. A push always spends one of the
20 notebook versions and must always include `--timeout 600`.
