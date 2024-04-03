import tkinter as tk
from tkinter import messagebox
import os
from datetime import datetime
import random
import re

from PIL import Image, ImageTk


def resize_background(event):

    window_width = event.width
    window_height = event.height

    resized_image = original_image.resize((window_width, window_height), Image.ABICUBIC)
    resized_photo = ImageTk.PhotoImage(resized_image)

    background_label.configure(image=resized_photo)
    background_label.image = resized_photo


root = tk.Tk()
root.title("Generador de CRUD (laravel 8.0)")


original_image = Image.open("fondo5.jpg")  # Ruta de la imagen de fondo

# Obtener las dimensiones de la ventana
window_width = root.winfo_screenwidth()
window_height = root.winfo_screenheight()

resized_image = original_image.resize((window_width, window_height), Image.BICUBIC)
resized_photo = ImageTk.PhotoImage(resized_image)

background_label = tk.Label(root, image=resized_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

root.bind("<Configure>", resize_background)


font_style = ("Verdana", 12)
root.option_add("*Font", font_style)

label_proyecto = tk.Label(
    root,
    text="Nombre del Proyecto:",
    bd=3,
    relief="solid",
    bg="lightblue",
    font=("Times New Roman", 12),
)
label_proyecto.pack(pady=6)

entry_proyecto = tk.Entry(
    root,
    highlightbackground="blue",
    bd=2,
    relief="solid",
    bg="lightblue",
    font=("Times New Roman", 12),
)
entry_proyecto.pack(pady=6)

label_tabla = tk.Label(
    root,
    text="Nombre de la Tabla:",
    bd=2,
    relief="solid",
    bg="lightblue",
    font=("Times New Roman", 12),
)
label_tabla.pack(pady=7)

entry_tabla = tk.Entry(
    root,
    highlightbackground="blue",
    bd=2,
    relief="solid",
    bg="lightblue",
    font=("Times New Roman", 12),
)
entry_tabla.pack(pady=6)

label_campos = tk.Label(
    root, text="Tipo ('campo',otros):", bg="lightblue", font=("Times New Roman", 12)
)
label_campos.pack(pady=6)

text_campos = tk.Text(
    root, height=6, width=60, highlightbackground="blue", bg="lightblue"
)
text_campos.pack(pady=4)


def round_corners(widget):
    widget.config(
        highlightthickness=2, highlightbackground="black", borderwidth=0, relief="solid"
    )


round_corners(label_proyecto)
round_corners(entry_proyecto)
round_corners(label_tabla)
round_corners(entry_tabla)
round_corners(label_campos)
round_corners(text_campos)

# Cargar la imagen PNG
imagen_pequena = Image.open("logoLharrys.jpg")
imagen_pequena = imagen_pequena.resize(
    (130, 100), Image.BICUBIC
)  # Redimensionar la imagen
imagen_pequena = ImageTk.PhotoImage(imagen_pequena)

# Crear una etiqueta con la imagen encima de la interfaz
label_imagen_pequena = tk.Label(root, image=imagen_pequena)
label_imagen_pequena.place(x=50, y=50)  # Colocar la etiqueta en la posición deseada

# ..........................................................................................
campos_list = []


def crear_carpeta_tabla():
    nombre_proyecto = entry_proyecto.get()

    if not nombre_proyecto:
        messagebox.showerror("Error", "Por favor, ingresa el nombre del proyecto.")
        return

    nombre_tabla = entry_tabla.get()
    if not nombre_tabla:
        messagebox.showerror("Error", "Por favor, ingresa el nombre de la tabla.")
        return

    ruta_carpeta_tabla = os.path.join(
        f"C:/laragon/www/{nombre_proyecto}/resources/views/",
        f"{nombre_tabla}s",
    )

    os.makedirs(ruta_carpeta_tabla, exist_ok=True)


def generar_migracion():
    nombre_proyecto = entry_proyecto.get()
    nombre_tabla = entry_tabla.get()
    campos_raw = text_campos.get("1.0", tk.END).strip()

    if not nombre_tabla or not campos_raw:
        messagebox.showerror(
            "Error", "Por favor, ingresa el nombre de la tabla y al menos un campo."
        )
        return

    campos_array = campos_raw.split("\n")
    campos_formatados = ""
    for campo in campos_array:
        campo = campo.strip()
        if campo:
            campos_formatados += f"            $table->{campo};\n"

    now = datetime.now()
    fecha = now.strftime("%Y_%m_%d_%H%M%S")
    aleatorio = random.randint(
        100000, 999999
    )  # Generar solo un número aleatorio de 6 dígitos

    contenido_migracion = f"""<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{{
    public function up(): void
    {{
        Schema::create('{nombre_tabla}s', function (Blueprint $table) {{
{campos_formatados}            $table->timestamps();
        }});
    }}

    public function down(): void
    {{
        Schema::dropIfExists('{nombre_tabla}s');
    }}
}};
"""

    ruta_archivo = os.path.join(
        f"C:/laragon/www/{nombre_proyecto}/database/migrations/",
        f"{fecha}_{aleatorio}_create_{nombre_tabla}s_table.php",
    )
    with open(ruta_archivo, "w") as archivo:
        archivo.write(contenido_migracion)

    messagebox.showinfo(
        "Éxito", f"Archivo de migración creado con éxito: {ruta_archivo}"
    )


def generar_modelo():
    nombre_proyecto = entry_proyecto.get()
    nombre_tabla = entry_tabla.get()
    if not nombre_tabla:
        messagebox.showerror("Error", "Por favor, ingresa el nombre de la tabla.")
        return

    campos_raw = text_campos.get("1.0", tk.END).strip()
    if not campos_raw:
        messagebox.showerror(
            "Error", "Por favor, ingresa al menos un campo en el formato 'nombre_campo'"
        )
        return

    campos_array = re.findall(r"'([^']*)'", campos_raw)
    campos_formatados = ""
    for i, campo in enumerate(campos_array):
        campos_formatados += f"        '{campo}'"
        if i < len(campos_array) - 1:
            campos_formatados += ","
        campos_formatados += "\n"

    contenido_modelo = f"""<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class {nombre_tabla.capitalize()} extends Model
{{
    use HasFactory;

    protected $fillable = [
{campos_formatados}    ];
}}
"""

    ruta_archivo = os.path.join(
        f"C:/laragon/www/{nombre_proyecto}/app/Models/",
        f"{nombre_tabla.capitalize()}.php",
    )
    with open(ruta_archivo, "w") as archivo:
        archivo.write(contenido_modelo)

    messagebox.showinfo("Éxito", f"Archivo de modelo creado con éxito: {ruta_archivo}")


def generar_controlador():
    nombre_proyecto = entry_proyecto.get()
    nombre_tabla = entry_tabla.get()

    if not nombre_tabla:
        messagebox.showerror("Error", "Por favor, ingresa el nombre de la tabla.")
        return

    campos_raw = text_campos.get("1.0", tk.END).strip()
    if not campos_raw:
        messagebox.showerror(
            "Error", "Por favor, ingresa al menos un campo en el formato 'nombre_campo'"
        )
        return

    campos_array = re.findall(r"'([^']*)'", campos_raw)
    campos_formatados = ""
    for i, campo in enumerate(campos_array):
        campos_formatados += f"        '{campo}'=>'required'"
        if i < len(campos_array) - 1:
            campos_formatados += ","
        campos_formatados += "\n"
    contenido_controlador = f"""<?php

namespace App\Http\Controllers;

use App\Models\{nombre_tabla.capitalize()};
use Illuminate\Http\Request;

class {nombre_tabla.capitalize()}Controller extends Controller
{{
    public function index()
    {{
        ${nombre_tabla}s = {nombre_tabla.capitalize()}::paginate(20);
        return view('{nombre_tabla}s.listar', compact('{nombre_tabla}s'));
    }}

    public function create()
    {{
        return view('{nombre_tabla}s.registrar');
    }}

    public function store(Request $request)
    {{
        $request->validate([
            {campos_formatados}
        ]);
        {nombre_tabla.capitalize()}::create($request->all());
        return redirect()->route('{nombre_tabla}s.create')
        ->with('succses','{nombre_tabla} registrada con exito...');
    }}

    public function show({nombre_tabla.capitalize()} ${nombre_tabla})
    {{
        //return view('{nombre_tabla}_show', compact('{nombre_tabla}'));
    }}

    public function edit({nombre_tabla.capitalize()} ${nombre_tabla})
    {{
        return view('{nombre_tabla}s.editar', ['{nombre_tabla}'=>${nombre_tabla}]);
    }}

    public function update(Request $request, {nombre_tabla.capitalize()} ${nombre_tabla})
    {{
        
        $request->validate([
            {campos_formatados}
        ]);
        
        ${nombre_tabla}->update($request->all());
        return redirect()->route('{nombre_tabla}s.index')
        ->with('success','{nombre_tabla} editado con exito...');
    }}

    public function destroy({nombre_tabla.capitalize()} ${nombre_tabla})
    {{
        ${nombre_tabla}->delete();
        return redirect()->route('{nombre_tabla}s.index');
    }}
}}
"""

    ruta_archivo = os.path.join(
        f"C:/laragon/www/{nombre_proyecto}/app/Http/Controllers/",
        f"{nombre_tabla.capitalize()}Controller.php",
    )
    with open(ruta_archivo, "w") as archivo:
        archivo.write(contenido_controlador)

    messagebox.showinfo(
        "Éxito", f"Archivo de controlador creado con éxito: {ruta_archivo}"
    )


def generar_edicion():
    nombre_proyecto = entry_proyecto.get()
    nombre_tabla = entry_tabla.get()
    if not nombre_tabla:
        messagebox.showerror("Error", "Por favor, ingresa el nombre de la tabla.")
        return

    campos_raw = text_campos.get("1.0", tk.END).strip()
    if not campos_raw:
        messagebox.showerror(
            "Error", "Por favor, ingresa al menos un campo en el formato 'nombre_campo'"
        )
        return

    campos_array = re.findall(r"'([^']*)'", campos_raw)
    campos_formatados = ""
    for campo in campos_array:
        campos_formatados += f'        <div class = "row"> <x-adminlte-input name="{campo}" label="{campo}" placeholder="Ingrese {campo}" fgroup-class="col-md-6" disable-feedback value="{{{{${nombre_tabla}->{campo}}}}}"/></div>\n'

    contenido_edicion = f"""@extends('adminlte::page')

@section('title', 'Editar {nombre_tabla.capitalize()}s')

@section('content_header')
    <h1 class="m-0 text-dark">Editar {nombre_tabla.capitalize()}</h1>
@stop

@section('content')
  @if ($errors->any()) 
    <div class="alert alert-danger" >
        <strong>Hubo errores en los datos</strong>
        <ul>
            @foreach ($errors->all() as $error)
               <li>{{{{$error}}}}</li> 
            @endforeach
        </ul> 
    </div>
  @endif

  @if (Session::get('success'))
    <div class="alert alert-success mt-2" >
      <strong>{{{{Session::get('success')}}}}</strong>
    </div>    
  @endif

  <form action="{{{{route('{nombre_tabla}s.update',${nombre_tabla})}}}}" method="POST" autocomplete="off"> 
    @csrf
    @method('PUT')
    
    
{campos_formatados}    
    <x-adminlte-button class="btn-flat" type="submit" label="Actualizar" theme="success" icon="fas fa-lg fa-save"/>
</form>
@stop
"""

    ruta_archivo = os.path.join(
        f"C:/laragon/www/{nombre_proyecto}/resources/views/{nombre_tabla}s/",
        f"editar.blade.php",
    )
    with open(ruta_archivo, "w") as archivo:
        archivo.write(contenido_edicion)

    messagebox.showinfo("Éxito", f"Archivo de edición creado con éxito: {ruta_archivo}")


def generar_listar():
    nombre_proyecto = entry_proyecto.get()
    nombre_tabla = entry_tabla.get()
    if not nombre_tabla:
        messagebox.showerror("Error", "Por favor, ingresa el nombre de la tabla.")
        return

    campos_raw = text_campos.get("1.0", tk.END).strip()
    if not campos_raw:
        messagebox.showerror(
            "Error", "Por favor, ingresa al menos un campo en el formato 'nombre_campo'"
        )
        return

    campos_array = re.findall(r"'([^']*)'", campos_raw)
    campos_formatados = ""
    ca_format = ""
    for campo in campos_array:
        campos_formatados += f"        <th> {{{{ ${nombre_tabla}->{campo}}}}} </th>\n"

    for campo in campos_array:
        ca_format += f"        <th> {campo.capitalize()} </th>\n"

    contenido_listar = f"""@extends('adminlte::page')

@section('title', 'Lista de {nombre_tabla.capitalize()}s')

@section('content_header')
    <h1 class="m-0 text-dark">Lista {nombre_tabla.capitalize()}s</h1>
@stop

@section('content')
  <table class="table table-bordered text-black">
     <tr>
{ca_format.replace('<th>', '<td>').replace('</th>', '</td>')} <th> Opciones </th>
      </tr> 
      @foreach (${nombre_tabla}s as ${nombre_tabla})
      <tr>
      
{campos_formatados.replace('<th>', '<td>').replace('</th>', '</td>')}        <td>

            <a href="{{{{route('{nombre_tabla}s.edit',${nombre_tabla})}}}}" class="btn btn-warning">Editar</a> 
            <form action="{{{{route('{nombre_tabla}s.destroy',${nombre_tabla})}}}}" 
            class="d-inline" method="POST">
              @csrf
              @method('DELETE')
              <button type="submit" class="btn btn-danger">Eliminar</button>
            </form>
        </td>
      </tr>
      @endforeach
  </table>
  <div>{{{{${nombre_tabla}s->links() }}}}</div> 
  
@stop
"""

    ruta_archivo = os.path.join(
        f"C:/laragon/www/{nombre_proyecto}/resources/views/{nombre_tabla}s/",
        f"listar.blade.php",
    )
    with open(ruta_archivo, "w") as archivo:
        archivo.write(contenido_listar)

    messagebox.showinfo("Éxito", f"Archivo de listar creado con éxito: {ruta_archivo}")


def generar_registro():
    nombre_proyecto = entry_proyecto.get()
    nombre_tabla = entry_tabla.get()
    if not nombre_tabla:
        messagebox.showerror("Error", "Por favor, ingresa el nombre de la tabla.")
        return

    campos_raw = text_campos.get("1.0", tk.END).strip()
    if not campos_raw:
        messagebox.showerror(
            "Error", "Por favor, ingresa al menos un campo en el formato "
        )
        return

    campos_array = re.findall(r"'([^']*)'", campos_raw)
    campos_formatados = ""
    for campo in campos_array:
        campos_formatados += f'        <div class="row"> <x-adminlte-input name="{campo}" label="{campo}" placeholder="Ingrese {campo}" fgroup-class="col-md-6" disable-feedback/></div>\n'

    contenido_registro = f"""@extends('adminlte::page')

@section('title', 'Registro de {nombre_tabla.capitalize()}s')

@section('content_header')
    <h1 class="m-0 text-dark">Registrar {nombre_tabla.capitalize()}s</h1>
@stop

@section('content')
  @if ($errors->any()) 
    <div class="alert alert-danger" >
        <strong>Hubo errores en los datos</strong>
        <ul>
            @foreach ($errors->all() as $error)
               <li>{{{{$error}}}}</li> 
            @endforeach
        </ul> 
    </div>
  @endif

  @if (Session::get('success'))
    <div class="alert alert-success mt-2" >
      <strong>{{{{Session::get('success')}}}}</strong> 
    </div>    
  @endif

  <form action="{{{{route('{nombre_tabla}s.store')}}}}" method="POST" autocomplete="off">
    @csrf
    
{campos_formatados}    
    <x-adminlte-button class="btn-flat" type="submit" label="Registrar" theme="success" icon="fas fa-lg fa-save"/>
</form>
@stop
"""

    ruta_archivo = os.path.join(
        f"C:/laragon/www/{nombre_proyecto}/resources/views/{nombre_tabla}s/",
        f"registrar.blade.php",
    )
    with open(ruta_archivo, "w") as archivo:
        archivo.write(contenido_registro)

    messagebox.showinfo(
        "Éxito", f"Archivo de registro creado con éxito: {ruta_archivo}"
    )


button_crear_carpeta_tabla = tk.Button(
    root,
    text="CREAR CARPETA TABLA",
    command=crear_carpeta_tabla,
    bg="blue",
    fg="white",
    relief="raised",
    padx=15,
)
button_crear_carpeta_tabla.pack(fill="x", padx=100, pady=(10, 0))

button_generar_registro = tk.Button(
    root,
    text="GENERAR REGISTRO",
    command=generar_registro,
    bg="#4169E1",
    fg="white",
    relief="raised",
    padx=95,
)
button_generar_registro.pack(fill="x", padx=100, pady=(10, 0))

button_generar_listar = tk.Button(
    root,
    text="GENERAR LISTAR",
    command=generar_listar,
    bg="blue",
    fg="white",
    relief="raised",
    padx=103,
)
button_generar_listar.pack(fill="x", padx=100, pady=(10, 0))

button_generar_edicion = tk.Button(
    root,
    text="GENERAR EDICIÓN",
    command=generar_edicion,
    bg="#4169E1",
    fg="white",
    relief="raised",
    padx=96,
)
button_generar_edicion.pack(fill="x", padx=100, pady=(10, 0))

button_generar_migracion = tk.Button(
    root,
    text="GENERAR MIGRACIÓN",
    command=generar_migracion,
    bg="blue",
    fg="white",
    relief="raised",
    padx=96,
)
button_generar_migracion.pack(fill="x", padx=100, pady=(10, 0))

button_generar_modelo = tk.Button(
    root,
    text="GENERAR MODELO",
    command=generar_modelo,
    bg="#4169E1",
    fg="white",
    relief="raised",
    padx=96,
)
button_generar_modelo.pack(fill="x", padx=100, pady=(10, 0))

button_generar_controlador = tk.Button(
    root,
    text="GENERAR CONTROLADOR",
    command=generar_controlador,
    bg="blue",
    fg="white",
    relief="raised",
    padx=96,
)
button_generar_controlador.pack(fill="x", padx=100, pady=(10, 0))

root.mainloop()
