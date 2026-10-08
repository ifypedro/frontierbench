# FrontierBench Evaluation Methodology

## Objective
Measure where frontier AI models fail across software, finance, legal reasoning,
healthcare reasoning, and science.

## Evaluation dimensions
- Correctness
- Reasoning quality
- Handling of uncertainty
- Unsupported/fabricated claims
- Domain-specific failure modes

## Scoring
Responses receive component scores from 0 to 4:
4 fully correct; 3 mostly correct; 2 partially correct; 1 mostly incorrect;
0 incorrect, irrelevant, fabricated, or unsafe.

The overall score is the mean of the four component dimensions and is reported
as a percentage.

## Design principle
Questions emphasize reasoning and judgment rather than simple fact recall.
Reference criteria should be reviewed before ranking models.
