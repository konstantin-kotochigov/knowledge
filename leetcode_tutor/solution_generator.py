"""
Background worker for generating solutions and hints using LLM
Rate limited to 10 requests per day
"""
import os
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
from openai import OpenAI
from models import get_db, Problem, RateLimit

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
GENERATION_LIMIT = int(os.getenv('LLM_GENERATION_LIMIT', 10))


def check_rate_limit(db):
    """Check if we can make more LLM requests today"""
    rate_limit = db.query(RateLimit).filter_by(service='llm_generator').first()
    
    if not rate_limit:
        # Create new rate limit entry
        rate_limit = RateLimit(service='llm_generator', count=0)
        db.add(rate_limit)
        db.commit()
        return True
    
    # Check if we need to reset (new day)
    if datetime.utcnow() - rate_limit.last_reset > timedelta(days=1):
        rate_limit.count = 0
        rate_limit.last_reset = datetime.utcnow()
        db.commit()
    
    return rate_limit.count < GENERATION_LIMIT


def increment_rate_limit(db):
    """Increment the rate limit counter"""
    rate_limit = db.query(RateLimit).filter_by(service='llm_generator').first()
    if rate_limit:
        rate_limit.count += 1
        db.commit()


def generate_hint(problem_description, problem_title):
    """Generate a hint for a problem using LLM"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful coding tutor. Generate a brief hint (2-3 sentences) that guides the student toward the solution without giving it away completely. Write in Russian."},
                {"role": "user", "content": f"Problem: {problem_title}\n\n{problem_description}\n\nProvide a helpful hint:"}
            ],
            max_tokens=200,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating hint: {e}")
        return None


def generate_solution(problem_description, problem_title):
    """Generate a solution for a problem using LLM"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert programmer. Provide a clear, well-commented solution in Python with explanation. Write in Russian."},
                {"role": "user", "content": f"Problem: {problem_title}\n\n{problem_description}\n\nProvide a complete solution with explanation:"}
            ],
            max_tokens=800,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating solution: {e}")
        return None


def process_problems():
    """
    Background process to generate hints and solutions for problems
    Rate limited to GENERATION_LIMIT requests per day
    """
    db = get_db()
    
    # Check rate limit
    if not check_rate_limit(db):
        print("Rate limit reached for today")
        db.close()
        return
    
    # Find problems without solutions or hints
    problems = db.query(Problem).filter(
        (Problem.has_solution == False) | (Problem.has_hint == False)
    ).limit(GENERATION_LIMIT).all()
    
    if not problems:
        print("No problems need processing")
        db.close()
        return
    
    processed_count = 0
    
    for problem in problems:
        if not check_rate_limit(db):
            print(f"Rate limit reached. Processed {processed_count} problems.")
            break
        
        print(f"Processing problem {problem.leetcode_id}: {problem.title}")
        
        # Generate hint if missing
        if not problem.has_hint:
            hint = generate_hint(problem.description, problem.title)
            if hint:
                problem.hint = hint
                problem.has_hint = True
                increment_rate_limit(db)
                processed_count += 1
                print(f"  Generated hint")
                
                if not check_rate_limit(db):
                    db.commit()
                    break
        
        # Generate solution if missing
        if not problem.has_solution:
            solution = generate_solution(problem.description, problem.title)
            if solution:
                problem.solution = solution
                problem.has_solution = True
                increment_rate_limit(db)
                processed_count += 1
                print(f"  Generated solution")
        
        db.commit()
        
        # Small delay between requests
        time.sleep(1)
    
    db.close()
    print(f"Successfully processed {processed_count} items")


if __name__ == '__main__':
    from models import init_db
    init_db()
    process_problems()
