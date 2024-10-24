from flask import Flask, render_template, request
from config import DevelopmentConfig
from forms import AssessmentForm
from models import db, Assessment

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# Initialise SQLAlchemy with app
db.init_app(app)

@app.route('/')
def index():
    return "Home Page Text"

# Create new assessment (handle GET and POST requests)
@app.route('/create', methods=['GET', 'POST'])
def create():
    form = AssessmentForm()

    if request.method == 'POST':
        # If form validation fails, log errors and return the form with errors
        if not form.validate_on_submit():
            print("Form validation failed. Errors:", form.errors)
            return render_template('create.html', form=form)
        
        new_assessment = Assessment(
            title=form.title.data,
            module_code=form.module_code.data,
            deadline=form.deadline.data,
            description=form.description.data,
            is_complete=form.is_complete.data
        )
        db.session.add(new_assessment)
        db.session.commit() 
        return "Assessment Created", 200  # Simple success message for test verification

    # If GET request, just render the empty form
    return render_template('create.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
