"""
Test script to add sample problems to database
"""
from models import init_db, get_db, Problem

def add_sample_problems():
    """Add sample problems for testing"""
    init_db()
    db = get_db()
    
    # Sample problem 1
    problem1 = Problem(
        leetcode_id=1,
        title="Two Sum",
        difficulty="Easy",
        description="""
        <p>Given an array of integers <code>nums</code> and an integer <code>target</code>, 
        return <em>indices of the two numbers such that they add up to <code>target</code></em>.</p>
        
        <p>You may assume that each input would have <strong>exactly one solution</strong>, 
        and you may not use the <em>same</em> element twice.</p>
        
        <p><strong>Example 1:</strong></p>
        <pre>
        <strong>Input:</strong> nums = [2,7,11,15], target = 9
        <strong>Output:</strong> [0,1]
        <strong>Explanation:</strong> Because nums[0] + nums[1] == 9, we return [0, 1].
        </pre>
        """,
        hint="Используйте хэш-таблицу для хранения чисел, которые вы уже видели. Для каждого числа проверяйте, существует ли его дополнение (target - число) в хэш-таблице.",
        solution="""
        <h3>Решение с использованием хэш-таблицы</h3>
        <p>Оптимальное решение использует словарь для хранения уже просмотренных чисел.</p>
        
        <pre><code class="python">
def twoSum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
        </code></pre>
        
        <p><strong>Сложность:</strong></p>
        <ul>
            <li>Время: O(n) - один проход по массиву</li>
            <li>Память: O(n) - для хэш-таблицы</li>
        </ul>
        """,
        has_hint=True,
        has_solution=True
    )
    
    # Sample problem 2
    problem2 = Problem(
        leetcode_id=2,
        title="Add Two Numbers",
        difficulty="Medium",
        description="""
        <p>You are given two <strong>non-empty</strong> linked lists representing two non-negative integers. 
        The digits are stored in <strong>reverse order</strong>, and each of their nodes contains a single digit. 
        Add the two numbers and return the sum as a linked list.</p>
        
        <p><strong>Example:</strong></p>
        <pre>
        <strong>Input:</strong> l1 = [2,4,3], l2 = [5,6,4]
        <strong>Output:</strong> [7,0,8]
        <strong>Explanation:</strong> 342 + 465 = 807.
        </pre>
        """,
        hint="Проходите по обоим спискам одновременно, складывая соответствующие цифры. Не забудьте обрабатывать перенос (carry) на следующий разряд.",
        solution="""
        <h3>Решение с обработкой переноса</h3>
        <p>Проходим по обоим связным спискам, складывая узлы и обрабатывая перенос.</p>
        
        <pre><code class="python">
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def addTwoNumbers(l1, l2):
    dummy = ListNode(0)
    current = dummy
    carry = 0
    
    while l1 or l2 or carry:
        val1 = l1.val if l1 else 0
        val2 = l2.val if l2 else 0
        
        total = val1 + val2 + carry
        carry = total // 10
        current.next = ListNode(total % 10)
        current = current.next
        
        if l1: l1 = l1.next
        if l2: l2 = l2.next
    
    return dummy.next
        </code></pre>
        
        <p><strong>Сложность:</strong></p>
        <ul>
            <li>Время: O(max(m, n)) - где m и n длины списков</li>
            <li>Память: O(max(m, n)) - для результирующего списка</li>
        </ul>
        """,
        has_hint=True,
        has_solution=True
    )
    
    # Check if problems already exist
    existing1 = db.query(Problem).filter_by(leetcode_id=1).first()
    existing2 = db.query(Problem).filter_by(leetcode_id=2).first()
    
    if not existing1:
        db.add(problem1)
        print("Added problem 1: Two Sum")
    else:
        print("Problem 1 already exists")
    
    if not existing2:
        db.add(problem2)
        print("Added problem 2: Add Two Numbers")
    else:
        print("Problem 2 already exists")
    
    db.commit()
    db.close()
    print("Sample data added successfully!")


if __name__ == '__main__':
    add_sample_problems()
