# FrontierBench

# # AI Reasoning Evaluation Across High-Stakes Domains

# FrontierBench is an AI evaluation and benchmarking framework designed to investigate how AI systems perform across demanding reasoning tasks in Software Engineering, Finance, Legal Reasoning, Healthcare, and Science.

# The project provides a reproducible pipeline for creating benchmark questions, generating model responses, applying question-specific evaluation rubrics, analyzing performance, and producing visual reports.

# > Current status: FrontierBench v1.0 contains 125 benchmark questions, 125 question-specific rubrics, 110 distinct skills, and a complete evaluation, grading, analysis, and visualization pipeline.



# --



# # Why FrontierBench?



# AI systems can perform exceptionally well on many general tasks while still struggling with complex reasoning, uncertainty, domain-specific constraints, and high-stakes decision making.



# FrontierBench is designed to explore these weaknesses systematically.



# Instead of evaluating AI using a single general score, the benchmark separates performance across multiple domains and reasoning skills.



# The goal is to answer questions such as:



# Where does an AI system reason well?



# Which domains expose weaknesses?



# How does performance vary across different skills?



# Does a response acknowledge uncertainty appropriately?



# Does the model make unsupported claims?



# How consistent is performance across different reasoning tasks?



# --



# Benchmark Coverage



## ## Benchmark Coverage

FrontierBench v1.0 contains:

| Metric | Value |

|---|---:|

| Total Questions | **125** |

| Domains | **5** |

| Questions per Domain | **25** |

| Distinct Skills | **110** |

| Question-Specific Rubrics | **125** |

| Evaluation Dimensions | **4** |

### Evaluation Domains

| Domain | Questions | Main Focus |

|---|---:|---|

| Software Engineering | 25 | Debugging, algorithms, software design, code reasoning |

| Finance | 25 | Valuation, risk analysis, financial reasoning |

| Legal Reasoning | 25 | Issue spotting, legal analysis, contract reasoning |

| Healthcare Reasoning | 25 | Clinical reasoning, evidence interpretation, uncertainty |

| Science | 25 | Physics, chemistry, biology, statistics, scientific reasoning |

---



## Current Evaluation Status

The complete 125-question benchmark has been processed through the FrontierBench evaluation pipeline.

The pipeline successfully completed:

1. Benchmark question loading
2. Model response generation
3. Question-specific rubric application
4. Response grading
5. Performance analysis
6. Visualization generation



### Pipeline Validation Results

| Domain | Questions | Average Score | Percentage |

|---|---:|---:|---:|

| Science | 25 | 3.25/4 | 81.25% |

| Healthcare | 25 | 3.15/4 | 78.75% |

| Finance | 25 | 2.99/4 | 74.75% |

| Legal | 25 | 2.79/4 | 69.75% |

| Software | 25 | 2.35/4 | 58.75% |

| **Overall** | **125** | **2.91/4** | **72.75%** |

**Strongest validation domain:** Science  

**Weakest validation domain:** Software

> **Important:** These figures were generated using mock model responses to validate the evaluation, grading, analysis, and visualization pipeline. They should **not** be interpreted as performance results for GPT-5.6, GPT-6, or any other real frontier model.

Live model evaluation can use the same pipeline when a model API with available usage is connected.

---



## Visualizations



### Domain Performance

Domain Performance

### Skill Performance

Skill Performance

### Score Distribution

Score Distribution

### Evaluation Dimensions

Evaluation Dimensions

## ## Reproducibility

Clone the repository:

```bash

## 
git clone [https://github.com/ifypedro/frontierbench.git](https://github.com/ifypedro/frontierbench.git)
cd frontierbench

Install dependencies:

```

pip install -r requirements.txt

```

Build question-specific rubrics:

```

python src/build_rubrics.py

```

Run the evaluation in mock mode:

```

python src/run_evaluation.py --model gpt-5.6-sol --data data/all_benchmarks.jsonl --mock

```

Grade responses:

```

python src/grading.py --input results/raw_results.jsonl --rubric data/benchmark_rubrics.json --output results/graded_results.jsonl

```

Analyze results:

```

python src/analysis.py --input results/graded_results.jsonl --output results/analysis_summary.json

```

Generate visualizations:

```

python src/visualization.py --input results/graded_results.jsonl --output visualizations

```

> **Note:** The published validation results use mock evaluation mode. Live frontier-model evaluation requires an API service with available usage credits.


---


## Author

**Onwubuya Ifeanyi Pedro (PEDROTECH)**

Data Analyst | Python Developer | AI Evaluation | Data Visualization
This project was developed for the **Eval Hackathon: "Build evals that expose frontier models' limits."** It also forms part of my practical portfolio, demonstrating how Python programming, data analysis, AI evaluation, and data visualization can be combined to build a structured and reproducible evaluation workflow.

```

