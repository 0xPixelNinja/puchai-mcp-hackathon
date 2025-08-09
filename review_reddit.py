from app.utils.review_analyzer import analyze_reviews
import json

results = analyze_reviews("one plus 13 pro")
print(json.dumps(results, indent=2))