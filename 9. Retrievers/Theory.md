# LangChain Retrievers --- Short Notes

## 1. What Is a Retriever?

A **retriever** is a LangChain component that fetches relevant documents
from a data source in response to a user's query.

-   Input: a query (usually text).
-   Output: relevant LangChain `Document` objects.
-   All LangChain retrievers are **Runnables**, so they can be used in
    pipelines.
-   Retrievers can search vector stores, web sources, Wikipedia,
    databases, or other data sources.

## 2. Where a Retriever Fits in RAG

``` mermaid
flowchart TD
    A[User question] --> B[Retriever]
    C[(Document collection / Vector store)] --> B
    B --> D[Relevant document chunks]
    D --> E[LLM]
    E --> F[Answer]
```

The retriever finds context; the LLM uses that context to generate an
answer.

## Vector Database vs Retriever

### 1. Vector Database Similarity Search
A vector database stores embeddings and finds similar vectors using distance or similarity metrics such as cosine similarity, Euclidean distance, or dot product.

- **Indexing algorithms** organize vectors to make searching efficient.
- Examples: HNSW, IVF, and exact search.

### 2. Retriever
A retriever is a higher-level component that fetches relevant documents for an application or LLM.

It can:
- Configure the number of results (`top-k`).
- Apply metadata filters or score thresholds.
- Combine vector and keyword search.
- Select diverse results using MMR (Maximum Marginal Relevance).

**Why do we need a retriever?** A vector database can search vectors independently, but a retriever provides a flexible interface to control how documents are fetched and selected for a RAG pipeline.

### 3. Indexing vs Retrieval

| Indexing Algorithms | Retrieval Strategies |
|---|---|
| Organize vectors for efficient searching. | Decide which documents to return. |
| Examples: HNSW, IVF, exact search. | Examples: top-k, MMR, hybrid search. |

**Remember:** HNSW is an indexing/search algorithm, whereas MMR is a retrieval strategy. A retriever can use a vector database with HNSW and apply MMR to select the final documents.


## 3. Common Retriever Types

### A. Wikipedia Retriever

Queries the Wikipedia API for relevant information and returns it as
LangChain `Document` objects.

**Use:** Getting general information from Wikipedia.

### B. Vector Store Retriever

Searches a vector store using semantic similarity.

1.  Documents are split into chunks and embedded.
2.  The query is embedded.
3.  The query vector is compared with stored vectors.
4.  The top-`k` similar chunks are returned.

**Use:** Searching a private or indexed document collection by meaning.

### C. Maximal Marginal Relevance (MMR) Retriever

Selects documents that are both relevant to the query and different from
one another.

-   First selects a highly relevant document.
-   Then favors relevant documents that add new information instead of
    repeating selected results.
-   Helps avoid near-duplicate chunks returned by ordinary similarity
    search.

**Use:** RAG when retrieved chunks overlap or repeat the same facts.

### D. Multi-Query Retriever

Uses an LLM to generate multiple alternative versions of the original
query, retrieves documents for each version, and combines/deduplicates
the results.

``` mermaid
flowchart LR
    Q[Original query] --> L[LLM creates query variations]
    L --> Q1[Query 1]
    L --> Q2[Query 2]
    L --> Q3[Query 3]
    Q1 --> R[Retrieve for each query]
    Q2 --> R
    Q3 --> R
    R --> U[Merge and deduplicate]
    U --> D[Relevant documents]
```

**Why:** A single query may miss relevant content because documents use
different wording.

**Example:** "How can I stay healthy?" may be expanded into queries
about diet, exercise, stress, and daily habits.

### E. Contextual Compression Retriever

Uses a base retriever to fetch documents, then filters or compresses
them to retain only the parts relevant to the query.

``` mermaid
flowchart TD
    Q[User query] --> R[Base retriever]
    S[(Document store)] --> R
    R --> D[Retrieved documents]
    D --> C[Compressor / relevance filter]
    C --> K[Relevant passages only]
    K --> L[LLM generates answer]
```

**Why:** A retrieved document may contain one useful sentence surrounded
by unrelated content.

**Use:** Long documents, noisy results, or reducing the context sent to
an LLM.

## 4. MMR vs. Ordinary Similarity Search

``` mermaid
flowchart LR
    Q[Query] --> S[Similarity search]
    S --> A[Chunk A: very relevant]
    S --> B[Chunk B: almost same as A]
    S --> C[Chunk C: relevant, different detail]
    A --> M[MMR selection]
    B --> M
    C --> M
    M --> O[Relevant and diverse chunks]
```

Ordinary similarity search ranks chunks by query similarity. MMR also
considers similarity between already selected chunks, encouraging
diversity while preserving relevance.

## 5. Retriever vs. Vector Store

-   **Vector store:** Stores embeddings and performs similarity search.
-   **Retriever:** Accepts a query and returns relevant documents.
-   A vector store can be converted into a retriever, but not all
    retrievers use vector stores.

## 6. Quick Comparison

  -----------------------------------------------------------------------
  Retriever               Main idea               Best suited for
  ----------------------- ----------------------- -----------------------
  Wikipedia               Search an external      General factual
                          encyclopedia            information

  Vector store            Semantic similarity     Private or indexed
                          search                  collections

  MMR                     Relevant but diverse    Avoiding repetitive
                          results                 chunks

  Multi-query             Search several query    Different phrasings or
                          variations              aspects

  Contextual compression  Keep only relevant      Long or noisy retrieved
                          passages                content
  -----------------------------------------------------------------------

## 7. Typical LangChain Usage

``` python
# Turn a vector store into a retriever
retriever = vector_store.as_retriever(
    search_kwargs={"k": 4}
)

# Retrieve relevant documents
docs = retriever.invoke("What is semantic search?")
```

**Key point:** A retriever finds and returns relevant context; it does
not itself generate the final answer. In RAG, the retrieved documents
are passed to an LLM, which uses them to answer the question.
