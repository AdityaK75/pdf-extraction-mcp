import argparse
from pdf_extractor import PDFExtractor

def main():
    parser = argparse.ArgumentParser(description="Extract PDF contents.")
    parser.add_argument("pdf_path", type=str, help="Path to the PDF file")
    parser.add_argument("--pages", type=str, default=None, help="Pages to extract (e.g., '1,2,-1')")

    args = parser.parse_args()

    extractor = PDFExtractor()
    content = extractor.extract_content(args.pdf_path, args.pages)
    print(content)

if __name__ == "__main__":
    main()
