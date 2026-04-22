import runpy, traceback
try:
    runpy.run_module('app.schemas', run_name='__main__')
    print('run_module completed')
except Exception:
    traceback.print_exc()
