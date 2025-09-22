from flask import Flask, request, jsonify
from difflib import SequenceMatcher

app = Flask(__name__)

def smart_match(keyword, cv_text):
    keyword = keyword.lower().strip()
    cv_text = cv_text.lower()
    
    if keyword in cv_text:
        return True
    
    words = cv_text.split()
    for word in words:
        similarity = SequenceMatcher(None, keyword, word).ratio()
        if similarity > 0.8:
            return True
    
    return False

def analyze_cv(cv_text, required_keywords):
    matches = []
    
    for keyword in required_keywords:
        if smart_match(keyword, cv_text):
            matches.append(keyword)
    
    total_keywords = len(required_keywords)
    matched_count = len(matches)
    
    if total_keywords > 0:
        score = (matched_count / total_keywords) * 100
    else:
        score = 0
    
    if score >= 70:
        status = "Interview"
    elif score >= 50:
        status = "Under Review"
    else:
        status = "Rejected"
    
    return {
        "matches": matches,
        "score": round(score, 2),
        "status": status,
        "matched_count": matched_count,
        "total_keywords": total_keywords
    }

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    
    cv_text = data.get('cv_text', '')
    required_keywords = data.get('keywords', [])
    
    result = analyze_cv(cv_text, required_keywords)
    return jsonify(result)

@app.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "AI is working! 🚀", "status": "active"})

if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0', port=5000)
