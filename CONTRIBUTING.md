# Contributing to ReportGen Agent

We welcome contributions to the ReportGen Agent project! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository on GitHub.
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/reportgen_agent.git
   cd reportgen_agent
   ```

3. Set up your development environment:
   - We recommend using DevContainer for a consistent development environment. See the README.md for instructions.
   - If you prefer manual setup, make sure you have Python 3.11+ and Poetry installed.

4. Install the project dependencies:
   ```bash
   poetry install
   ```

5. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Workflow

1. Make your changes in the new branch.
2. Write or update tests for your changes.
3. Run the tests to ensure they pass:
   ```bash
   make test
   ```

4. Format your code, run linting, and type checking:
   ```bash
   make check
   ```

5. Commit your changes:
   ```bash
   git commit -am "Add some feature"
   ```

6. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

7. Create a pull request from your fork to the main repository.


## Pull Request Guidelines

- Ensure your code passes all checks (format, lint, type-checking). You can run all checks with:
  ```bash
  make check
  ```
- Include tests for new features or bug fixes.
- Update the documentation if necessary.
- Describe your changes in the pull request description.


## Code of Conduct

Please note that this project is released with a Contributor Code of Conduct. By participating in this project you agree to abide by its terms.

## Questions?

If you have any questions, please open an issue or reach out to the maintainers.

Thank you for contributing to ReportGen Agent!