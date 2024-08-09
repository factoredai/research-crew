# ReportGen Agent

## Overview

**ReportGen Agent** is a modular and extensible workflow designed to generate structured reports from web-based and user-provided content. The workflow is built using the LangGraph framework, which facilitates the creation of stateful, multi-actor applications powered by large language models (LLMs).

The main features of the ReportGen Agent include:
- **Query Processing**: Parse and enhance input queries.
- **Web Search**: Perform targeted web searches and gather relevant data.
- **Content Retrieval and Parsing**: Extract and parse content from various sources.
- **Information Filtering**: Filter and rank information based on relevance.
- **Content Analysis**: Summarize and analyze the gathered data.
- **Report Generation**: Generate structured Markdown reports with citations and cross-references.
- **Output Refinement**: Refine and polish the final output.
- **Final Review**: Perform quality checks and ensure the output meets the required standards.

## Project Structure

The project follows a clear and modular structure, adhering to the SOLID principles:

```plaintext
reportgen_agent/
│
├── reportgen_agent/            # Main source code directory
│   ├── config/                 # Configuration files
│   ├── core/                   # Core components like graph definition and state management
│   ├── nodes/                  # Individual nodes for each step of the workflow
│   └── utils/                  # Utility functions
│
├── tests/                      # Unit and integration tests
└── README.md                   # Project overview and instructions
```

## Setup Instructions

### 1. Configure Your Environment

Before running the project, you need to set up your configuration files.

#### Configuration Files

1. **Copy the example secrets file:**

   ```bash
   cp config/.secrets.example.toml config/.secrets.toml
   ```

2. **Edit `.secrets.toml` with your actual API keys and sensitive information:**

   Open `config/.secrets.toml` in your preferred text editor and replace the placeholder values with your actual credentials:

   ```toml
   [default]
   SEARCH_API_KEY = "your-real-search-api-key"
   LLM_API_KEY = "your-real-llm-api-key"
   ```

3. **General Configuration:**

   The general configuration is managed in `config/settings.toml`. This file contains non-sensitive configurations like logging levels, directory paths, etc.

### 2. Install dependencies

To set up the project, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/reportgen_agent.git
    cd reportgen_agent
    ```

2. **Install dependencies**:
    Make sure you have Python 3.8+ installed. You can create a virtual environment and install the required packages:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3. **Configure settings**:
    Update the `settings.py` file in the `reportgen_agent/config` directory with your API keys and other configuration details.

## Usage

To run the ReportGen Agent, execute the main script:

```bash
python run.py
```

The main script initializes the workflow and processes an example query. You can modify the query and other settings within the script or pass them as arguments.

## Running Tests

To run the tests, use:

```bash
pytest tests/
```

This will execute all unit and integration tests to ensure that each component of the workflow functions as expected.

## Contributing

Contributions are welcome! If you would like to contribute to the project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
