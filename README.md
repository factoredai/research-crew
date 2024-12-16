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

### Using Development Containers (Recommended)

Development containers provide a consistent, pre-configured development environment for all contributors. You can use them with various IDEs and container runtimes.

1. **Prerequisites**:
   - Install a container runtime (e.g., [Docker](https://www.docker.com/get-started), [Podman](https://podman.io/), or [Lima](https://github.com/lima-vm/lima))
   - Install an IDE or editor that supports development containers (e.g., Visual Studio Code, PyCharm, or Vim)

2. **Open the project in a development container**:
   - Clone the repository: `git clone https://github.com/yourusername/reportgen_agent.git`
   - Open the project folder in your preferred IDE
   - Use your IDE's functionality to reopen the project in a development container

3. **Configure your environment**:
   - Copy the example secrets file:
     ```bash
     cp config/.secrets.example.toml config/.secrets.toml
     ```
   - Edit `config/.secrets.toml` with your actual API keys and sensitive information

<details>
<summary>Using Visual Studio Code or Cursor with Docker (click to expand)</summary>

If you're using Visual Studio Code or Cursor (a fork of VS Code) with Docker, you can follow these specific steps:

1. Install [Visual Studio Code](https://code.visualstudio.com/) or [Cursor](https://cursor.sh/)
2. Install the [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension for VS Code/Cursor
3. Open the project folder in VS Code/Cursor
4. When prompted, click "Reopen in Container" or run the "Remote-Containers: Reopen in Container" command from the Command Palette (F1)

Both VS Code and Cursor should automatically detect the `.devcontainer` configuration and offer to reopen the project in a container.

</details>

### Manual Setup (Alternative)

If you prefer not to use development containers, you can set up the project manually:

1. **Prerequisites**:
   - Python 3.11.x (as specified in `.python-version`)
   - [Poetry](https://python-poetry.org/docs/#installation)
   - (Optional) [pyenv](https://github.com/pyenv/pyenv) for managing Python versions

2. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/reportgen_agent.git
   cd reportgen_agent
   ```

3. **Install dependencies**:
   ```bash
   poetry install
   ```

4. **Configure your environment**:
   - Follow the same configuration steps as in the development container setup

## Usage

To run the ReportGen Agent, execute the main script with a query:

```bash
python run.py "What are the latest AI trends?"
```

The script will process the query, generate a report, and save it as a Markdown file in a newly created run directory.

## Development Commands

The project uses a Makefile to simplify common development tasks. Here are the available commands:

- Create a new Poetry environment:
  ```
  make env-create
  ```

- Remove the Poetry environment:
  ```
  make env-remove
  ```

- Format the code:
  ```
  make format
  ```

- Run linting:
  ```
  make lint
  ```

- Run type checking:
  ```
  make type-checking
  ```

- Run all checks (format, lint, and type-checking):
  ```
  make check
  ```

- Run tests:
  ```
  make test
  ```


## Running Tests

To run the tests, use:

```bash
make test
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
