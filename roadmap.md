# Roadmap

#### **Phase 1: MVP Implementation**

1. **Integration**
   - **Task**: Integrate the above components into the graph.
   - **Details**: 
     - Connect the nodes with edges and test the entire graph workflow to ensure it works as expected.

#### **Phase 2: Post-MVP Enhancements**
reportgen_agent/core/executor.py is not being used!!!

1. **Step 1: Query Processing**
   - **Task**: Implement the `process_query` function.
   - **Purpose**: Parse the input query, extract keywords, and expand concepts.
   - **Details**: 
     - Input: Raw query string.
     - Output: Updated state with keywords and expanded concepts.

1. **Step 2: Web Search**
   - **Task**: Implement the `perform_web_search_node` function.
   - **Purpose**: Perform web searches using the extracted keywords and concepts.
   - **Details**: 
     - Input: Keywords and expanded concepts.
     - Output: A list of search results (URLs and snippets).

1. **Step 4: Content Analysis**
   - **Task**: Implement the `analyze_content` function.
   - **Purpose**: Analyze and summarize the retrieved content.
   - **Details**: 
     - Input: Retrieved content.
     - Output: Summarized and analyzed information.
   1. **Step 6: Information Filtering**
      - **Task**: Implement the `filter_information` function.
      - **Purpose**: Filter the retrieved content to prioritize high-quality and relevant information.
      - **Details**: 
        - Input: Retrieved content.
        - Output: Filtered content.
   1. **Fact Extraction and Verification**
     - **Task**: Extract key facts from the content and optionally verify them against a known dataset or external API.
     - **Approach**: Use information retrieval techniques to pull out facts and statements, then cross-reference them with authoritative sources. This is useful for ensuring the accuracy of the information in your reports.
   2. **Contextual Analysis**
      - **Task**: Understand the broader context of the content, including any implied meanings, assumptions, or underlying narratives.
      - **Approach**: Analyze the content to detect nuances, underlying arguments, or perspectives that are not immediately apparent. This could involve deeper LLM-based analysis that looks at context beyond the explicit text.
   3. **Comparative Analysis**
      - **Task**: Compare different pieces of content or sources to identify similarities, differences, and unique insights.
      - **Approach**: Analyze and contrast multiple documents to find consensus or conflicting information. This could be useful for producing a balanced report that considers multiple perspectives.
    4. **Quality Assessment**
      - **Task**: Assess the quality, credibility, and relevance of the content.
      - **Approach**: Evaluate the source and content quality based on predefined criteria such as source authority, writing quality, and relevance to the query. This helps in filtering out low-quality or irrelevant information.

1. **Content Structuring for Reports**
   - **Task**: Organize the analyzed content in a way that it can be effectively used in report generation.
   - **Approach**: Structure the content based on themes, topics, or relevance so that the report generation node can use it directly. This might involve creating outlines, bullet points, or section headers that guide the report structure.

2. **Step 7: Source Citation**
   - **Task**: Implement the `add_citations` function.
   - **Purpose**: Add citations and references to the generated report.
   - **Details**: 
     - Input: Analyzed content and sources.
     - Output: Updated report with citations.

3. **Step 8: Output Refinement**
   - **Task**: Implement the `refine_output` function.
   - **Purpose**: Refine the language and format of the generated report for better readability.
   - **Details**: 
     - Input: Generated report.
     - Output: Refined report with improved clarity and structure.

4. **Step 9: Final Review**
   - **Task**: Implement the `review_final_output` function.
   - **Purpose**: Perform a final check to ensure the report is complete and accurate.
   - **Details**: 
     - Input: Final report.
     - Output: Reviewed and finalized report, ready for delivery.

5. **Testing and Validation**
   - **Task**: Thoroughly test each new component individually and within the entire graph.
   - **Details**: 
     - Validate the correctness and completeness of each node.

#### **Phase 3: Future Enhancements**

1. **Step 11: Advanced Analysis Techniques**
   - **Task**: Implement more sophisticated content analysis techniques, such as sentiment analysis or trend detection.

1. **Step 12: Performance Optimization**
   - **Task**: Optimize the workflow for faster execution, possibly by parallelizing certain tasks.
