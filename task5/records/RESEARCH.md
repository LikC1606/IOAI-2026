# Research

## Questions

- Is hybrid human/machine text best treated as independent sentence classification or constrained sequence labeling?
- Which local style/context features transfer without an external language model?
- Does the provided embedding encoder add signal over supervised competition-only lexical features within the 600-second deployment budget?

The fixed `ds-skills` catalog was searched for change-point, machine-generated text, authorship, stylometry, boundary, and sentence terms. It contained only generic sentence-transformer and time-series boundary entries, with no task-matched recipe. No `reference/precompetition` directory exists in this project.

## Sources And Mechanisms

### SeqXGPT (Wang et al., EMNLP 2023)

URL: https://aclanthology.org/2023.emnlp-main.73/

Context/intervention: primary paper introducing sentence-level AI-generated text detection on hybrid documents and using a sequence model over per-sentence features. The reported mechanism is that neighboring sentence evidence and sequence structure matter when documents mix human and generated text. Applicability: directly supports the competition-specific framing as sentence-origin sequence labeling, but its white-box generator probability features are unavailable and therefore not used. Legal/resource risk: none for the abstract method; external data and models from the paper are prohibited. Cheapest disproof here: compare competition-only independent sentence predictions with the one-switch cumulative likelihood objective on official dev.

### SenDetEX (Jiang et al., EMNLP 2025)

URL: https://aclanthology.org/2025.emnlp-main.268/

Context/intervention: primary paper on sentence-level detection in hybrid human/AI content; it explicitly fuses intrinsic sentence style with surrounding context and reports gains over context-free baselines. Applicability: supports testing both local lexical style and document context. Legal/resource risk: the paper's benchmark/models cannot be imported; only the method hypothesis is relevant. Expected headroom: fewer isolated false sentence labels and a more stable unique boundary. Cheapest disproof: ablate sequence aggregation and local/context feature families on disjoint dev halves.

### GL-CLiC (Adi et al., IJCNLP-AACL 2025)

URL: https://aclanthology.org/2025.ijcnlp-long.188/

Context/intervention: primary paper combining global/local coherence and lexical complexity for sentence-level generated-text detection. Applicability: motivates comparing a competition-trained lexical sentence classifier with frozen bge local/coherence embeddings. Legal/resource risk: CEFR/external linguistic resources are not permitted and will not be used. Cheapest disproof: frozen-bge and lexical sequence routes evaluated under the same structural candidate set and official dev metric.

### Fine-Grained Detection Using Sentence-Level Segmentation (Sai Teja et al., IJCNLP-AACL Findings 2025)

URL: https://aclanthology.org/2025.findings-ijcnlp.48/

Context/intervention: primary paper frames fine-grained mixed human/AI detection as sentence-level sequence labeling and uses structured decoding. Applicability: its core framing matches the observed exact sentence-start targets. Legal/resource risk: its external pretrained models/data are prohibited, so no artifact is used. Cheapest disproof: candidate recall plus official dev change-point score using only provided labels and allowed representations.

## Current Mapping

The research sources converge on sentence-level context/sequence modeling, and local forensics independently show 100% sentence-start candidate recall on both train and dev. Executable screens take precedence over further broad searching: the active distinct routes are competition-only lexical sequence likelihood, frozen-bge embedding change-point modeling, and structural/local classical seam ranking.

No external source supplies candidate data, labels, predictions, embeddings, model weights, or features. All executable evidence is produced solely from the official competition bundle.
