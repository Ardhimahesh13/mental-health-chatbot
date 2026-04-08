def format_response(text):
    if not text :
        return text
    text = text.strip()

     # Remove excessive line breaks
    text = text.replace("\n\n\n", "\n\n")

    return text