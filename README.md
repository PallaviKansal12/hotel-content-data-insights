# Hotel Content Insights

This project builds a lightweight AI content quality monitoring workflow for hotel marketing copy. It compares AI-generated descriptions against known hotel metadata such as name, city, rating, and review count to detect factual mismatches, unsupported claims, and hallucinated content before it reaches customers. The project combines Python-based data checks with a simple interactive dashboard so the output is not only technically useful but also easy to understand for product, marketing, and operations teams.

## What this project is doing

The core idea is to evaluate generated hotel descriptions in a structured, repeatable way: the system reads hotel reference data, checks whether key facts are present in the AI text, identifies unsupported claims such as fake room counts or amenities, and classifies the content as low, medium, or high risk. It also calculates a confidence score and flags content that should require human review. This creates a practical safeguard for AI-generated marketing content, where factual accuracy and brand trust matter as much as speed and scale.

## Why this matters

AI can generate convincing marketing copy very quickly, but it can also invent details that are not supported by official hotel data. For hotel brands, even a small error in location, rating, or amenity description can create trust issues for customers and additional review work for teams. This project addresses that problem by turning content quality into an operational, measurable signal.

## Product and business angle

This project is valuable beyond just technical validation because it supports real business decisions:

- Marketing teams can see whether AI-generated descriptions are safe to publish.
- Product teams can prioritize content review workflows based on risk levels.
- Ops teams can reduce the cost of manual QA by focusing only on flagged content.
- Stakeholders can understand the quality of generated content through a clear dashboard instead of raw model output.

## How it fits the role

This is a strong fit for a Working Student – Data & Insights role because it combines data analysis, Python, AI experimentation, and practical product thinking. It demonstrates hands-on work with Python, structured data, quality evaluation, and a dashboard-oriented view that helps translate insights into clear business decisions. It also reflects the kind of curiosity and AI-aware mindset the role is looking for: using AI as an enabler while still validating output rigorously.

## SQL summary for insights work

The project also includes SQL-style analysis that mirrors how a data team would summarize the same results in a business context. It answers questions such as:

- How many generated hotel descriptions fall into each risk bucket?
- What percentage of content should be escalated for human review?
- Which unsupported claims appear most frequently?
- Which hotels are most likely to require intervention?

This makes the project more relevant for a data-focused role because it shows not only model logic, but also the ability to summarize and communicate findings in a structured way.

## Mini case study

Imagine a hotel marketing team wants to scale AI-generated content for several properties across Europe. The challenge is that AI can write fluent copy quickly, but it may invent details that do not match the actual hotel profile. This project solves that by creating a quality monitoring layer: it validates the generated description against the hotel’s official attributes and flags risky content before publication. In a real business environment, this reduces manual review effort, protects brand trust, and helps teams decide whether AI-assisted content is safe to publish or needs editing. This is a very practical example of how data insight and product thinking can improve an AI workflow.

## Run the dashboard

```bash
cd /Users/princejain/hotel-content-data-insights
source venv/bin/activate
streamlit run dashboard/streamlit_app.py
```

## Project structure

- `src/agents/content_evaluation_agent.py` — evaluation logic for comparing AI-generated content with hotel metadata
- `data/` — hotel data and evaluation output files
- `dashboard/streamlit_app.py` — business-facing dashboard for risk monitoring
- `tests/test_content_evaluation.py` — unit tests for the evaluation logic
