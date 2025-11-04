import os

BASE = "D:/NOJA/noja/backend/static/home/homepage"
expected = [
    "css/vendors.min.css",
    "css/icon.min.css",
    "css/style.css",
    "css/responsive.css",
    "demos/startup/startup.css",
]

missing = [f for f in expected if not os.path.exists(os.path.join(BASE, f))]
print("Archivos faltantes:", missing)

