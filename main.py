from flask import Flask, render_template, redirect, url_for, flash
from forms import SearchForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'cacc1e303ec4e2c891af9883df1df9b1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DrawingLogDB.db'

db  = SQLAlchemy(app)

class Projects(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String())
    sheets = db.relationship('Sheets', backref='project', lazy='dynamic')

    def __repr__(self):
        return f'Project ({self.id}, {self.project_name})'


class Sheets(db.Model):
    __tablename__ = 'sheets'
    sheet_num = db.Column(db.String(), primary_key=True)
    sheet_name = db.Column(db.String())
    current_rev = db.Column(db.String(), primary_key=True)
    current_rev_date = db.Column(db.String())
    current_rev_desc = db.Column(db.String())
    current_rev_by = db.Column(db.String())
    sheet_type = db.Column(db.String())
    eng_pc = db.Column(db.String())
    model_pc = db.Column(db.String())
    coordination_pc = db.Column(db.String())
    drawing_pc = db.Column(db.String())
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))

    def __repr__(self):
        return f'Sheet ({self.project_id}, {self.sheet_num}, {self.sheet_name}, {self.current_rev}, {self.current_rev_desc}, {self.current_rev_date}'


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = SearchForm()
    if form.validate_on_submit():
        project = Projects.query.filter_by(id=form.project_num.data).first()
        if project:
            return redirect(url_for('project', project_num=project.id))
        else:
            flash('That project number was not found', 'danger')
    return render_template('home.html', form=form)

@app.route('/<int:project_num>')
@app.route('/<int:project_num>/<string:sheet_type>')
def project(project_num, sheet_type=None):
    drawings_for_dropdown = Sheets.query.filter_by(project_id=project_num)
    if sheet_type:
        drawings_for_table = Sheets.query.filter_by(project_id=project_num, sheet_type=sheet_type)
        sheet_filter_applied = True
    else:
        drawings_for_table = Sheets.query.filter_by(project_id=project_num)
        sheet_filter_applied = False
    sheet_types = drawings_for_dropdown.with_entities(Sheets.sheet_type).distinct()
    project = Projects.query.filter_by(id=project_num).first()
    return render_template('project.html', drawings=drawings_for_table, title=project_num, sheet_types=sheet_types, project_num=project_num, project_name=project.project_name, sheet_filter_applied=sheet_filter_applied)

if __name__ == '__main__':
    app.run(debug=True)