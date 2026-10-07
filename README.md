# OmniDoc-RAG — Multimodal Document Intelligence System

> **HNX26PSI01 — Multimodal Document Intelligence & Vision RAG Engine**

OmniDoc-RAG is an end-to-end multimodal document question-answering system that can understand complex PDF documents containing text, tables, charts, graphs, images, and scanned pages.

The system uses Retrieval-Augmented Generation (RAG), vector embeddings, MongoDB Atlas, PDF processing, visual analysis, and Gemini AI to retrieve relevant evidence and generate answers with page-level source attribution.

---

# 1. What Does the Project Do?

## 1.1 Project Overview

Traditional document question-answering systems mainly extract text from PDFs and search through the extracted text.

However, real-world documents often contain important information inside:

- Tables
- Charts
- Graphs
- Images
- Scanned pages
- Multi-column layouts
- Multiple pages
- Multiple documents

OmniDoc-RAG is designed to handle these different types of content.

The system allows a user to:

1. Upload one or more PDF documents.
2. Process the documents.
3. Identify text, tables, images, charts and visual regions.
4. Generate embeddings for the processed information.
5. Store embeddings and document metadata in MongoDB Atlas.
6. Ask questions in natural language.
7. Convert the question into an embedding.
8. Perform similarity search against stored document vectors.
9. Retrieve the most relevant evidence.
10. Send the retrieved evidence to Gemini for reasoning.
11. Generate the final answer.
12. Display the answer together with document/page/evidence information.

---

## 1.2 Overall Workflow

```text
                    USER
                     |
                     v
              Upload PDF
                     |
                     v
             PDF Preprocessing
                     |
          +----------+----------+
          |          |          |
          v          v          v
        Text       Tables     Images/
                               Charts
          |          |          |
          +----------+----------+
                     |
                     v
          Multimodal Processing
                     |
                     v
             Embedding Generation
                     |
                     v
              MongoDB Atlas
          Vector + Metadata Storage
                     |
                     |
                USER QUESTION
                     |
                     v
             Question Embedding
                     |
                     v
              Similarity Search
                     |
                     v
             Relevant Evidence
                     |
                     v
                Gemini API
                     |
                     v
          Answer + Page + Evidence
```

---

## 1.3 PDF Preprocessing

After a PDF is uploaded, the backend preprocesses the document.

The preprocessing stage identifies the available content and preserves page-level information.

Conceptually:

```text
PDF
 |
 +---- Page 1
 |       |
 |       +---- Text
 |       +---- Table
 |       +---- Chart
 |
 +---- Page 2
 |       |
 |       +---- Text
 |       +---- Image
 |
 +---- Page 3
         |
         +---- Scanned Content
```

The system preserves metadata such as:

```text
Document Name
Page Number
Section
Content Type
Content
Bounding Box
Embedding
```

This metadata is important because the system must not only answer a question, but also identify where the information came from.

---

## 1.4 Embedding and Retrieval

After document processing, the relevant content is converted into numerical vector representations called embeddings.

Example:

```text
Document Chunk
       |
       v
Embedding Model
       |
       v
Numerical Vector
       |
       v
MongoDB Atlas
```

When a user asks a question:

```text
User Question
       |
       v
Question Embedding
       |
       v
Vector Similarity Search
       |
       v
Top Relevant Document Chunks
```

The retrieved evidence is then passed to the Gemini model for reasoning and final answer generation.

---

## 1.5 Page-Level Evidence

A major feature of the project is source attribution.

The generated answer can provide information such as:

```text
Document:
Q2_vs_Q4_Manufacturing_Report.pdf

Page:
2

Section:
Production Efficiency

Content Type:
Chart
```

Therefore, the user can trace the generated answer back to the original document.

---

## 1.6 Example Question

A typical multimodal question is:

> Compare production efficiency between Q2 and Q4 and identify the three biggest reasons for the change.

The answer may require:

```text
Table Evidence
       +
Chart Evidence
       +
Text Evidence
       |
       v
Multimodal Reasoning
       |
       v
Final Answer
       +
Source Pages
```

This demonstrates why the system is more than a simple text search system.

---

# 2. What Technologies, Libraries and Models Are Used?

## 2.1 Frontend

The frontend provides the interactive web interface.

### Technologies

- React
- Vite
- JavaScript
- HTML
- CSS

### Frontend Responsibilities

The frontend handles:

- PDF upload
- Document selection
- Question input
- Sending queries to the backend
- Displaying generated answers
- Displaying source information
- Displaying document pages
- Displaying evidence and visual regions

---

## 2.2 Backend

The backend contains the main document intelligence pipeline.

### Technologies

- Python
- FastAPI
- Uvicorn

### Backend Responsibilities

The backend handles:

- PDF upload
- PDF preprocessing
- Text extraction
- Page rendering
- Document layout processing
- Visual content processing
- Embedding generation
- Vector storage
- Similarity retrieval
- RAG orchestration
- Gemini API communication
- Source attribution

---

## 2.3 PDF Processing Libraries

### PyMuPDF

PyMuPDF is used for PDF processing.

It is used for:

- Opening PDF documents
- Reading pages
- Extracting text
- Rendering PDF pages
- Processing page layouts
- Obtaining page-level information
- Obtaining bounding-box information
- Generating visual page representations

The project uses the `fitz` interface provided by PyMuPDF.

---

### PyPDF

PyPDF is used for additional PDF handling and document operations.

---

### Pillow

Pillow is used for image processing.

---

### Matplotlib

Matplotlib is used where required for generating or handling chart-based sample documents and visual data.

---

### ReportLab

ReportLab is used for generating realistic/sample PDF documents for testing and evaluation.

---

## 2.4 AI Model / Gemini API

The project uses the Google Gemini API for AI-based reasoning and response generation.

Gemini is used to analyze retrieved evidence and generate the final natural-language response.

For visual document content, the Gemini vision-language capability can be used to reason over:

- Charts
- Graphs
- Images
- Visual document regions

The Gemini API is accessed using an API key.

The API key is stored in an environment variable and is not hard-coded into the application.

---

## 2.5 Embedding Model

Embeddings are used to represent document content and user questions as numerical vectors.

The embedding process allows semantic similarity search.

For example:

```text
"production efficiency increased in Q4"
```

and

```text
"Q4 manufacturing performance improved"
```

can have similar vector representations even though the exact words are different.

The project uses a pretrained embedding approach rather than training a custom machine-learning model from scratch.

---

## 2.6 MongoDB Atlas

MongoDB Atlas is used as the database and vector storage layer.

It stores information such as:

```text
Document ID
Document Name
Page Number
Section
Content Type
Content
Embedding
Bounding Box
Metadata
```

Example document:

```json
{
  "document": "Q2_vs_Q4_Manufacturing_Report.pdf",
  "page": 2,
  "section": "Production Efficiency",
  "content_type": "chart",
  "content": "Production efficiency increased from Q2 to Q4",
  "embedding": [0.012, -0.231, 0.442, "..."]
}
```

MongoDB Atlas Vector Search can be used to retrieve the most semantically relevant vectors.

---

## 2.7 RAG

RAG stands for:

**Retrieval-Augmented Generation**

The project follows:

```text
Question
   |
   v
Question Embedding
   |
   v
Vector Search
   |
   v
Relevant Evidence
   |
   v
Gemini
   |
   v
Final Answer
```

The purpose of RAG is to provide the language model with relevant information retrieved from the uploaded documents.

---

## 2.8 Mathematical Verification

For questions involving numerical comparisons, the system can perform numerical reasoning using retrieved values.

Example:

```text
Q2 Efficiency = 72.4%
Q4 Efficiency = 91.8%

Absolute Change
= 91.8 - 72.4
= 19.4 percentage points
```

This helps reduce errors in numerical answers.

---

# 3. How to Install Dependencies?

## 3.1 Prerequisites

Install the following:

- Python 3.10 or later
- Node.js 18 or later
- npm
- Git
- MongoDB Atlas account
- Google AI Studio / Gemini API key

---

## 3.2 Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd <YOUR_PROJECT_FOLDER>
```

---

## 3.3 Install Backend Dependencies

From the project root:

```bash
pip install fastapi uvicorn PyMuPDF pypdf reportlab pillow matplotlib pymongo requests pydantic
```

If a `requirements.txt` file is included in the repository, use:

```bash
pip install -r requirements.txt
```

---

## 3.4 Install Frontend Dependencies

Move into the frontend directory:

```bash
cd frontend
```

Install Node.js dependencies:

```bash
npm install
```

Return to the project root:

```bash
cd ..
```

---

# 4. How to Configure and Run the System?

## 4.1 Configure Gemini API

Create a Gemini API key through Google AI Studio.

Create:

```text
backend/.env
```

Add:

```env
GEMINI_API_KEY=your_gemini_api_key
MONGO_URI=your_mongodb_atlas_connection_string
```

Replace the placeholder values with the actual credentials.

### Important

Do not:

- Put API keys directly inside Python/JavaScript source code.
- Commit `.env` to GitHub.
- Expose API keys in the frontend.

Add `.env` to `.gitignore`:

```text
.env
```

---

## 4.2 Configure MongoDB Atlas

Create a MongoDB Atlas cluster.

Then:

1. Create the required database.
2. Create the required collection.
3. Configure network access.
4. Create database credentials.
5. Copy the MongoDB connection string.
6. Add it to the backend `.env`.

Example:

```env
MONGO_URI=mongodb+srv://<username>:<password>@<cluster>/<database>
```

---

## 4.3 Start the Backend

From the project root:

```bash
python backend/main.py
```

If the FastAPI application is exposed as `app`, the alternative command is:

```bash
uvicorn backend.main:app --reload
```

The backend normally runs on:

```text
http://localhost:8000
```

---

## 4.4 Start the Frontend

Open a second terminal.

```bash
cd frontend
npm run dev
```

The frontend normally runs on:

```text
http://localhost:5173
```

Open the displayed URL in a browser.

---

## 4.5 System Components

The project is organized approximately as:

```text
project/
│
├── backend/
│   ├── main.py
│   ├── rag_engine.py
│   ├── vision_parser.py
│   ├── gemini_vlm.py
│   ├── embeddings.py
│   ├── mongo_db.py
│   ├── generate_sample_docs.py
│   ├── sample_docs/
│   └── .env
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── ...
│
├── README.md
└── .gitignore
```

### Important Backend Files

#### `main.py`

Handles the backend API and application entry point.

#### `rag_engine.py`

Handles the RAG pipeline, retrieval and answer orchestration.

#### `vision_parser.py`

Handles PDF page rendering, layout information and visual document processing.

#### `gemini_vlm.py`

Handles Gemini-based visual/AI reasoning.

#### `embeddings.py`

Handles embedding generation.

#### `mongo_db.py`

Handles MongoDB Atlas database operations and storage.

#### `generate_sample_docs.py`

Generates sample documents used for demonstration/testing.

---

# 5. How to Reproduce the Demonstrated Results?

This section describes the complete demonstration procedure.

---

## 5.1 Start the System

Start MongoDB Atlas and make sure the required environment variables are configured.

Start the backend:

```bash
python backend/main.py
```

Then start the frontend:

```bash
cd frontend
npm run dev
```

Open:

```text
http://localhost:5173
```

---

## 5.2 Load or Generate Sample Documents

The project includes sample mixed-content documents for demonstration.

Example documents include:

```text
Q2_vs_Q4_Manufacturing_Report.pdf
TechCorp_Financial_Statements_2025.pdf
Scanned_SupplyChain_Audit_Messy.pdf
Global_Energy_Transition_Whitepaper.pdf
```

These documents contain different types of information such as:

- Text
- Tables
- Charts
- Financial data
- Operational data
- Scanned/visual content

---

## 5.3 Upload a PDF

Use the web interface to upload a PDF.

Example:

```text
Q2_vs_Q4_Manufacturing_Report.pdf
```

The backend receives the PDF and starts document processing.

---

## 5.4 Preprocess the PDF

The backend processes each page.

The processing pipeline identifies:

```text
Text
Tables
Charts
Images
Scanned Content
Page Layout
```

Each piece of information retains its page-level metadata.

For example:

```json
{
  "document": "Q2_vs_Q4_Manufacturing_Report.pdf",
  "page": 1,
  "content_type": "table"
}
```

---

## 5.5 Generate Embeddings

The processed document information is converted into embeddings.

```text
PDF Content
     |
     v
Content Chunks
     |
     v
Embedding Model
     |
     v
Vectors
```

The vectors are stored in MongoDB along with the source metadata.

---

## 5.6 Ask a Question

Use the RAG query box to ask:

```text
Compare production efficiency between Q2 and Q4 and identify the three biggest reasons for the change.
```

---

## 5.7 Question Embedding

The system converts the question into a vector:

```text
User Question
      |
      v
Question Embedding
      |
      v
Query Vector
```

---

## 5.8 Similarity Search

The query vector is compared against stored document vectors.

The system retrieves the most relevant evidence.

For example:

```text
Query
 |
 +---- Page 1 — Production Table
 |
 +---- Page 2 — Efficiency Chart
 |
 +---- Page 2 — Explanation Text
```

---

## 5.9 RAG Generation

The retrieved evidence is passed to the Gemini model.

Gemini uses the retrieved context to generate a final response.

The answer is expected to remain grounded in the retrieved evidence.

---

## 5.10 Final Response

The frontend displays the final answer together with its evidence.

Example:

```text
Answer:

Production efficiency increased from Q2 to Q4.

The main reasons were:
1. Reduced equipment downtime
2. Automated quality inspection
3. Improved predictive maintenance

Sources:

Q2_vs_Q4_Manufacturing_Report.pdf
Page 1 — Production Efficiency Table

Q2_vs_Q4_Manufacturing_Report.pdf
Page 2 — Efficiency Chart

Q2_vs_Q4_Manufacturing_Report.pdf
Page 2 — Operational Reasons
```

---

# Demonstration Questions

The following questions can be used to reproduce and test the demonstrated functionality.

## Question 1 — Text Retrieval

```text
What is the main objective of the manufacturing report?
```

Expected system behavior:

```text
Question
   ↓
Vector Search
   ↓
Relevant Text
   ↓
Gemini
   ↓
Answer + Page Source
```

---

## Question 2 — Table Retrieval

```text
What were the production efficiency values in Q2 and Q4?
```

Expected behavior:

```text
Question
   ↓
Retrieve relevant table
   ↓
Extract numerical values
   ↓
Generate answer
   ↓
Show page source
```

---

## Question 3 — Chart Understanding

```text
What trend is shown in the production efficiency chart?
```

Expected behavior:

```text
Question
   ↓
Retrieve relevant visual evidence
   ↓
Analyze chart
   ↓
Generate answer
   ↓
Show chart page
```

---

## Question 4 — Multimodal Question

```text
Compare production efficiency between Q2 and Q4 and identify the three biggest reasons for the change.
```

Expected behavior:

```text
Table Evidence
      +
Chart Evidence
      +
Text Evidence
      |
      v
RAG
      |
      v
Gemini Reasoning
      |
      v
Combined Answer
      +
Page-Level Sources
```

This is the primary demonstration of the multimodal RAG capability.

---

## Question 5 — Cross-Document Question

```text
Compare the operational performance from the manufacturing report with the financial performance from the financial statement.
```

Expected behavior:

```text
Manufacturing Report
        +
Financial Report
        |
        v
Cross-Document Retrieval
        |
        v
Relevant Evidence
        |
        v
Gemini Reasoning
        |
        v
Combined Answer
        +
Sources from Both Documents
```

---

# Expected Demonstration Result

For a successful demonstration, the system should show:

```text
User Question
      ↓
Relevant Evidence Retrieved
      ↓
AI-Generated Answer
      ↓
Document Name
      ↓
Page Number
      ↓
Section / Content Type
```

The important requirement is that the system should not return only an unsupported answer.

It should also identify the evidence used to generate that answer.

---

# Dataset

The project uses realistic/sample mixed-content PDF documents for testing and demonstration.

The document collection includes examples containing:

- Text
- Tables
- Charts
- Graphs
- Images
- Scanned pages
- Financial information
- Operational information

The dataset is primarily used for:

- System testing
- Retrieval evaluation
- Multimodal question testing
- Demonstration
- Benchmarking

The project does not require training a custom ML model from scratch.

Instead, pretrained embedding and generative AI models are integrated into the RAG pipeline.

---

# End-to-End Architecture

```text
                    PDF DOCUMENT
                         |
                         v
                PDF PREPROCESSING
                         |
          +--------------+--------------+
          |              |              |
          v              v              v
        TEXT          TABLES        IMAGES/CHARTS
          |              |              |
          +--------------+--------------+
                         |
                         v
               MULTIMODAL PROCESSING
                         |
                         v
                 EMBEDDING GENERATION
                         |
                         v
                 MONGODB ATLAS
                VECTOR + METADATA
                         |
                         |
                    USER QUERY
                         |
                         v
                  QUERY EMBEDDING
                         |
                         v
                  VECTOR SEARCH
                         |
                         v
                RELEVANT EVIDENCE
                         |
                         v
                    GEMINI API
                         |
                         v
             FINAL ANSWER GENERATION
                         |
             +-----------+-----------+
             |           |           |
             v           v           v
           Answer     Page No.    Evidence
```

---

# Key Features

## Multimodal Document Understanding

The system is designed to work with different document content types:

```text
Text
Tables
Charts
Images
Scanned Pages
```

---

## Semantic Retrieval

Instead of relying only on exact keyword matching, embeddings allow semantically similar content to be retrieved.

---

## Vector Database

MongoDB Atlas stores document embeddings together with document metadata.

---

## RAG-Based Answer Generation

The retrieved evidence is supplied to Gemini to generate the final answer.

---

## Page-Level Attribution

The system preserves document and page information so answers can be traced back to the source.

---

## Cross-Document Reasoning

The system can retrieve relevant information from multiple documents for a single question.

---

# Security

API keys and database credentials should never be committed to the repository.

Use:

```text
backend/.env
```

Example:

```env
GEMINI_API_KEY=your_api_key
MONGO_URI=your_mongodb_connection_string
```

Add `.env` to `.gitignore`:

```text
.env
```

Never expose real API keys in:

- GitHub
- Frontend code
- Screenshots
- README files
- Public repositories

---

# Troubleshooting

## Backend Does Not Start

Check:

```bash
python --version
```

and reinstall dependencies:

```bash
pip install -r requirements.txt
```

---

## Frontend Does Not Start

Run:

```bash
cd frontend
npm install
npm run dev
```

---

## Gemini API Error

Check that:

```env
GEMINI_API_KEY=your_valid_key
```

is correctly configured.

---

## MongoDB Connection Error

Check:

- MongoDB cluster status
- Username
- Password
- Connection string
- Network access
- IP allowlist
- Database permissions

---

# Conclusion

OmniDoc-RAG provides an end-to-end solution for multimodal document question answering.

The complete pipeline is:

```text
PDF Upload
    ↓
PDF Preprocessing
    ↓
Text / Tables / Images / Charts
    ↓
Embedding Generation
    ↓
MongoDB Vector Storage
    ↓
Question Embedding
    ↓
Similarity Search
    ↓
Relevant Evidence
    ↓
Gemini Reasoning
    ↓
Answer + Page-Level Evidence
```

The system is designed not only to answer questions from documents, but also to provide traceable evidence showing **where the answer came from**.

This makes the system suitable for complex document intelligence tasks involving text, tables, charts, images, scanned pages and cross-document information retrieval.
