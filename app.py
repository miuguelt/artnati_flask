from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = "clave_secreta_segura"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/nosotros")
def nosotros():
    return render_template("nosotros.html")

@app.route("/servicios")
def servicios():
    return render_template("servicios.html")

@app.route("/informacion-esal", methods=["GET", "POST"])
def informacion_esal():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No se seleccionó ningún archivo")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            flash("El archivo no tiene nombre")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            flash("Archivo subido con éxito")
            return redirect(request.url)
        else:
            flash("Formato no permitido. Solo se aceptan PDFs.")
            return redirect(request.url)
    archivos = os.listdir(app.config["UPLOAD_FOLDER"])
    return render_template("informacion_esal.html", archivos=archivos)

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/eliminar-archivo/<filename>", methods=["POST"])
def eliminar_archivo(filename):
    try:
        archivo_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        if os.path.exists(archivo_path):
            os.remove(archivo_path)
            flash("Archivo eliminado con éxito", "success")
        else:
            flash("El archivo no existe", "error")
    except Exception as e:
        flash(f"Error al eliminar el archivo: {str(e)}", "error")
    return redirect(url_for("informacion_esal"))

@app.route("/equipo")
def equipo():
    mp3_folder = os.path.join("static", "mp3")
    if os.path.exists(mp3_folder):
        mp3_files = [f for f in os.listdir(mp3_folder) if f.lower().endswith('.mp3')]
    else:
        mp3_files = []
    return render_template("equipo.html", mp3_files=mp3_files)

@app.route("/orquesta")
def orquesta():
    return render_template("orquesta.html")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
