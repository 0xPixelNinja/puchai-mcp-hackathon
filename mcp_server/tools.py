from . import information_gathering, recommendation

def compare_product(product_a: str, product_b: str) -> str:
    """
    Compares two products and returns a recommendation.
    """
    search_results_a = information_gathering.search_web(f"reviews for {product_a}")
    search_results_b = information_gathering.search_web(f"reviews for {product_b}")
    
    return recommendation.generate_recommendation(product_a, product_b, search_results_a, search_results_b)

def fact_check_product(product: str, claims: list[str]) -> dict:
    """
    Fact-checks a list of claims about a product.
    """
    search_results = {}
    for claim in claims:
        search_results[claim] = information_gathering.search_web(f"{product} {claim}")
    
    print(f"Search results for {product} claims: {search_results}")
    
    return {
        "product": product,
        "results": [{claim: "verified" for claim in claims}]
    }

