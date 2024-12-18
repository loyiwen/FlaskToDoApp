import os
from flask import Flask, redirect, render_template, url_for, request, flash
from models import db, Assessment
from forms import AssessmentForm
from config import DevelopmentConfig, TestingConfig, ProductionConfig
from datetime import datetime

app = Flask(__name__)

if os.getenv("FLASK_ENV") == "testing" or os.getenv("TESTING") == "1":
    app.config.from_object(TestingConfig)
else:
    app.config.from_object(ProductionConfig)

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
            flash("Form validation failed. Please correct the errors and try again.", "danger")
            return render_template('create.html', form=form)

        # Check if date and time fields are fully populated
        if not form.date.data or not form.time.data:
            flash("Please enter a complete date and time.", "danger")
            return render_template('create.html', form=form)

        try:         
            # Combine date and time fields
            deadline = datetime.combine(form.date.data, form.time.data)
            
            new_assessment = Assessment(
                title=form.title.data,
                module_code=form.module_code.data,
                deadline=deadline,
                description=form.description.data,
                is_complete=False
            )
            
            db.session.add(new_assessment)
            db.session.commit()
            flash("Assessment created successfully.", "success")
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

    # Pre-fill the form with existing date and time
    if request.method == 'GET':
        form.date.data = assessment.deadline.date()
        form.time.data = assessment.deadline.time()

    if form.validate_on_submit():
        # Check if date and time fields are fully populated
        if not form.date.data or not form.time.data:
            flash("Please enter a complete date and time.", "danger")
            return render_template('create.html', form=form)
        
        assessment.title = form.title.data
        assessment.module_code = form.module_code.data
        # Combine the date and time fields
        assessment.deadline = datetime.combine(form.date.data, form.time.data)
        assessment.description = form.description.data
        db.session.commit()
        flash("Assessment updated successfully.", "success")
        return redirect(url_for('index'))
    
    return render_template('edit.html', form=form, assessment=assessment)

# Delete an assessment
@app.route('/delete/<int:id>', methods=['POST'])
def delete_assessment(id):
    assessment = Assessment.query.get_or_404(id)
    db.session.delete(assessment)
    db.session.commit()
    flash("Assessment deleted successfully.", "success")
    return redirect(url_for('index'))

# Toggle completion status
@app.route('/toggle_complete/<int:id>', methods=['POST'])
def toggle_completion(id):
    assessment = Assessment.query.get_or_404(id)
    assessment.is_complete = not assessment.is_complete
    db.session.commit()
    status = "completed" if assessment.is_complete else "marked as incomplete"
    flash(f"Assessment {status}.", "info")
    return redirect(url_for('index'))

# View only completed assessments
@app.route('/completed')
def completed():
    assessments = Assessment.query.filter_by(is_complete=True).all()
    return render_template('index.html', assessments=assessments, filter='Completed')

# View only uncompleted assessments
@app.route('/uncomplete')
def uncomplete():
    assessments = Assessment.query.filter_by(is_complete=False).all()
    return render_template('index.html', assessments=assessments, filter='Uncompleted')

if __name__ == '__main__':
    app.run(debug=True)
