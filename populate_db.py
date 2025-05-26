from src.app import app
from src.db.core import db
from src.db.models.quiz_db import Questions, Options, Answers
from src.db.models.quiz_questions import quiz_questions

# Dictionary of correct answers for each question
answer_key = {
    1: "c", 2: "c", 3: "b", 4: "a", 5: "a", 6: "d", 7: "a", 8: "b", 9: "c", 10: "b",
    11: "d", 12: "b", 13: "b", 14: "d", 15: "b", 16: "d", 17: "b", 18: "d", 19: "b", 20: "c",
    21: "b", 22: "d", 23: "c", 24: "c", 25: "c", 26: "d", 27: "d", 28: "b", 29: "b", 30: "d",
    31: "d", 32: "a", 33: "b", 34: "d", 35: "c", 36: "b", 37: "b", 38: "c", 39: "b", 40: "b",
    41: "c", 42: "b", 43: "b", 44: "c", 45: "a", 46: "d", 47: "c", 48: "b", 49: "b", 50: "b",
    51: "c", 52: "a", 53: "b", 54: "b", 55: "b", 56: "b", 57: "b", 58: "b", 59: "b", 60: "d",
    61: "b", 62: "a", 63: "c", 64: "b", 65: "c", 66: "b", 67: "d", 68: "a", 69: "a", 70: "b",
    71: "b", 72: "a", 73: "c", 74: "b", 75: "b", 76: "b", 77: "b", 78: "c", 79: "a", 80: "a",
    81: "b", 82: "b", 83: "c", 84: "c", 85: "c", 86: "b", 87: "a", 88: "b", 89: "a", 90: "a",
    91: "c", 92: "a", 93: "d", 94: "b", 95: "b", 96: "b", 97: "c", 98: "c", 99: "b"
}

with app.app_context(): 
    # Add each question from quiz_questions
    for q in quiz_questions:
        question = Questions(question_no=q["question_no"], question=q["question"])
        db.session.add(question)
        db.session.commit()  # Commit to get question_id
        
        # Add options for this question
        for opt in q["options"]:
            option = Options(
                question_id=question.question_id,
                label=opt["label"],
                text=opt["text"]
            )
            db.session.add(option)
        db.session.commit()
        
        # Add correct answer for this question
        correct_label = answer_key.get(q["question_no"])
        if correct_label:
            answer = Answers(
                question_id=question.question_id,
                correct_answer=correct_label
            )
            db.session.add(answer)
            db.session.commit()

