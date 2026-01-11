"""
LeetCode parser - fetches problems from LeetCode API
Rate limited to 10-20 requests per day
"""
import requests
import json
from datetime import datetime, timedelta
from models import get_db, Problem, RateLimit
import os
from dotenv import load_dotenv

load_dotenv()

LEETCODE_API_URL = "https://leetcode.com/api/problems/all/"
LEETCODE_GRAPHQL_URL = "https://leetcode.com/graphql"
PARSE_LIMIT = int(os.getenv('LEETCODE_PARSE_LIMIT', 20))


def check_rate_limit(db):
    """Check if we can make more requests today"""
    rate_limit = db.query(RateLimit).filter_by(service='leetcode_parser').first()
    
    if not rate_limit:
        # Create new rate limit entry
        rate_limit = RateLimit(service='leetcode_parser', count=0)
        db.add(rate_limit)
        db.commit()
        return True
    
    # Check if we need to reset (new day)
    if datetime.utcnow() - rate_limit.last_reset > timedelta(days=1):
        rate_limit.count = 0
        rate_limit.last_reset = datetime.utcnow()
        db.commit()
    
    return rate_limit.count < PARSE_LIMIT


def increment_rate_limit(db):
    """Increment the rate limit counter"""
    rate_limit = db.query(RateLimit).filter_by(service='leetcode_parser').first()
    if rate_limit:
        rate_limit.count += 1
        db.commit()


def fetch_problem_list():
    """Fetch list of all problems from LeetCode"""
    try:
        response = requests.get(LEETCODE_API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get('stat_status_pairs', [])
    except Exception as e:
        print(f"Error fetching problem list: {e}")
        return []


def fetch_problem_details(title_slug):
    """Fetch detailed information about a specific problem"""
    query = """
    query questionData($titleSlug: String!) {
        question(titleSlug: $titleSlug) {
            questionId
            title
            difficulty
            content
            topicTags {
                name
            }
        }
    }
    """
    
    variables = {"titleSlug": title_slug}
    
    try:
        response = requests.post(
            LEETCODE_GRAPHQL_URL,
            json={"query": query, "variables": variables},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        return data.get('data', {}).get('question')
    except Exception as e:
        print(f"Error fetching problem details for {title_slug}: {e}")
        return None


def parse_and_save_problems(limit=None):
    """
    Parse problems from LeetCode and save to database
    
    Args:
        limit: Maximum number of problems to parse in this run
    """
    db = get_db()
    
    # Check rate limit
    if not check_rate_limit(db):
        print("Rate limit reached for today")
        db.close()
        return
    
    # Get problem list
    problems = fetch_problem_list()
    if not problems:
        print("No problems fetched")
        db.close()
        return
    
    # Limit how many we parse
    if limit is None:
        limit = PARSE_LIMIT
    
    parsed_count = 0
    
    for item in problems:
        if parsed_count >= limit:
            break
        
        # Check rate limit before each request
        if not check_rate_limit(db):
            print(f"Rate limit reached. Parsed {parsed_count} problems.")
            break
        
        stat = item.get('stat', {})
        leetcode_id = stat.get('frontend_question_id')
        title_slug = stat.get('question__title_slug')
        
        # Skip if already in database
        existing = db.query(Problem).filter_by(leetcode_id=leetcode_id).first()
        if existing:
            continue
        
        # Fetch detailed information
        details = fetch_problem_details(title_slug)
        if not details:
            continue
        
        # Save to database
        problem = Problem(
            leetcode_id=leetcode_id,
            title=details.get('title', 'Unknown'),
            difficulty=details.get('difficulty', 'Unknown'),
            description=details.get('content', ''),
            has_solution=False,
            has_hint=False
        )
        
        db.add(problem)
        increment_rate_limit(db)
        parsed_count += 1
        
        print(f"Parsed problem {leetcode_id}: {problem.title}")
    
    db.commit()
    db.close()
    print(f"Successfully parsed {parsed_count} problems")


if __name__ == '__main__':
    from models import init_db
    init_db()
    parse_and_save_problems(limit=10)  # Parse 10 problems as test
