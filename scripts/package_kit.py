"""Empaqueta solo fuentes permitidas del Director, sin .env ni archivos temporales."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / "kit-director"
FILES = [".env.example", ".gitignore", "README.md", "requirements-director.txt", "probar_oci.py", "director/ficha.yaml", "app.py", "Dockerfile", ".dockerignore", "tests/test_politica.py"]
FILES += [str(p.relative_to(KIT)) for p in sorted((KIT / "director").glob("*.py"))]
with ZipFile(ROOT / "downloads/kit-director.zip", "w", ZIP_DEFLATED) as archive:
    for name in FILES:
        archive.write(KIT / name, "kit-director/" + name)
print(f"Kit empaquetado: {len(FILES)} archivos")
