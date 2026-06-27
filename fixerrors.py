import os

fname = 'backend/src/middleware/errorHandler.ts'
if os.path.exists(fname):
    c = open(fname, encoding='utf-8').read()
    print('errorHandler.ts exists')
    print(c[:500])
else:
    print('errorHandler.ts not found')
    for root, dirs, files in os.walk('backend/src'):
        for f in files:
            print(os.path.join(root, f))