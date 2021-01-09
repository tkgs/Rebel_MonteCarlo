from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = '8730ceb869d207b824ba14a8f894a20d'

from Rebel_MonteCarlo import routes