from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Question, Option, Answer, QuestionFlow, User

questionnaire_bp = Blueprint('questionnaire', __name__, url_prefix="/questionnaire")

@questionnaire_bp.route("/questions", methods=["GET"])
@jwt_required()
def get_initial_questions():
    questions = Question.query.limit(2).all()
    if not questions:
        return jsonify({"msg": "No questions found"}), 404

    result = []
    for q in questions:
        result.append({
            "id": q.id,
            "text": q.text,
            "type": q.type,
            "is_required": q.is_required,
            "options": [{"id": o.id, "text": o.text} for o in q.options]
        })
    return jsonify(result)


@questionnaire_bp.route("/answers", methods=["POST"])
@jwt_required()
def submit_answer():
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data or not data.get("question_id") or not data.get("response"):
        return jsonify({"msg": "Invalid data"}), 400

    question = Question.query.get(data["question_id"])
    if not question:
        return jsonify({"msg": "Question not found"}), 404

    answer = Answer(user_id=user_id, question_id=data["question_id"], response=data["response"])
    db.session.add(answer)
    db.session.commit()

    return jsonify({"msg": "Answer saved successfully"}), 201


@questionnaire_bp.route("/next", methods=["POST"])
@jwt_required()
def get_next_question():
    data = request.get_json()
    current_question_id = data.get("current_question_id")
    answer = data.get("answer")

    if not current_question_id or not answer:
        return jsonify({"msg": "Missing current_question_id or answer"}), 400

    flow = QuestionFlow.query.filter_by(current_question_id=current_question_id, expected_answer=answer).first()

    if not flow:
        return jsonify({"msg": "No matching next question found"}), 404

    q = Question.query.get(flow.next_question_id)
    if not q:
        return jsonify({"msg": "Next question data not found"}), 404

    return jsonify({
        "id": q.id,
        "text": q.text,
        "type": q.type,
        "is_required": q.is_required,
        "options": [{"id": o.id, "text": o.text} for o in q.options]
    })


@questionnaire_bp.route("/summary", methods=["GET"])
@jwt_required()
def summary():
    user_id = get_jwt_identity()
    answers = Answer.query.filter_by(user_id=user_id).all()

    if not answers:
        return jsonify({"msg": "No answers submitted yet"}), 404

    result = []
    for a in answers:
        result.append({
            "question": a.question.text,
            "answer": a.response
        })
    return jsonify(result)
