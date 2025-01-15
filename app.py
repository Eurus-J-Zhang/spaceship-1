from flask import Flask,render_template,url_for,request, redirect, send_from_directory, session
from flask_migrate import Migrate
from forms import EmotionForm
from forms import DemographicInfo
import os
import pymysql
from models import db, Data

pymysql.install_as_MySQLdb()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('JAWSDB_URL')
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SECRET_KEY'] = "iloveeurus"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app

app = create_app()

def handle_form_submission(form, session_key, next_page):
    if form.validate_on_submit():
        data = form.data
        data.pop('csrf_token', None)
        session[session_key] = data
        return redirect(next_page)
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    form = DemographicInfo()
    if form.validate_on_submit():
        data = form.data
        data.pop('csrf_token', None)
        session['index_data'] = data
        session['counter'] = 0
        return redirect(url_for('lock_info'))
    return render_template('index.html',form=form)

@app.route('/lock_choice', methods=['GET', 'POST'])
def handle_form():
    if request.method == 'POST':
        slot_choice = request.form.get('slotChoice')
        session['final_choice'] = slot_choice
        if slot_choice == 'B':
            return redirect(url_for('correct'))  # Redirect to the correct page
        elif slot_choice in ('A', 'C'):
            return redirect(url_for('wrong')) # Redirect to the wrong page
        else:
            return render_template('p4.html', error='Please select an option.') 
    return render_template('lock_choice.html')


@app.route('/emo', methods=['GET', 'POST'])
def emo():
    final_choice = session.get('final_choice', None)
    content = {
    'B': {'image_path': 'static/img/ring.jpg'},
    'A_C': {'image_path': 'static/img/alarm.jpg'}
    }
    chosen_content = content['B'] if final_choice == 'B' else content['A_C']
    
    form = EmotionForm()

    result = handle_form_submission(form, 'emo_data', 'end')
    if result:
        index_data = session.get('index_data')
        final_choice = session.get('final_choice')
        emo_data = session.get('emo_data')
        combined_data = {**index_data, 'final_choice': final_choice, **emo_data}
        data = Data(**combined_data)
        db.session.add(data)
        db.session.commit()
        return result
    return render_template('emo.html',form=form,chosen_content=chosen_content)


# P1
@app.route('/lock_info')
def lock_info():
    return render_template('lock_info.html')

# P2
@app.route('/livingroom')
def livingroom():
    return render_template('livingroom.html')

# P3
@app.route('/liv_choice')
def liv_choice():
    return render_template('liv_choice.html')

# P4
@app.route('/office')
def office():
    return render_template('office.html')


# livingroomA
@app.route('/livingroomA')
def livingroomA():
    return render_template('livingroomA.html')


# livingroomB
@app.route('/livingroomB')
def livingroomB():
    return render_template('livingroomB.html')

# livingroomC
@app.route('/livingroomC')
def livingroomC():
    return render_template('livingroomC.html')

# livingroomD
@app.route('/livingroomD')
def livingroomD():
    return render_template('livingroomD.html')

# r_correct
@app.route('/correct')
def correct():
    return render_template('correct.html')

# r_wrong
@app.route('/wrong')
def wrong():
    return render_template('wrong.html')

# end page
@app.route('/end')
def end():
    return render_template('end.html')

if __name__ == "__main__":
    app.run(debug=True)