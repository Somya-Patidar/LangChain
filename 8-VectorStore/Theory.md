# Vector Stores --- Short Notes

## 1. Why Do We Need Vector Stores?

In RAG, documents are split into chunks and converted into
**embeddings** (numerical vectors that represent their meaning). When a
user asks a question, the question is also embedded. We need a way to
store the document vectors and quickly find the ones most similar to the
question vector.

A vector store provides this functionality. Instead of searching only
for exact words, it can retrieve text whose meaning is similar to the
query.

**Typical RAG flow:**

1.  Load documents and split them into chunks.
2.  Convert each chunk into an embedding.
3.  Store the embedding, its text, and metadata in a vector store.
4.  Embed the user's query.
5.  Search for the most similar vectors.
6.  Send the retrieved chunks to the LLM to generate an answer.

## 2. What Is a Vector Store?

A **vector store** is a system or library used to store numerical
vectors (embeddings) and retrieve vectors that are similar to a query
vector.

### Key features

-   **Storage:** Retains vectors and associated text or metadata, in
    memory or on disk.
-   **Similarity search:** Finds vectors most similar to a query vector.
-   **Indexing:** Uses data structures or algorithms to make similarity
    search faster, especially for high-dimensional vectors.
-   **CRUD operations:** Supports adding, reading, updating, and
    deleting vectors.

### Use cases

-   Semantic search
-   Retrieval-Augmented Generation (RAG)
-   Recommendation systems
-   Image and multimedia search

## 3. Vector Store vs. Vector Database

The terms are sometimes used interchangeably, but a useful distinction
is:

-   **Vector store:** A relatively lightweight library or service
    focused on storing embeddings and performing similarity search. It
    may require you to manage persistence and scaling.
-   **Vector database:** A database system built for vector search,
    often with additional features such as persistence, metadata
    filtering, access control, replication, backups, and distributed
    scaling.

The distinction is not strict: products vary in capabilities, and some
vector stores provide database-like features.

## 4. Vector Stores in LangChain

LangChain provides a common interface for working with different vector
stores, so a backend can often be changed with fewer application-code
changes.

Common operations:

-   `from_documents(...)` --- create a store from LangChain `Document`
    objects.
-   `from_texts(...)` --- create a store from text strings.
-   `add_documents(...)` / `add_texts(...)` --- add data to an existing
    store.
-   `similarity_search(query, k=...)` --- retrieve the top `k` similar
    documents.
-   **Metadata filtering:** Restrict retrieval by fields such as source,
    author, date, or category.

Examples of backends include FAISS, Chroma, Pinecone, and Weaviate.
Their persistence, filtering, and scaling capabilities differ.

## 5. Chroma (Example)

Chroma is an open-source vector database commonly used for local
development and small-to-medium applications, though its suitable scale
depends on deployment and workload.

A typical hierarchy is:

`Tenant → Database → Collection → Documents`

-   **Tenant:** A top-level organization or isolation boundary.
-   **Database:** Groups collections within a tenant.
-   **Collection:** Holds related records and their embeddings.
-   **Document/record:** Stores an item, often with text, metadata, and
    an ID.

## 6. How Vector Search Is Indexed

A vector store may use different search strategies. The main goal is to
find the nearest vectors to a query efficiently.

### A. Brute-force / Exact Nearest Neighbor (Flat Search)

-   Compare the query vector with every stored vector.
-   Rank results by a distance or similarity measure, such as cosine
    similarity or Euclidean distance.
-   **Advantage:** Exact results; simple to implement.
-   **Limitation:** Search cost grows with the number of vectors, making
    it slow for very large collections.

### B. Approximate Nearest Neighbor (ANN)

ANN methods search only a promising subset of vectors, so they are
usually much faster on large datasets. They may miss some true nearest
neighbors, trading a small amount of recall for speed.

Common ANN techniques:

-   **HNSW (graph-based):** Builds a multi-layer graph connecting nearby
    vectors. Search navigates the graph toward promising neighbors.
    Often a strong general-purpose choice for fast retrieval.
-   **IVF (cluster-based):** Groups vectors into clusters using methods
    such as k-means. At query time, searches only selected nearby
    clusters instead of the entire dataset.
-   **LSH (hash-based):** Hashes similar vectors into likely matching
    buckets, then searches those buckets. Useful in some settings, but
    performance depends strongly on the data and configuration.

### C. Clustering (e.g., k-means)

-   Groups vectors into clusters based on similarity.
-   Each cluster has a centroid (representative vector).
-   At query time, identify nearby centroids and search vectors in
    selected clusters.
-   **Important:** Clustering is a way to organize vectors and can
    support ANN search; it is not the same as exact nearest-neighbor
    search.

## 7. Why Not Use a Regular Relational Database (RDBMS)?

You're right: **relational databases can use indexes too**, and some
modern relational databases support vector indexes. The difference is
not that RDBMSs cannot index vectors.

Traditional relational indexes (such as B-trees) are designed mainly for
exact matches, ranges, sorting, and structured queries. Semantic search
asks a different question:

> Which vectors are closest to this query vector in a high-dimensional
> space?

That requires distance calculations and specialized indexing or search
methods.

  -----------------------------------------------------------------------
  Requirement             Traditional relational  Vector index
                          index                   
  ----------------------- ----------------------- -----------------------
  Find `age = 20`         Well suited             Not the purpose

  Find values in a range  Well suited             Not the purpose

  Find nearest embedding  Usually requires        Designed for this
  vectors                 scanning or special     
                          support                 

  Filter by metadata,     Can handle filters;     Commonly supported,
  then search by meaning  vector support depends  with backend-specific
                          on database             behavior
  -----------------------------------------------------------------------

An RDBMS can still be a good choice when the dataset is small, exact
relational queries are central, or the database has vector extensions
(for example, PostgreSQL with `pgvector`). In that case, one database
can handle both structured data and vector similarity search.

**Bottom line:** Vector stores specialize in similarity search over
embeddings. Their indexes---such as HNSW or IVF---make nearest-neighbor
retrieval efficient. Traditional relational databases excel at
structured queries, but they can also perform vector search when
equipped with suitable vector types and indexes.
