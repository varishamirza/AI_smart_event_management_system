# test_import_db.py
import importlib, traceback

try:
    m = importlib.import_module('app.database')
    print('IMPORTED:', m)
    print('HAS_ENGINE =', hasattr(m, 'engine'))
    print('ENGINE =', getattr(m, 'engine', None))
except Exception:
    traceback.print_exc()