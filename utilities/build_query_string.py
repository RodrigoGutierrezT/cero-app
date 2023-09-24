def build_query_string(params) -> str:
    return "?q="+(str(params)).replace(' ', '').replace('\'', '"')