import json
import uuid
import logging
import datetime

from models.database import db
from models.Hardware import Hardware
from models.User import User
from models.UsageLog import UsageLog

from services.BarService import BarService
from services.UsageLogService import UsageLogService
from services.IndexService import IndexService

from authlib.integrations.flask_client import OAuth
from flask import Flask, request, session, render_template, url_for, redirect

with open('config.json', 'r') as file:
    config = json.load(file)

app = Flask(__name__)
app.secret_key = uuid.uuid4().hex
oauth = OAuth(app)
oauth.register(
    **config['OAuth']
)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

logging.basicConfig(filename='./logs/app.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

with app.app_context():
    db.create_all()
    for machine, gpus in config['Hardware'].items():
        for gpu in gpus:
            if db.session.query(Hardware).filter_by(machine=machine, gpu=gpu).first() is None:
                db.session.add(Hardware(id=uuid.uuid4().hex, machine=machine, gpu=gpu))
        db.session.commit()


@app.errorhandler(Exception)
def page_not_found(error):
    ncu_protal = None if 'ncu_protal' not in session else session['ncu_protal']
    bar_service = BarService(ncu_protal)
    app.logger.error(str(error))
    return render_template(
        '404.html',
        bar_service=bar_service,
    ), 404


@app.route('/', methods=['GET'])
def index_page():
    ncu_protal = None if 'ncu_protal' not in session else session['ncu_protal']
    bar_service = BarService(ncu_protal)
    index_service = IndexService()
    return render_template(
        'index.html',
        bar_service=bar_service,
        index_service=index_service
    )


@app.route('/tables/<hardware_id>', methods=['GET'])
def tables_page(hardware_id):
    ncu_protal = None if 'ncu_protal' not in session else session['ncu_protal']
    bar_service = BarService(ncu_protal)
    usage_log_service = UsageLogService(request.args['year'], request.args['week'], hardware_id)
    return render_template(
        'tables.html',
        bar_service=bar_service,
        current_hardware_id=hardware_id,
        usage_log_service=usage_log_service
    )


@app.route('/apply', methods=['GET'])
def apply_page():
    if 'ncu_protal' not in session:
        return redirect(url_for('login'))
    ncu_protal = session['ncu_protal']
    bar_service = BarService(ncu_protal)
    return render_template(
        'apply.html',
        bar_service=bar_service,
    )


@app.route('/apply', methods=['POST'])
def record_apply_form():
    user = User.query.filter_by(token=session['ncu_protal']).first()
    user_id = user.id
    data = request.json
    start_date = datetime.datetime.strptime(data['startTime'], "%Y-%m-%d")
    end_date = datetime.datetime.strptime(data['endTime'], "%Y-%m-%d")
    start_time_period, end_time_period = int(data['startTimeSelect']), int(data['endTimeSelect'])
    hardware_id = data['gpuSelect']

    if start_date == end_date:
        for hour in range(start_time_period, end_time_period):
            db.session.add(UsageLog(user_id=user_id, hardware_id=hardware_id, date=start_date, period=hour))

    else:
        for hour in range(start_time_period, 24):
            db.session.add(UsageLog(user_id=user_id, hardware_id=hardware_id, date=start_date, period=hour))
        date_generated = [start_date + datetime.timedelta(days=x) for x in range(1, (end_date - start_date).days)]
        for date in date_generated:
            for hour in range(24):
                db.session.add(UsageLog(user_id=user_id, hardware_id=hardware_id, date=date, period=hour))
        for hour in range(0, end_time_period):
            db.session.add(UsageLog(user_id=user_id, hardware_id=hardware_id, date=end_date, period=hour))
    db.session.commit()
    return {'msg': "log usage success"}, 200


@app.route('/login')
def login():
    if 'ncu_protal' in session:
        return redirect(url_for('index_page'))
    return oauth.ncu_protal.authorize_redirect(f"{config['Domain']}/authorize")


@app.route('/logout')
def logout():
    session.pop('ncu_protal', None)
    return redirect(url_for('index_page'))


@app.route('/authorize')
def authorize():
    token = oauth.ncu_protal.authorize_access_token()
    user_info = oauth.ncu_protal.get('https://portal.ncu.edu.tw/apis/oauth/v1/info').json()
    session['ncu_protal'] = token['access_token']
    user = User.query.filter_by(id=user_info['identifier']).first()
    if user:
        user.token = session['ncu_protal']
    else:
        db.session.add(User(
            token=token['access_token'],
            account_type=user_info['accountType'],
            chinese_name=user_info['chineseName'],
            id=user_info['identifier'],
            email=user_info['email'],
        ))
    db.session.commit()
    return redirect(url_for('apply_page'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=config['Port'])
