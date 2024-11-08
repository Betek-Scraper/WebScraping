from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import pandas as pd
import os
import linkedinjob
import Empleo_Candidato
import enviar_correos
from werkzeug.utils import secure_filename
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necesario para mostrar mensajes flash

# Ruta de subida de archivos
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Variable de estado para verificar si se han generado los archivos
files_generated = False


# Página principal
@app.route('/')
def index():
    return render_template('index.html')


# Ruta para subir y procesar el archivo de candidatos
@app.route('/upload', methods=['POST'])
def upload_file():
    global files_generated  # Declarar la variable como global para modificarla

    if 'file' not in request.files:
        flash('No seleccionaste ningún archivo')
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        flash('Selecciona un archivo válido')
        return redirect(url_for('index'))

    # Guardar el archivo de candidatos en la carpeta de subida
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Obtener las URLs de los formularios
    url1 = request.form.get('url1') or 'https://co.computrabajo.com/trabajo-de-desarrollador'  # Valor predeterminado
    url2 = request.form.get('url2')
    vacancy_count = int(request.form.get('vacancy_count'))

    # Verificar los campos necesarios en el archivo Excel
    try:
        df = pd.read_excel(filepath)
        required_columns = ['Nombre(s)', 'Apellidos', 'Perfil', 'Género', 'Ubicación',
                            'Nivel de Inglés', 'Teléfono de Contacto', 'Correo de Contacto',
                            'Skills', 'Perfil en LinkedIn', 'Perfil GitHub', 'Hoja de Vida']

        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            flash(f'Faltan los siguientes campos en el archivo: {", ".join(missing_columns)}')
            return redirect(url_for('index'))

    except Exception as e:
        flash(f'Error al leer el archivo: {e}')
        return redirect(url_for('index'))

    # Generar el Excel de trabajos usando linkedinjob
    linkedinjob.generar_excel(urls=[url1, url2], vacancy_count=vacancy_count)  # Esto guardará el archivo en disco

    # Procesar el archivo de candidatos usando Empleo_Candidato
    Empleo_Candidato.procesar_excel(filepath)

    # Cambiar el estado a verdadero al completar la generación de archivos
    files_generated = True

    flash('Archivo procesado exitosamente. Puedes descargar los archivos generados.')
    return redirect(url_for('index'))


# Ruta para descargar el archivo de coincidencias
@app.route('/download_coincidencias')
def download_coincidencias():
    if not files_generated:  # Verificar si los archivos han sido generados
        flash('Primero debes procesar los archivos antes de descargar.')
        return redirect(url_for('index'))

    best_matches_df = pd.read_excel('Mejores_Coincidencias_Ingles_Ajustado.xlsx')
    output = BytesIO()
    best_matches_df.to_excel(output, index=False)
    output.seek(0)
    return send_file(output, as_attachment=True, download_name='Mejores_Coincidencias_Ingles_Ajustado.xlsx')


# Ruta para descargar el archivo de Computrabajo
@app.route('/download_computrabajo')
def download_computrabajo():
    if not files_generated:  # Verificar si los archivos han sido generados
        flash('Primero debes procesar los archivos antes de descargar.')
        return redirect(url_for('index'))

    computrabajo_df = pd.read_excel('Computrabajo_Jobs.xlsx')
    output = BytesIO()
    computrabajo_df.to_excel(output, index=False)
    output.seek(0)
    return send_file(output, as_attachment=True, download_name='Computrabajo_Jobs.xlsx')


# Ruta para enviar correos a todos los candidatos
@app.route('/send_emails', methods=['POST'])
def send_emails():
    global files_generated  # Usar la variable global para verificar el estado

    if not files_generated:
        flash('Debes procesar primero los archivos de candidatos antes de enviar correos.')
        return redirect(url_for('index'))

    try:
        enviar_correos.enviar_emails()  # Llamar a la función que envía correos
        flash('Correos enviados exitosamente.')
    except Exception as e:
        flash(f'Error al enviar correos: {e}')

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
