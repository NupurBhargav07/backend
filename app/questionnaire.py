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

    existing_answer = Answer.query.filter_by(user_id=user_id, question_id=data["question_id"]).first()
    if existing_answer:
        existing_answer.response = data["response"]
        msg = "Answer updated successfully"
    else:
        new_answer = Answer(user_id=user_id, question_id=data["question_id"], response=data["response"])
        db.session.add(new_answer)
        msg = "Answer saved successfully"

    db.session.commit()
    return jsonify({"msg": msg}), 201



@questionnaire_bp.route("/next", methods=["POST"])
@jwt_required()
def get_next_question():
    data = request.get_json()
    current_question_id = data.get("current_question_id")
    answer = data.get("answer")

    if not current_question_id or not answer:
        return jsonify({"msg": "Missing current_question_id or answer"}), 400

    flows = QuestionFlow.query.filter_by(current_question_id=current_question_id, expected_answer=answer).all()

    if not flows:
        return jsonify({"msg": "No matching next question found"}), 404

    result = []
    for flow in flows:
        q = Question.query.get(flow.next_question_id)
        if q:
            result.append({
                "id": q.id,
                "text": q.text,
                "type": q.type,
                "is_required": q.is_required,
                "options": [{"id": o.id, "text": o.text} for o in q.options]
            })

    return jsonify(result)


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


@questionnaire_bp.route("/total", methods=["GET"])
@jwt_required()
def get_total_questions():
    total = Question.query.count()
    return jsonify({"total": total})


@questionnaire_bp.route("/create-question", methods=["POST"])
def create_question():
    data = request.get_json()
    text = data.get("text")
    q_type = data.get("type")  # e.g., 'text', 'multiple_choice'
    is_required = data.get("is_required", True)
    options = data.get("options", [])

    if not text or not q_type:
        return jsonify({"msg": "Missing required fields"}), 400

    question = Question(text=text, type=q_type, is_required=is_required)
    db.session.add(question)
    db.session.flush()  # Get question.id before commit

    if q_type == "multiple_choice":
        for opt in options:
            db.session.add(Option(text=opt, question_id=question.id))

    db.session.commit()
    return jsonify({"msg": "Question created", "id": question.id}), 201


@questionnaire_bp.route("/create-flow", methods=["POST"])
def create_flow():
    data = request.get_json()
    current_id = data.get("current_question_id")
    expected_answer = data.get("expected_answer")
    next_id = data.get("next_question_id")

    if not current_id or expected_answer is None or not next_id:
        return jsonify({"msg": "Missing required fields"}), 400

    flow = QuestionFlow(
        current_question_id=current_id,
        expected_answer=expected_answer,
        next_question_id=next_id
    )
    db.session.add(flow)
    db.session.commit()
    return jsonify({"msg": "Flow created"}), 201
