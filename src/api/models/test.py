from flask import Blueprint, jsonify, request, render_template, session
from src.db.core import db
from src.db.models.quiz_db import Questions, Answers, Options, Response

test_bp = Blueprint('test', __name__)
@test_bp.route('/test/view', methods=['GET'])
def test_view():
    return render_template('test.html')

@test_bp.route('/test', methods=['GET', 'POST'])
def test_question():
    '''view test questions'''
    if request.method == 'GET':
        # fetch question 1-70 from the database
        question_ids = [q.question_id for q in Questions.query.filter(Questions.question_no.between(1,70)).all()]
        all_correct_answers = {a.question_id: a.correct_answer for a in Answers.query.filter(Answers.question_id.in_(question_ids)).all()}       
        test_questions = Questions.query.filter(Questions.question_no.between(1, 70)).all()
        if not test_questions:
            return jsonify({'error': 'No test questions found'}), 404
        
        result = []
        for question in test_questions:
            # get options for each question
            options = Options.query.filter_by(question_id=question.question_id).all()
            options_list =[{'label': opt.label, 'text': opt.text} for opt in options]
            question_data = {
                'question_no': question.question_no,
                'question': question.question,
                'options': options_list
            }
            result.append(question_data)
        
        return jsonify(result), 200
        
    elif request.method == 'POST':
    # for test submission
        data = request.get_json()
        user_answers = data.get('answers', {})
        score = 0 
        total_questions = 70
        results = []

    # loop through question 1-5
    for question_no in range(1, 71):
        question = Questions.query.filter_by(question_no=question_no).first()
        if not question:
            return jsonify({'error': f'Question {question_no} not found'}), 404
        if question:
            # get correct answer
            correct_answer = Answers.query.filter_by(question_id=question.question_id).first()
            user_ans = user_answers.get(str(question_no))
            # Convert both answers to lowercase and strip whitespace
            user_ans_clean = user_ans.strip().lower() if user_ans else None
            correct_ans_clean = correct_answer.correct_answer.strip().lower() if correct_answer else None
            is_correct = (user_ans_clean == correct_ans_clean)
            if is_correct:
                score += 1
            results.append({
                "question_no": question_no,
                "question": question.question,
                "user_answer": user_ans,
                "correct_answer": correct_answer.correct_answer if correct_answer else None,
                "is_correct": is_correct
            })

    return jsonify({
        "score": score,
        "total": total_questions,
        "percentage": (score / total_questions) * 100 if total_questions > 0 else 0,
        "results": results
    }), 200