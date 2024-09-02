# ReportGen Agent Workflow Design

## 1. Query Processing
- Parse the input query
- Identify key topics and concepts
- If references are provided, the agent should extract and categorize these references (e.g., links, PDFs, etc.) for later use.
- Query Enhancement:
  - Keyword Extraction: Identify the most important technical keywords from the research question (e.g., "Python," "pipelines," "quantitative finance").
  - Concept Expansion:  Use an LLM to potentially expand the query with related terms or synonyms (e.g., "data pipelines," "algorithmic trading," "financial modeling"). This can help in retrieving more comprehensive information.

## 2. Web Search
- Perform web searches using search APIs (e.g., Google Custom Search, Bing Web Search)
- Collect search results (titles, snippets, URLs)

## 3. Content Retrieval and Parsing
- Fetch full content from top search results
- Parse HTML/PDF content to extract relevant text
- If user-provided references exist, parse and extract their content

## 4. Information Filtering and Relevance Ranking
- Use LLM to assess relevance of each piece of information
-   Result Filtering:  Implement intelligent filtering to prioritize:
    - Results from reputable sources (e.g., official documentation, technical blogs, academic papers).
    - Pages that are highly relevant to the technical keywords and concepts.
    - User provided references are high ranked by default
- Filter out irrelevant or low-quality content
- Rank remaining information by relevance and credibility

## 5. Content Analysis
- Use LLM to analyze the filtered information
- Text Summarization: Use the LLM's text summarization capabilities to condense the retrieved information into concise summaries for each relevant source.
- Identify key points, trends, and insights
- Compare and contrast different sources and viewpoints

## 6. Synthesis and Report Generation
- Synthesize analyzed information into a coherent narrative
- Structured Output: Convert the aggregated and analyzed content into a structured Markdown document. Consider having sections like:
  1. Introduction: Brief overview of the research question.
  2. Findings: Detailed analysis, organized by themes or categories.
  3. Comparison: If multiple tools or approaches are discussed, provide a comparison table or summary.
  4. Conclusion: Summarize the key takeaways.
  5. References: List all the sources used.
- Generate the final analysis in Markdown format

## 7. Source Citation and Fact-Checking
- Include citations for all sources used in the analysis
- Use LLM to cross-reference facts across multiple sources
- Flag any inconsistencies or potential inaccuracies

## 8. Output Refinement
- Use LLM to refine the language and improve clarity
- Review and refine the generated report to ensure accuracy, completeness, and readability.
- Ensure the output adheres to technical writing standards
- Format the Markdown for readability and proper structure

## 9. Final Review
- Perform a final check for relevance to the original query
- Ensure all parts of the question are addressed
- Verify that the output meets the defined purpose of the agent
- Quality Check: Implement a step where the agent reviews the generated Markdown document for completeness and coherence.
- (Optional) User Feedback:  Allow users to provide feedback on the generated report. 


## 10. Delivery
- Present the final Markdown output to the user
- Provide options for further refinement or additional queries if needed