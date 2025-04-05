from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    answers = db.relationship('Answer', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    is_required = db.Column(db.Boolean, default=True)

    options = db.relationship('Option', backref='question', lazy=True)
    flows_from = db.relationship('QuestionFlow', foreign_keys='QuestionFlow.current_question_id', backref='current_question', lazy=True)
    flows_to = db.relationship('QuestionFlow', foreign_keys='QuestionFlow.next_question_id', backref='next_question', lazy=True)

    def __repr__(self):
        return f'<Question {self.text[:30]}>'


class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    text = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Option {self.text}>'


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    response = db.Column(db.Text)

    question = db.relationship('Question', backref='answers')

    def __repr__(self):
        return f'<Answer Q{self.question_id} - User {self.user_id}>'


class QuestionFlow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    current_question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    expected_answer = db.Column(db.String(255))
    next_question_id = db.Column(db.Integer, db.ForeignKey('question.id'))

    def __repr__(self):
        return f'<Flow Q{self.current_question_id} → Q{self.next_question_id} if "{self.expected_answer}">'
