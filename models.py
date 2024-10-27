from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

db = SQLAlchemy()

class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    module_code = db.Column(db.String(10), nullable=False)
    _deadline = db.Column('deadline', db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=False)
    is_complete = db.Column(db.Boolean, default=False)

    @property
    def deadline(self):
        """Getter for deadline."""
        return self._deadline
    
    @deadline.setter
    def deadline(self, value):
        """Setter for deadline that accepts both string and datetime object."""
        if isinstance(value, str):
            try:
                # Attempt to convert string to datetime
                self._deadline = datetime.strptime(value, '%Y-%m-%d')
            except ValueError:
                raise ValueError("Invalid date format. Expected 'YYYY-MM-DD'.")
        elif isinstance(value, (datetime, date)):
            self._deadline = value
        else:
            raise ValueError("Invalid format for deadline. Must be a string or datetime object.")
