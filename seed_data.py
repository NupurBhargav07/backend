from app import create_app
from app.models import db, Question, Option, QuestionFlow

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    question_data = [
        ("What is your age?", "numeric"),
        ("What is your gender?", "multiple_choice"),
        ("Do you experience prostate issues?", "boolean"),
        ("Do you have any allergies?", "boolean"),
        ("Preferred contact method?", "multiple_choice"),
        ("Do you smoke?", "boolean"),
        ("What’s your marital status?", "multiple_choice"),
        ("Do you exercise regularly?", "boolean"),
        ("Do you wear glasses?", "boolean"),
        ("Enter your height in cm.", "numeric"),
        ("Enter your weight in kg.", "numeric"),
        ("Are you on any medications?", "boolean"),
        ("Do you have a balanced diet?", "boolean"),
        ("Do you have any chronic illness?", "boolean"),
        ("How often do you consume alcohol?", "multiple_choice"),
        ("How often do you feel stressed?", "multiple_choice"),
        ("Do you undergo regular health checkups?", "boolean"),
        ("How many hours do you work per day?", "numeric"),
        ("Do you use digital screens for more than 5 hours daily?", "boolean"),

        # 🆕 New questions
        ("What is your blood type?", "multiple_choice"),
        ("Do you follow a vegetarian diet?", "boolean"),
        ("How often do you travel?", "multiple_choice"),
        ("Do you have a family history of genetic disorders?", "boolean"),
        ("How would you rate your mental well-being?", "multiple_choice"),
    ]

    questions = []

    for text, q_type in question_data:
        q = Question(text=text, type=q_type, is_required=True)
        db.session.add(q)
        questions.append(q)

    db.session.commit()

    multi_choice_options = {
        "What is your gender?": ["Male", "Female", "Other"],
        "Preferred contact method?": ["Email", "Phone", "SMS"],
        "What’s your marital status?": ["Single", "Married", "Divorced"],
        "How often do you consume alcohol?": ["Never", "Occasionally", "Frequently"],
        "How often do you feel stressed?": ["Rarely", "Sometimes", "Often", "Always"],
        "What is your blood type?": ["A", "B", "AB", "O"],
        "How often do you travel?": ["Rarely", "Sometimes", "Frequently"],
        "How would you rate your mental well-being?": ["Poor", "Fair", "Good", "Excellent"],
    }

    for q in questions:
        if q.type == "multiple_choice":
            for opt in multi_choice_options.get(q.text, ["Option A", "Option B"]):
                db.session.add(Option(question_id=q.id, text=opt))

    db.session.commit()

    flows = [
        (questions[0].id, ">=18", questions[1].id),

        (questions[1].id, "Male", questions[2].id),
        (questions[1].id, "Female", questions[3].id),
        (questions[1].id, "Other", questions[3].id),

        (questions[2].id, "Yes", questions[3].id),
        (questions[2].id, "No", questions[3].id),

        (questions[3].id, "Yes", questions[4].id),
        (questions[3].id, "No", questions[4].id),

        (questions[4].id, "Email", questions[5].id),
        (questions[4].id, "Phone", questions[5].id),
        (questions[4].id, "SMS", questions[5].id),

        (questions[5].id, "Yes", questions[6].id),
        (questions[5].id, "No", questions[6].id),

        (questions[6].id, "Single", questions[7].id),
        (questions[6].id, "Married", questions[7].id),
        (questions[6].id, "Divorced", questions[7].id),

        (questions[7].id, "Yes", questions[8].id),
        (questions[7].id, "No", questions[8].id),

        (questions[8].id, "Yes", questions[9].id),
        (questions[8].id, "No", questions[9].id),

        (questions[9].id, ">=150", questions[10].id),
        (questions[10].id, ">=50", questions[11].id),

        (questions[11].id, "Yes", questions[12].id),
        (questions[11].id, "No", questions[12].id),

        (questions[12].id, "Yes", questions[13].id),
        (questions[12].id, "No", questions[13].id),

        (questions[13].id, "Yes", questions[14].id),
        (questions[13].id, "No", questions[14].id),

        (questions[14].id, "Frequently", questions[15].id),
        (questions[14].id, "Occasionally", questions[15].id),
        (questions[14].id, "Never", questions[15].id),

        (questions[15].id, "Often", questions[16].id),
        (questions[15].id, "Always", questions[16].id),
        (questions[15].id, "Sometimes", questions[16].id),
        (questions[15].id, "Rarely", questions[16].id),

        (questions[16].id, "Yes", questions[17].id),
        (questions[16].id, "No", questions[17].id),

        (questions[17].id, ">=8", questions[18].id),
        (questions[17].id, "<8", questions[18].id),

        (questions[18].id, "Yes", questions[19].id),
        (questions[18].id, "No", questions[19].id),

        (questions[19].id, "A", questions[20].id),
        (questions[19].id, "B", questions[20].id),
        (questions[19].id, "AB", questions[20].id),
        (questions[19].id, "O", questions[20].id),

        (questions[20].id, "Yes", questions[21].id),
        (questions[20].id, "No", questions[21].id),

        (questions[21].id, "Rarely", questions[22].id),
        (questions[21].id, "Sometimes", questions[22].id),
        (questions[21].id, "Frequently", questions[22].id),

        (questions[22].id, "Yes", questions[23].id),
        (questions[22].id, "No", questions[23].id),
    ]

    for current_id, expected_answer, next_id in flows:
        db.session.add(QuestionFlow(
            current_question_id=current_id,
            expected_answer=expected_answer,
            next_question_id=next_id
        ))

    db.session.commit()

    print("Questionnaire seeded successfully.")
