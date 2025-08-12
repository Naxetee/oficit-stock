# Tests package
import os
from sqlalchemy import text

def reset_db(db):
    """
    Limpia todas las tablas de la base de datos.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, '..', '..', 'scripts', 'reset.sql')
    with open(file_path, "r", encoding="utf-8") as f:
        sql_script = f.read()
    db.execute(text(sql_script))
    db.commit()
