search_function_description = {
    "name": "search_vector_database",
    "description": "Search the associated vector database. Call this to retrieve information to answer FAQ questions.",
    "parameters": {
        "type": "object",
        "properties": {
            "q": {"type": "string", "description": "The query string."},
        },
        "required": ["q"],
        "additionalProperties": False,
    },
}

openai_tools = [
    {
        "type": "function",
        "function": search_function_description,
    }
]
