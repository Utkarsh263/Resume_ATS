# 🎯 AI Resume Scorer — ATS Analysis Engine

> **An end-to-end AI-powered resume analysis platform** that scores resumes against job descriptions using NLP, semantic embeddings, and LLM-based parsing — then exports a beautiful 4-section PDF report.

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-Auth%20%2B%20DB-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLaMA%203.3%2070B-F55036?style=for-the-badge&logo=groq&logoColor=white)

</div>

---


## ✨ Features

- 📄 **Resume Parsing** — PDF & DOCX support with dual-fallback extraction (`pdfplumber` → `PyPDF2`), hyperlink extraction, and MIME validation
- 🤖 **LLM Extraction** — Groq's `llama-3.3-70b-versatile` at temperature 0 extracts name, contact info, skills, experience (with duration), projects, action verbs, and ATS keywords
- 📊 **5-Dimension ATS Scoring** — Weighted 100-point score across Formatting, Keywords, Content, Skill Validation, and ATS Compatibility
- 🔍 **Job Description Matching** — Semantic similarity via `all-MiniLM-L6-v2` + fuzzy keyword matching (`rapidfuzz`) + spaCy NER skills gap analysis
- ✅ **Skill Validation** — Cross-references claimed skills against actual project/experience entries using sentence embeddings
- 📑 **PDF Report Export** — 4-section WeasyPrint PDF: Score Summary · Skill Validation · JD Match · Recommendations + Checklist
- 🔐 **Auth & History** — Supabase JWT auth (HS256 + RS256/ES256 via JWKS), per-user analysis history, delete support
- 🌐 **Streamlit Frontend** — Clean UI with file upload, JD input, score display, and PDF download

---

## ⚙️ How It Works

```
Upload Resume (PDF/DOCX)
        │
        ▼
┌─────────────────────┐
│   File Validation   │  MIME check, size limit (5MB), DOCX/ZIP fix
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│   Text Extraction   │  pdfplumber → PyPDF2 fallback + hyperlink extraction
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│   Groq LLM Parse    │  llama-3.3-70b → skills, experience, projects, keywords
└────────┬────────────┘
         │
         ▼
┌──────────────────────────────────────────┐
│           Analysis Pipeline              │
│                                          │
│  ┌─────────────┐   ┌──────────────────┐  │
│  │ ATS Scoring │   │  Skill Validation│  │
│  │  (5 dims)   │   │ (embedding match)│  │
│  └─────────────┘   └──────────────────┘  │
│                                          │
│  ┌──────────────────────────────────┐    │
│  │       JD Matching (optional)     │    │
│  │  Semantic sim + fuzzy keywords   │    │
│  │  + spaCy NER skills gap          │    │
│  └──────────────────────────────────┘    │
│                                          │
│  ┌──────────────────────────────────┐    │
│  │  Feedback & Recommendation Engine│    │
│  └──────────────────────────────────┘    │
└─────────────────┬────────────────────────┘
                  │
                  ▼
        ┌──────────────────┐
        │  Save to Supabase│  (non-blocking, per user)
        └────────┬─────────┘
                 │
                 ▼
        ┌──────────────────┐
        │  PDF Generation  │  Jinja2 → HTML → WeasyPrint → merged PDF
        └──────────────────┘
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- `libmagic` system library
- WeasyPrint system dependencies (`pango`, `cairo`, `gdk-pixbuf`)

```bash
# Ubuntu / Debian
sudo apt install libmagic1 libpango-1.0-0 libcairo2 libgdk-pixbuf2.0-0

# macOS
brew install libmagic pango cairo gdk-pixbuf
```

### 1. Clone & Install

```bash
git clone https://github.com/Utkarsh263/ai-resume-scorer.git
cd ai-resume-scorer

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Download NLP Models

```bash
python -m spacy download en_core_web_md
```

> The `all-MiniLM-L6-v2` sentence transformer downloads automatically on first run.

### 3. Configure Environment

Create a `.env` file in the project root:

```env
# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-key
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_JWT_SECRET=your-jwt-secret

# Groq
GROQ_API_KEY=your-groq-api-key

# Optional
SENTENCE_TRANSFORMER_MODEL=all-MiniLM-L6-v2
```

For the Streamlit frontend, add secrets to `frontend/.streamlit/secrets.toml`:

```toml
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_ANON_KEY = "your-anon-key"
BACKEND_URL = "http://localhost:8000"
```

### 4. Supabase Setup

Create an `analyses` table in your Supabase project:

```sql
create table analyses (
  id            bigserial primary key,
  user_id       uuid references auth.users(id),
  filename      text,
  ats_score     float,
  keyword_match float,
  missing_keywords jsonb,
  analysis_result  jsonb,
  created_at    timestamptz default now()
);

-- Enable Row Level Security
alter table analyses enable row level security;

create policy "Users can manage own analyses"
  on analyses for all
  using (auth.uid() = user_id);
```

### 5. Run

**Backend (FastAPI):**
```bash
uvicorn backend.main:app --reload --port 8000
```

**Frontend (Streamlit):**
```bash
streamlit run frontend/streamlit_app.py
```

---

## 📊 Scoring Breakdown

| Component | Weight | What It Measures |
|---|---|---|
| **Formatting** | 20 pts | Section headers, bullet structure, length, layout |
| **Keywords & Skills** | 25 pts | Keyword density, skill coverage, ATS-relevant terms |
| **Content Quality** | 25 pts | Action verbs, quantified achievements, descriptions |
| **Skill Validation** | 15 pts | Skills backed by evidence in projects/experience |
| **ATS Compatibility** | 15 pts | Clean formatting, no parsing blockers |
| **Total** | **100 pts** | |

### Score Interpretation

| Score | Rating | Meaning |
|---|---|---|
| 80–100 | 🟢 Excellent | Strong ATS performance, ready to apply |
| 60–79 | 🟡 Good | A few targeted fixes will boost pass rate |
| Below 60 | 🔴 Needs Work | Significant improvements required |

---

## 🔌 API Reference

### `POST /api/v1/analyze-resume`
Analyze a resume file against an optional job description.

**Headers:** `Authorization: Bearer <supabase_access_token>`

**Form Data:**
| Field | Type | Required | Description |
|---|---|---|---|
| `resume` | `File` | ✅ | PDF or DOCX, max 5MB |
| `job_description` | `string` | ❌ | JD text for match analysis |

**Response:** `AnalysisResponse` JSON with full scores, feedback, and JD comparison.

---

### `GET /api/v1/history`
Returns all past analyses for the authenticated user.

---

### `DELETE /api/v1/history/{analysis_id}`
Delete a specific analysis entry.

---

### `POST /api/v1/generate-pdf`
Generate and download a 4-section PDF report from an `AnalysisResponse` payload.

---

### `GET /api/v1/history/{analysis_id}/pdf`
Generate PDF for a saved historical analysis.

---

### `GET /api/v1/health`
Health check — confirms NLP models are loaded.

```json
{
  "status": "healthy",
  "nlp_loaded": true,
  "embedder_loaded": true
}
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend API** | FastAPI + Uvicorn |
| **Frontend** | Streamlit |
| **LLM** | Groq — `llama-3.3-70b-versatile` |
| **NLP** | spaCy `en_core_web_md` |
| **Embeddings** | `sentence-transformers` — `all-MiniLM-L6-v2` |
| **Fuzzy Matching** | `rapidfuzz` |
| **File Parsing** | `pdfplumber`, `PyPDF2`, `python-docx`, `python-magic` |
| **PDF Generation** | `WeasyPrint` + `Jinja2` |
| **Auth & Database** | Supabase (PostgreSQL + JWT) |
| **HTTP Client** | `httpx` (async) |

---

## 🤝 Contributing

1. Fork the repo
2. Create your feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m 'Add my feature'`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <sub>Built with ❤️ using FastAPI · Groq · spaCy · Supabase · Streamlit</sub>
</div>
