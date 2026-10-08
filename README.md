# Simple PDF chat with FastAPI and LlamaIndex

Use Python 3.10+ and run these commands from the project root:

```powershell
python -m pip install -r requirements.txt
python -m uvicorn backend.llama:app --reload
```

Set `OPENAI_API_KEY` in your environment, `backend/.env`, or the root `.env`.
Existing environment variables take priority. Optional: set `OPENAI_MODEL`
to override the default `gpt-4o-mini`.

Place text-based PDFs in `backend/business_knowledge`, or upload them using
`POST /upload-file` in http://127.0.0.1:8000/docs. Then call `POST /chat`:

```json
{"user_msg": "What courses do you offer?"}
```

The response contains `answer` and source filenames/page numbers.
Each question is independent (no conversation history).

The index lives in memory and is built on the first question. Uploading a PDF
causes it to rebuild on the next question. Restart after manually adding,
editing, or removing PDFs. No separate vector database is needed.
OpenAI is used for embeddings and answers, so API calls incur usage charges.
Scanned/image-only PDFs require OCR before uploading.

Reference: [LlamaIndex PDF loading](https://developers.llamaindex.ai/python/framework/module_guides/loading/simpledirectoryreader/).
