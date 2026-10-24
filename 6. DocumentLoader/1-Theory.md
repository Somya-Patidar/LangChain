# LangChain Document Loaders --- Short Notes

## 1. Document Loaders

Document loaders are LangChain components used to load data from
different sources into a standardized format, usually LangChain
`Document` objects. The loaded documents can then be used for chunking,
embedding, retrieval, and generation.

### Document object

A `Document` stores the extracted text and its metadata.

``` python
Document(
    page_content="The actual text content",
    metadata={"source": "filename.pdf", ...}
)
```

-   `page_content`: The actual text extracted from the source.
-   `metadata`: Additional information such as source filename, page
    number, or other details.

Different sources (PDF, TXT, databases, websites, etc.) are converted
into a common `Document` format.

## 2. Common Document Loaders

### TextLoader

-   Loads plain-text `.txt` files into LangChain `Document` objects.
-   **Use cases:** Chat logs, scraped text, transcripts, code snippets,
    and other plain-text data.
-   **Limitation:** Works with plain-text files.

### PyPDFLoader

-   Loads content from PDF files.
-   Converts each PDF page into a separate `Document` object.
-   Metadata can include page number and source filename.
-   **Limitation:** Uses the PyPDF library; may not work well with
    scanned PDFs or complex layouts.

### DirectoryLoader

-   Loads multiple documents from a directory (folder).
-   Uses glob patterns to select files; `**` enables recursive search
    through subfolders.

  Glob pattern   What it loads
  -------------- ----------------------------------------
  `**/*.txt`     All `.txt` files in all subfolders
  `*.pdf`        All `.pdf` files in the root directory
  `data/*.csv`   All `.csv` files in the `data/` folder
  `**/*`         All files in all subfolders

### WebBaseLoader

-   Loads and extracts text content from web pages (URLs).
-   Uses BeautifulSoup to parse HTML and extract visible text.
-   **Use cases:** Text-based blogs, news articles, and public websites.
-   **Limitations:** Not suitable for JavaScript-heavy pages; typically
    extracts static HTML content.

### CSVLoader

-   Loads CSV files into LangChain `Document` objects.
-   By default, creates one `Document` per row.

## 3. Choosing a PDF Loader

  -----------------------------------------------------------------------
  Use case                            Recommended loader
  ----------------------------------- -----------------------------------
  Simple, clean PDFs                  `PyPDFLoader`

  PDFs with tables or columns         `PDFPlumberLoader`

  Scanned or image-based PDFs         `UnstructuredPDFLoader` or
                                      `AmazonTextractPDFLoader`

  Need layout and image data          `PyMuPDFLoader`

  Want best structure extraction      `UnstructuredPDFLoader`
  -----------------------------------------------------------------------

## 4. Eager Loading vs. Lazy Loading

### `load()`

-   Eager loading: loads all documents immediately.
-   Returns a list of `Document` objects.
-   Keeps all loaded documents in memory.
-   Best for small collections or when all documents are needed upfront.

### `lazy_load()`

-   Lazy loading: loads documents on demand, one at a time.
-   Returns a generator/iterator of `Document` objects.
-   Does not load all documents into memory at once.
-   Best for large files or many documents, and for streaming processing
    such as chunking or embedding.

## 5. Custom Document Loaders

Custom loaders can be created when built-in loaders do not support a
data source or its required extraction format.

The goal is to extract source data and convert it into LangChain
`Document` objects, containing `page_content` and `metadata`.

Typical flow:

1.  Read or access the source data.
2.  Extract its text or content.
3.  Create one or more `Document` objects.
4.  Include useful metadata such as source, page, or record identifiers.
