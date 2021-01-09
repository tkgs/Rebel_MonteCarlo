import random
import pickle
import secrets
from PIL import Image
import io
from montecarlo import montecarlo_simulation
from flask import render_template, url_for, flash, redirect, request, abort, Response
# from flaskblog import app, db, bcrypt
from Rebel_MonteCarlo import app
from Rebel_MonteCarlo.forms import InputForm
from Rebel_MonteCarlo.utils import number_format
# from matplotlib.figure import Figure
# from matplotlib.backends.backend_svg import FigureCanvasSVG

# Valores usados para preencher o formulario de inputs quando rodar o app pela 1a vez.
# Apos a 1a vez, os inputs usados sao lembrados para preencher o formulario nas próximas vezes.
default_inputs = [[6, 21, 36, 8],   #prazo (min, med, max, std)
                  [1.9, 3.45, 5, 1], #juros
                  [1000, 15000, 30000, 5000], #divida
                  "5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27", #curva_default (mes1 a mes12)
                  1000] #numero de simulacoes

@app.route('/', methods=['GET','POST'])
@app.route('/home', methods=['GET','POST'])
def home():
    # Tenta importar os inputs usados na última simulação rodada
    try:
        with open('input_pickle', 'rb') as f:
            input = pickle.load(f)
    except:
        input = default_inputs

    form = InputForm()
    if form.validate_on_submit():
        prazo = [form.prazo_min.data, form.prazo_med.data, form.prazo_max.data, form.prazo_std.data]
        juros = [form.juros_min.data, form.juros_med.data, form.juros_max.data, form.juros_std.data]
        divida = [form.divida_min.data, form.divida_med.data, form.divida_max.data, form.divida_std.data]
        curva_default = form.curva_default.data
        n_sim = int(form.num_sim.data)
        input = [prazo, juros, divida, curva_default, n_sim]
        # Salva pickle
        with open('input_pickle', 'wb') as f:
            pickle.dump(input, f)

        # Converte curva_default para uma lista int e remove possíveis caracteres indesejados
        curva_default = list(curva_default.replace(" ","")
                             .replace("[","").replace("]","")
                             .split(","))
        curva_default = [int(i) for i in curva_default]

        output = montecarlo_simulation(prazo=prazo, juros=juros, divida=divida, curva_default=curva_default, n_sim=n_sim)
        flash('Simulação executada com sucesso! Número de simulações: ' + str(n_sim), 'success')
    else:
        output = None
        data = None
    return render_template('home.html', form=form, input=input, output=output)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

# @app.route("/matplot-as-image.svg")
# def plot_svg(num_x_points=50):
#     # Renders the plot on the fly
#     fig = Figure()
#     axis = fig.add_subplot(1, 1, 1)
#     x_points = range(num_x_points)
#     axis.plot(x_points, [random.randint(1, 30) for x in x_points])
#     fig.tight_layout()
#
#     output = io.BytesIO()
#     FigureCanvasSVG(fig).print_svg(output)
#     return Response(output.getvalue(), mimetype="image/svg+xml")