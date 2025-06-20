# pdf-extraction-mcp
# 🧾 PDF Content Extractor with OCR Support

A Python-based tool that extracts content from PDF files, including scanned documents, using OCR (Tesseract). Includes both a **CLI interface** and an optional **Streamlit web UI** for ease of use.

---

## ✨ Features

- Extract text from **standard PDFs**
- Extract text from **scanned PDFs** using **Tesseract OCR**
- Support for selecting **specific pages** (including negative indexing like `-1` for last page)
- Simple **command-line interface**
- Optional **Streamlit-based web app**

---

## 🚀 Quickstart

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/pdf-extraction-mcp.git
cd pdf-extraction-mcp
2. Install dependencies
We recommend using a virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt
Make sure you have Tesseract OCR installed:

macOS: brew install tesseract
Ubuntu: sudo apt install tesseract-ocr
Windows: Download installer
🛠 Usage

✅ Command Line Interface
python main.py /path/to/file.pdf --pages "1,2,-1"
--pages is optional. Use comma-separated values. Negative indices are supported (e.g., -1 = last page).
🌐 Streamlit Web App
Run the app:

streamlit run app.py
Then open http://localhost:8501 in your browser.

📁 Project Structure

pdf-extraction-mcp/
├── pdf_extraction/
│   ├── __init__.py
│   ├── pdf_extractor.py    # Core logic
│   └── server.py            # Optional server interface
├── main.py                  # CLI entry point
├── app.py                   # Streamlit interface
├── requirements.txt
├── setup.py (optional)
└── README.md
🧪 Example Output

Page 1:
Lorem ipsum dolor sit amet...

Page 2:
(Scanned image text via OCR)
合同书
这是测试页。
🧱 Dependencies

PyPDF2
pytesseract
pymupdf
Pillow
streamlit (for UI)
Install with:

pip install -r requirements.txt
📝 License

MIT License.

👤 Author

Built by Aditya. Feel free to contribute or open issues!