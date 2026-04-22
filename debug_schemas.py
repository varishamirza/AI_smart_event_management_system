import traceback
try:
    import app.schemas as s
    print('MODULE FILE:', s.__file__)
    print('ATTRS:', dir(s))
    print('Has VenueCreate:', hasattr(s, 'VenueCreate'))
    if hasattr(s, 'VenueCreate'):
        print('VenueCreate repr:', s.VenueCreate)
except Exception:
    traceback.print_exc()
