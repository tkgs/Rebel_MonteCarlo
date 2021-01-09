from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DecimalField
from wtforms.validators import InputRequired, NumberRange


class InputForm(FlaskForm):

    num_sim = IntegerField('Número de simulações',
                           validators=[InputRequired(), NumberRange(min=2)])
    prazo_min = DecimalField('Prazo mínimo',
                           validators=[InputRequired(), NumberRange(min=1)])
    prazo_med = DecimalField('Prazo médio',
                            validators=[InputRequired(), NumberRange(min=1)])
    prazo_max = DecimalField('Prazo máximo',
                            validators=[InputRequired(), NumberRange(min=1)])
    prazo_std = DecimalField('Desvio padrão',
                            validators=[InputRequired(), NumberRange(min=0)])

    juros_min = DecimalField('Juros mínimo',
                           validators=[InputRequired(), NumberRange(min=0.01)])
    juros_med = DecimalField('Juros médio',
                            validators=[InputRequired(), NumberRange(min=0.01)])
    juros_max = DecimalField('Juros máximo',
                            validators=[InputRequired(), NumberRange(min=0.01)])
    juros_std = DecimalField('Desvio padrão',
                            validators=[InputRequired(), NumberRange(min=0)])

    divida_min = DecimalField('Dívida mínima',
                            validators=[InputRequired(), NumberRange(min=1000)], default=1000)
    divida_med = DecimalField('Dívida média',
                            validators=[InputRequired(), NumberRange(min=1000)], default=15000)
    divida_max = DecimalField('Dívida máxima',
                            validators=[InputRequired(), NumberRange(min=1000)], default=30000)
    divida_std = DecimalField('Desvio padrão',
                            validators=[InputRequired(), NumberRange(min=0)], default=5000)

    curva_default = StringField('Curva de default',
                             validators=[InputRequired()], default='1, 2, 3, 4, 5')

    submit = SubmitField('Simular')

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        result = True
        error_msg = 'Valor incompatível.'
        if self.prazo_min.data > self.prazo_max.data or self.prazo_min.data > self.prazo_med.data:
            self.prazo_min.errors.append(error_msg)
            result = False
        if self.prazo_med.data > self.prazo_max.data:
            self.prazo_max.errors.append(error_msg)
            result = False
            
        if self.juros_min.data > self.juros_max.data or self.juros_min.data > self.juros_med.data:
            self.juros_min.errors.append(error_msg)
            result = False
        if self.juros_med.data > self.juros_max.data:
            self.juros_max.errors.append(error_msg)
            result = False
            
        if self.divida_min.data > self.divida_max.data or self.divida_min.data > self.divida_med.data:
            self.divida_min.errors.append(error_msg)
            result = False
        if self.divida_med.data > self.divida_max.data:
            self.divida_max.errors.append(error_msg)
            result = False

        return result