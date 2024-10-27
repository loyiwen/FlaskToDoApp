from flask import Flask, redirect, render_template, url_for, request
from models import db, Assessment
from forms import AssessmentForm
from config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    assessments = Assessment.query.all()
    return render_template('index.html', assessments=assessments)

# Create new assessment
@app.route('/create', methods=['GET', 'POST'])
def create():
    form = AssessmentForm()

    if request.method == 'POST':
        # If form validation fails, log errors and return the form with errors
        if not form.validate_on_submit():
            print("Form validation failed. Errors:", form.errors)
            return render_template('create.html', form=form)
        
        try:
            new_assessment = Assessment(
                title=form.title.data,
                module_code=form.module_code.data,
                deadline=form.deadline.data,
                description=form.description.data,
                is_complete=form.is_complete.data
            )
            db.session.add(new_assessment)
            db.session.commit()
            return redirect(url_for('index'))
        
        except Exception as e:
            db.session.rollback()
            print("Database commit failed:", e)
            return render_template('create.html', form=form)
    else:
        # If GET request, just render the empty form
        return render_template('create.html', form=form)
    
# Edit an existing assessment
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    assessment = Assessment.query.get_or_404(id)
    form = AssessmentForm(obj=assessment)
    if form.validate_on_submit():
        assessment.title = form.title.data
        assessment.module_code = form.module_code.data
        assessment.deadline = form.deadline.data
        assessment.description = form.description.data
        assessment.is_complete = form.is_complete.data
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', form=form, assessment=assessment)

if __name__ == '__main__':
    app.run(debug=True)