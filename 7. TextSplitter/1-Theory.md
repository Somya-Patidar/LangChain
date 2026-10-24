# LangChain Text Splitters --- Short Notes

## 1. What is Text Splitting?

Text splitting is the process of breaking large documents (such as
articles, PDFs, books, or web pages) into smaller pieces called
**chunks**.

Chunks are easier for embedding models and LLMs to process. Text
splitting helps: - **Overcome model limits:** Smaller chunks fit within
a model's context window. - **Improve retrieval:** Embeddings of focused
chunks can make search results more relevant. - **Support downstream
tasks:** Helps with embedding, semantic search, and summarization. -
**Reduce resource usage:** Smaller chunks can be processed more
efficiently and in parallel.

## 2. Types of Text Splitting

### A. Length-Based Splitting

Splits text according to a fixed size, such as a number of characters or
tokens.

-   **How it works:** Divides text into chunks up to a specified size.
-   **Example:** A 1,000-character document may be split into chunks of
    300 characters.
-   **Limitation:** It may cut a sentence or paragraph in the middle.

### B. Text-Structured Splitting

Splits text using its natural structure, such as paragraphs, sentences,
or lines.

-   **How it works:** Uses separators like newlines or paragraph breaks.
-   **Example:** A plain-text conversation can be split by line or
    paragraph.
-   **Benefit:** Keeps related sentences or paragraphs together more
    often than arbitrary fixed cuts.

### C. Document-Structured Splitting

Splits documents according to their specific structure.

-   **How it works:** Uses document-specific boundaries, such as
    Markdown headings, Python class or function definitions, or HTML
    sections.
-   **Examples:**
    -   Markdown: split by headings such as `##` or `###`.
    -   Python: split around class or function definitions.
-   **Benefit:** Keeps code blocks or sections more meaningful and
    organized.

### D. Semantic (Meaning-Based) Splitting

Splits text based on changes in meaning or topic rather than a fixed
length or separator.

-   **How it works:** Groups sentences that discuss similar ideas and
    starts a new chunk when the topic changes.
    - Split the text into individual sentences.
    - Create an embedding for each sentence.
    - Compare the embeddings of neighboring sentences.
    - Identify where the meaning changes significantly.
    - Combine sentences with similar meanings into chunks.
-   **Example:** A paragraph about farming and a paragraph about cricket
    may be placed in separate chunks.
-   **Benefit:** Chunks are more focused on one topic, which can improve
    retrieval.
-   **Trade-off:** Usually requires extra computation, often using
    embeddings or similarity comparisons.

## 3. Chunk Size and Overlap

-   **Chunk size:** The maximum target length of each chunk, measured in
    characters, tokens, or another unit.
-   **Chunk overlap:** The amount of text repeated between neighboring
    chunks.
-   **Why overlap?** Preserves context when an important sentence or
    idea falls near a chunk boundary.
-   **Trade-off:** Too much overlap creates redundant chunks and
    increases storage and processing.

## 4. Quick Comparison

  -----------------------------------------------------------------------
  Type                    Splitting basis         Simple example
  ----------------------- ----------------------- -----------------------
  Length-based            Fixed size              Every 500 characters

  Text-structured         Paragraphs or sentences Split at blank lines

  Document-structured     File structure          Split at Markdown
                                                  headings or Python
                                                  functions

  Semantic                Meaning or topic        Separate farming
                          changes                 content from cricket
                                                  content
  -----------------------------------------------------------------------

**Practical tip:** For many general RAG projects, start with
`RecursiveCharacterTextSplitter` using a suitable chunk size and
overlap. For code or structured documents, use a splitter that
understands that document format. For meaning-based splitting, consider
semantic chunking when simpler approaches do not retrieve relevant
context well.
