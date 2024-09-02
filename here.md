research-crew/
├── Makefile
├── README.md
├── Research Agent Workflow Design.md
├── here.md
├── poetry.lock
├── pyproject.toml
├── reportgen_conda_env.yml
├── roadmap.md
├── run.py
├── .devcontainer/
│   ├── Dockerfile
│   ├── devcontainer.json
├── .vscode/
│   ├── settings.json
├── config/
│   ├── .secrets.example.toml
│   ├── .secrets.toml
│   ├── settings.toml
├── docs/
│   ├── agent_graph-detailed.png
│   ├── agent_graph.png
│   ├── architecture.md
├── notebooks/
│   ├── agent_graph-detailed.png
│   ├── agent_graph.png
│   ├── test-root-graph.ipynb
├── reportgen_agent/
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── executor.py
│   │   ├── graph/
│   │   │   ├── __init__.py
│   │   │   ├── content_anaysis_graph.py
│   │   │   ├── pre_report_summarization_graph.py
│   │   │   ├── root_graph.py
│   │   ├── state/
│   │   │   ├── __init__.py
│   │   │   ├── other_states.py
│   │   │   ├── root_state.py
│   ├── nodes/
│   │   ├── __init__.py
│   │   ├── content_analysis.py
│   │   ├── content_retrieval.py
│   │   ├── final_review.py
│   │   ├── output_refinement.py
│   │   ├── query_processing.py
│   │   ├── report_generation.py
│   │   ├── source_citation.py
│   │   ├── web_search.py
│   │   ├── subnodes/
│   │   │   ├── __init__.py
│   │   │   ├── collapse_summaries.py
│   │   │   ├── collect_summaries.py
│   │   │   ├── generate_final_summary.py
│   │   │   ├── generate_summary.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── helper_functions.py
│   │   ├── storage_utils.py
│   │   ├── web_fetcher.py
├── scripts/
│   ├── get_folder_structure.py
├── tests/
│   ├── __init__.py
│   ├── test_content_retrieval.py
│   ├── test_query_processing.py
│   ├── test_report_generation.py
│   ├── test_web_search.py