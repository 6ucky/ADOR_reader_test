# ADOR Reader Test

## Objectives
This coding test focuses on the **Named Entity Recognition (NER)** feature of the product. Your task is to develop a **Proof of Concept (PoC)** that demonstrates the tool's ability to parse and extract **financial entities** from documents. 

## Approach
Depending on the nature of the provided document, you may utilize one or a combination of the following methods:
- **Rule-Based Parser**: If financial entities follow a well-defined pattern.
- **NER Model (spaCy)**: A trained Named Entity Recognition model for extracting structured financial data.
- **Large Language Model (LLM - OpenAI GPT-3.5)**: For a more flexible and context-aware entity extraction.

## Data Pipeline
The **data pipeline** follows a **general method** developed during the **GRDF mission**. It is designed to process:
- **File Readers:** Supports `.docx`, `.xlsx`, `.pptx`, and `.pdf` files via `DocxReader`, `XlsxReader`, `PptxReader`, and `PdfReader`.
- **Text** (Extracted using `SimpleDirectoryReader`)
- **Tables** (Extracted from all the files)
- **Images** (Processed via multi-modal techniques)

The test includes three extraction methods:
1. **Rule-Based Extraction** (`/rule` endpoint)
   - Uses regular expressions to extract structured financial information.
2. **NER Extraction (spaCy)** (`/spacy` endpoint)
   - Utilizes the `en_core_web_sm` model to detect and classify entities.
3. **LLM-Based Extraction (OpenAI GPT-3.5)** (`/llm` endpoint)
   - Employs OpenAI's GPT-3.5-turbo model for more flexible entity recognition.

## Test Results
The test results are stored in the **Jupyter Notebook** for evaluation and documentation purposes.

## API Endpoints
- `GET /rule` - Extracts financial entities using a rule-based approach.
- `POST /spacy` - Extracts financial entities using spaCy’s NER model.
- `GET /llm` - Uses OpenAI's GPT-3.5 to extract and understand financial entities from documents.

## Additional Resources
- [LlamaIndex](https://www.llamaindex.ai/)

