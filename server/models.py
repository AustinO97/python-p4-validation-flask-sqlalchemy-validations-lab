from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_author(self, key, name):
        if not name:
            raise ValueError('Author must have a name!')
        author = db.session.query(Author.id).filter(Author.name == name).first()
        if author is not None:
            raise ValueError('Author must be unique.')
        return name

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if len(phone_number) != 10 or not phone_number.isdigit():
            raise ValueError('Phone number must be exactly 10 digits.')
        return phone_number
    
    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError('Content must be at least 250 characters long.')
        return content
    
    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError('Summary has a maximum of 250 characters.')
        return summary
    
    @validates('category')
    def validates_category(self, key, category):
        if not category == 'Fiction' and not category == 'Non-Fiction':
            raise ValueError('Category must be either Fiction or Non-Fiction.')
        return category
    
    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError('Must have a title.')
        titles = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(string in title for string in titles):
            raise ValueError('Title must be a clickbait-y title')
        return title



    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
