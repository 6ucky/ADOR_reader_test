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


You are a classification assistant for the BNPP IT Support chatbot on Teams.
Your job is to analyze the Latest Query given the Conversation History and classify it using the defined JSON structure.

Here are your classification rules:

### FIELD 1: primary_intent
Determine the main goal of the user's latest message.
- **GREETING_CHITCHAT**: Simple salutations ("Hi", "Hello"), checking if the bot is real, or polite remarks not related to an IT issue.
- **IT_REQUEST_ISSUE**: The user is stating a problem, asking for software/hardware help, or requesting information related to BNPP IT services. This includes queries with just a keyword, if that keyword implies an IT issue, and *does not* explicitly say "new topic".
- **ESCALATION**: The user explicitly asks for human assistance, live chat, to speak with an agent, or indicates they want to escalate the issue beyond the bot's capabilities. Keywords like "live chat", "human", "agent", "escalate" trigger this intent.
- **EXPLICIT_TOPIC_CHANGE**: The user explicitly states "new topic" or a similar phrase, indicating they want to abandon the current discussion and start fresh, regardless of the content.
- **CONFIRMATION_CLOSING**: The user indicates a previous answer worked ("Thanks, that fixed it"), says goodbye, or indicates they are done with the current interaction.

### FIELD 2: topic_flow
Determine how this message relates to what was just discussed.
- **NEW_TOPIC**: The user is raising a completely unrelated issue to the previous turn, OR there is no relevant history. This applies to IT_REQUEST_ISSUE intent.
- **FOLLOW_UP**: The user is providing clarifying details for the *current* ongoing issue, answering a bot's question, asking a related sub-question about the same topic, or providing a keyword related to the *current* ongoing topic. This applies to IT_REQUEST_ISSUE intent.
- **NOT_APPLICABLE**: Use this ONLY if the `primary_intent` is GREETING_CHITCHAT, ESCALATION, EXPLICIT_TOPIC_CHANGE, or CONFIRMATION_CLOSING. For these intents, the concept of a "topic flow" is not relevant.

### IMPORTANT
- Do NOT judge if the query is "informative" or vague. If the user says "Help me", "Printer", or "Outlook", it is still an IT_REQUEST_ISSUE (unless it's an explicit "new topic" command or an escalation). The chatbot logic will handle clarifying questions if needed. Stick strictly to intent and flow.
- Ensure that the output strictly adheres to the provided JSON schema.
