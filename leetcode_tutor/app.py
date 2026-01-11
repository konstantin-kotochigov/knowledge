"""
Flask web application for LeetCode tutor
Shows 2 daily problems with collapsible hints and solutions
"""
import os
import random
from datetime import datetime, timedelta
from flask import Flask, render_template
from dotenv import load_dotenv
from models import init_db, get_db, Problem, DailyProblem

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')


def get_daily_problems():
    """
    Get 2 problems for today
    If problems for today already exist, return them
    Otherwise, select 2 new random problems with solutions and hints
    """
    db = get_db()
    today = datetime.utcnow().date()
    
    # Check if we already have daily problems for today
    daily_problems = db.query(DailyProblem).filter(
        DailyProblem.date >= datetime.combine(today, datetime.min.time())
    ).all()
    
    if daily_problems:
        # Return existing daily problems
        problem_ids = [dp.problem_id for dp in daily_problems]
        problems = db.query(Problem).filter(Problem.id.in_(problem_ids)).all()
        # Convert to dicts to avoid session issues
        result = [{
            'leetcode_id': p.leetcode_id,
            'title': p.title,
            'difficulty': p.difficulty,
            'description': p.description,
            'hint': p.hint,
            'solution': p.solution
        } for p in problems]
        db.close()
        return result
    
    # Select 2 new problems that have both hints and solutions
    available_problems = db.query(Problem).filter(
        Problem.has_solution == True,
        Problem.has_hint == True
    ).all()
    
    if len(available_problems) < 2:
        db.close()
        return []
    
    # Randomly select 2 problems
    selected = random.sample(available_problems, min(2, len(available_problems)))
    
    # Save as daily problems
    for problem in selected:
        daily_problem = DailyProblem(problem_id=problem.id)
        db.add(daily_problem)
    
    db.commit()
    
    # Convert to dicts to avoid session issues
    result = [{
        'leetcode_id': p.leetcode_id,
        'title': p.title,
        'difficulty': p.difficulty,
        'description': p.description,
        'hint': p.hint,
        'solution': p.solution
    } for p in selected]
    
    db.close()
    
    return result


@app.route('/')
def index():
    """Main page showing daily problems"""
    problems = get_daily_problems()
    current_date = datetime.utcnow().strftime('%d %B %Y')
    
    # Russian month names
    months = {
        'January': 'января', 'February': 'февраля', 'March': 'марта',
        'April': 'апреля', 'May': 'мая', 'June': 'июня',
        'July': 'июля', 'August': 'августа', 'September': 'сентября',
        'October': 'октября', 'November': 'ноября', 'December': 'декабря'
    }
    
    for eng, rus in months.items():
        current_date = current_date.replace(eng, rus)
    
    return render_template('index.html', problems=problems, date=current_date)


if __name__ == '__main__':
    init_db()
    port = int(os.getenv('FLASK_PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
