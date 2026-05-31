import logging
from weasyprint import HTML, CSS

logger = logging.getLogger("ats_resume_scorer")


def generate_combined_pdf(html_docs: dict[str, str]) -> bytes:
    """
    Generate a combined PDF from multiple HTML documents.
    """

    if not html_docs:
        raise ValueError("No HTML documents were provided.")

    documents = []

    try:
        # Render all HTML strings
        for name, html_str in html_docs.items():

            if not html_str or not html_str.strip():
                logger.warning(f"Skipping empty HTML document: {name}")
                continue

            logger.info(f"Rendering PDF section: {name}")

            doc = HTML(string=html_str).render()
            documents.append(doc)

        if not documents:
            raise ValueError(
                "No valid HTML documents could be rendered."
            )

        # Merge into first document
        first_doc = documents[0]

        for other_doc in documents[1:]:
            for page in other_doc.pages:
                first_doc.pages.append(page)

        logger.info(
            f"Successfully merged {len(documents)} PDF sections"
        )

        pdf_bytes = first_doc.write_pdf()

        logger.info(
            f"Generated PDF successfully ({len(pdf_bytes)} bytes)"
        )

        return pdf_bytes

    except Exception as e:
        logger.exception("PDF generation failed")
        raise RuntimeError(
            f"Failed to generate PDF: {str(e)}"
        ) from e







