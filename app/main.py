from fastapi import FastAPI
from app.api.models import QueryRequest, RecommendationResponse

app = FastAPI(
  title="Smart Ecommerce MCP Tool",
  description="Provides unbiased, user-centric product recommendations.",
  version="0.1.0"
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Smart Ecommerce MCP Tool"}

@app.post("/process-query", response_model=RecommendationResponse)
async def process_query(request: QueryRequest):
    """
    Processes a user query and returns a product recommendation.
    
    This endpoint simulates the entire MCP workflow:
    1.  **Intent Analysis**: Understands the user's query.
    2.  **Data Collection**: Gathers product info, reviews, and social media sentiment.
    3.  **AI Processing**: Analyzes the data for sentiment, bias, and key insights.
    4.  **Recommendation Generation**: Creates a user-centric recommendation.
    """
    
    # 1. Mock Intent Analysis
    intent = "product_comparison"
    
    # 2. Mock Data Collection
    product_data = {
        "product_a": {"name": "Laptop Pro X", "price": 1200},
        "product_b": {"name": "Laptop Plus Y", "price": 1100}
    }
    reviews = [
        {"source": "TechCrunch", "content": "Laptop Pro X has a great screen."},
        {"source": "Reddit", "content": "Laptop Plus Y has better battery life."}
    ]
    
    # 3. Mock AI Processing
    analysis_summary = "Both laptops are good, but Pro X is better for visuals and Plus Y is better for portability."
    
    # 4. Mock Recommendation Generation
    mock_recommendation = {
        "query": request.query,
        "recommendations": [
            {
                "product_name": "Laptop Pro X",
                "recommendation_reason": "Based on your request for a 'good gaming laptop', the Pro X's superior graphics card makes it a better fit.",
                "confidence_score": 0.85,
                "pros": ["Excellent display", "Powerful GPU"],
                "cons": ["Slightly more expensive", "Heavier"],
                "source_summary": "Praised by professional reviewers for its performance."
            },
            {
                "product_name": "Laptop Plus Y",
                "recommendation_reason": "A solid alternative if battery life is a priority.",
                "confidence_score": 0.75,
                "pros": ["Longer battery life", "More lightweight"],
                "cons": ["Less powerful graphics"],
                "source_summary": "Popular on forums for its portability and value."
            }
        ],
        "summary": "For gaming, the Laptop Pro X is the top recommendation. However, if you need a more portable option for general use, the Laptop Plus Y is a strong contender."
    }
    
    return RecommendationResponse(**mock_recommendation)




