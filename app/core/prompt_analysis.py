async def understand_user_prompt(prompt: str) -> str:
    """
    Understand the user's prompt and determine the intent.
    """
    if "compare" in prompt.lower():
        return "compare_product"
    elif "fact-check" in prompt.lower():
        return "fact_check_product"
    elif "find" in prompt.lower():
        return "find_product"
    else:
        return "unknown"
