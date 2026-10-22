import os

dirs = [
    "c:/cep/documentready/app/routes",
    "c:/cep/documentready/app/services",
    "c:/cep/documentready/app/models",
    "c:/cep/documentready/app/data/schema",
    "c:/cep/documentready/app/templates/partials",
    "c:/cep/documentready/app/static/css",
    "c:/cep/documentready/app/static/js",
    "c:/cep/documentready/app/static/img/icons",
    "c:/cep/documentready/scripts",
    "c:/cep/documentready/tests",
    "c:/cep/documentready/docs"
]

for d in dirs:
    os.makedirs(d, exist_ok=True)

print("Directories created.")
