import os, re

# Find the db init file
for fname in ['backend/src/db/seed.ts', 'backend/src/db/init.ts', 'backend/src/db/schema.ts']:
    if not os.path.exists(fname):
        continue
    c = open(fname, encoding='utf-8').read()
    
    # Add incident_comments table if missing
    if 'incident_comments' not in c:
        new_table = """
    await pool.query(`
      CREATE TABLE IF NOT EXISTS incident_comments (
        id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        incident_id UUID NOT NULL REFERENCES incidents(id) ON DELETE CASCADE,
        user_id     UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        content     TEXT NOT NULL,
        created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
      )
    `);
    await pool.query(`
      CREATE INDEX IF NOT EXISTS idx_incident_comments_incident_id
        ON incident_comments(incident_id)
    `);"""
        
        # Insert before the last closing of initDb function
        c = re.sub(
            r'(console\.log\(["\']Database initialized["\'])',
            new_table + r'\n  \1',
            c
        )
        open(fname, 'w', encoding='utf-8').write(c)
        print('Fixed: ' + fname)
    else:
        print('incident_comments already in: ' + fname)

print('Done')