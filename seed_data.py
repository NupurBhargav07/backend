from app import create_app
from app.models import db, Question, Option, QuestionFlow

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    question_data = [
        ("What is your full name?", "text"),
        ("What is your age?", "numeric"),
        ("What is your gender?", "multiple_choice"),
        ("Do you have any allergies?", "boolean"),
        ("Select your preferred contact method.", "multiple_choice"),
        ("What is your date of birth?", "date"),
        ("Do you smoke?", "boolean"),
        ("How many hours do you sleep?", "numeric"),
        ("What’s your marital status?", "multiple_choice"),
        ("Describe your daily routine.", "text"),
        ("Are you currently employed?", "boolean"),
        ("What is your annual income?", "numeric"),
        ("What’s your highest qualification?", "multiple_choice"),
        ("How often do you exercise?", "multiple_choice"),
        ("What is your blood group?", "text"),
        ("Do you wear glasses?", "boolean"),
        ("Enter your height in cm.", "numeric"),
        ("Enter your weight in kg.", "numeric"),
        ("What languages do you speak?", "text"),
        ("Are you taking any medications?", "boolean"),
    ]

    extra_question_data = [
        ("What grade are you in?", "text"),
        ("Are you pregnant?", "boolean"),
        ("Do you experience prostate issues?", "boolean"),
        ("Do you have any specific health concerns?", "text"),
    ]

    questions = []

    for text, q_type in question_data + extra_question_data:
        q = Question(text=text, type=q_type, is_required=True)
        db.session.add(q)
        questions.append(q)

    db.session.commit()

    for q in questions:
        if q.type == "multiple_choice":
            sample_options = {
                "What is your gender?": ["Male", "Female", "Other"],
                "Select your preferred contact method.": ["Email", "Phone", "SMS"],
                "What’s your marital status?": ["Single", "Married", "Divorced"],
                "What’s your highest qualification?": ["High School", "Bachelor’s", "Master’s", "PhD"],
                "How often do you exercise?": ["Never", "Sometimes", "Regularly"]
            }
            for option_text in sample_options.get(q.text, ["Option A", "Option B"]):
                db.session.add(Option(question_id=q.id, text=option_text))

    db.session.commit()

    flows = [
        (1, "Nupur", 2),
        (2, "15", 21),
        (2, "25", 3),

        (3, "Female", 22),
        (3, "Male", 23),
        (3, "Other", 24),

        (22, "No", 4),
        (23, "No", 4),
        (24, "None", 4),

        (4, "Yes", 5),
        (5, "Email", 6),
        (6, "1995-05-25", 7),
        (7, "No", 8),
        (8, "8", 9),
        (9, "Single", 10),
        (10, "Busy", 11),
        (11, "Yes", 12),
        (12, "50000", 13),
        (13, "Bachelor’s", 14),
        (14, "Sometimes", 15),
        (15, "B+", 16),
        (16, "Yes", 17),
        (17, "170", 18),
        (18, "65", 19),
        (19, "English, Hindi", 20),
        (20, "No", None)  # End
    ]

    for current_id, expected_answer, next_id in flows:
        db.session.add(QuestionFlow(
            current_question_id=current_id,
            expected_answer=expected_answer,
            next_question_id=next_id
        ))

    db.session.commit()

    print("✅ Seeded 24 questions with diverse types and conditional flows.")
