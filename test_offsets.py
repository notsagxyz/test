import sys

with open(r'ps4_offsets.js', 'r', encoding='utf-8') as f:
    code = f.read()

if 'PS4["13.52"] = Object.assign' in code:
    print('[OK] Verified 13.52 WebKit inheritance in ps4_offsets.js')
else:
    print('[FAIL] 13.52 WebKit inheritance missing')
    sys.exit(1)
