from app.report_generator import generate_txt, generate_docx, generate_pdf

def create_report(data: dict, format: str, output_path: str):
    content=f"""
Document Type: {data.get("document_type","N/A")}
Extracted Data:
{data.get("extracted_data")}

Summary:
{data.get("summary", "N/A")}"""
    format=format.lower()
    match format:
        case "txt":
            generate_txt(content, output_path)
        case "pdf":
            generate_pdf(content, output_path)
        case "docx":
            generate_docx(content, output_path)
        case _:
            raise ValueError("Unsupported report format")
