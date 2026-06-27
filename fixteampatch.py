import os, re

fname = 'backend/src/routes/users.ts'
c = open(fname, encoding='utf-8').read()

# Fix PATCH /:id/team to handle errors gracefully
old = """router.patch('/:id/team', requireAuth, requireRole(['admin']), async (req: Request, res: Response) => {
  const { teamId } = req.body as { teamId?: string | null };
  await pool.query(
    "UPDATE users SET team_id = $1 WHERE id = $2",
    [teamId || null, req.params.id]
  );"""

new = """router.patch('/:id/team', requireAuth, requireRole(['admin']), async (req: Request, res: Response) => {
  const { teamId } = req.body as { teamId?: string | null };
  try {
    if (teamId) {
      const teamCheck = await pool.query("SELECT id FROM teams WHERE id = $1", [teamId]);
      if (teamCheck.rows.length === 0) {
        res.status(404).json({ message: "Team not found" });
        return;
      }
    }
    await pool.query(
      "UPDATE users SET team_id = $1 WHERE id = $2",
      [teamId || null, req.params.id]
    );"""

if old in c:
    c = c.replace(old, new)
    # Close the try block before the audit log closing
    c = c.replace(
        "  res.json({ message: \"Team updated\" });\n});",
        "  res.json({ message: \"Team updated\" });\n  } catch (err: any) { res.status(500).json({ message: err.message || \"Failed to update team\" }); }\n});"
    , 1)
    open(fname, 'w', encoding='utf-8').write(c)
    print("Fixed PATCH /:id/team with error handling")
else:
    print("Pattern not found - checking current content:")
    # Find the team patch route
    idx = c.find("/:id/team")
    if idx > -1:
        print(c[idx-20:idx+400])
    else:
        print("No /:id/team route found")