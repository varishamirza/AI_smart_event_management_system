#!/usr/bin/env python
import sys
import traceback

# Add project root to path
sys.path.insert(0, '.')

print("=" * 60)
print("DEBUGGING APP.DATABASE IMPORT")
print("=" * 60)

try:
    print("\n1. Attempting to import app.database...")
    import app.database as db_module
    print(f"   ✓ Module imported")
    print(f"   Module file: {db_module.__file__}")
    print(f"   Module attributes: {dir(db_module)}")
    
    # Try to access each expected attribute
    print("\n2. Checking for expected attributes...")
    attrs = ['SessionLocal', 'engine', 'Base', 'get_db']
    for attr in attrs:
        if hasattr(db_module, attr):
            print(f"   ✓ {attr}: {getattr(db_module, attr)}")
        else:
            print(f"   ✗ MISSING: {attr}")
            
except Exception as e:
    print(f"\n   ✗ ERROR during import:")
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("DEBUG COMPLETE")
print("=" * 60)
