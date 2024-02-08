from weasyprint import HTML, Document

def pdf(html_content: str) -> Document:
    return HTML(string=html_content).render()