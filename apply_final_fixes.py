import os

# --- 1. Fix backend/src/middleware/errorHandler.ts to intercept Check Constraints ---
err_path = 'backend/src/middleware/errorHandler.ts'
if os.path.exists(err_path):
    c = open(err_path, encoding='utf-8').read()
    
    # Check if we already patched it
    if '23514' not in c:
        patched_handler = """export const errorHandler = (err: any, req: Request, res: Response, _next: NextFunction): void => {
  logger.error("Unhandled error", { message: err.message, path: req.path, method: req.method });
  
  // Intercept PostgreSQL check constraint validation errors (e.g., users_role_check)
  if (err.code === '23514') {
    res.status(400).json({ message: f"Database constraint violation: {err.constraint or 'Invalid field input value'}" });
    return;
  }
  
  res.status(500).json({ message: "Internal server error" });
};"""
        # Find where errorHandler starts and swap it cleanly
        idx = c.find("export const errorHandler")
        if idx > -1:
            c = c[:idx] + patched_handler
            open(err_path, 'w', encoding='utf-8').write(c)
            print("Successfully updated errorHandler.ts to intercept constraint crashes!")
else:
    print("errorHandler.ts not found")

# --- 2. Fix backend/src/routes/users.ts to wrap PATCH in try/catch ---
users_path = 'backend/src/routes/users.ts'
if os.path.exists(users_path):
    c = open(users_path, encoding='utf-8').read()
    
    old_segment = """  const { teamId } = req.body as { teamId?: string | null };
  await pool.query(
    "UPDATE users SET team_id = $1 WHERE id = $2",
    [teamId || null, req.params.id]
  );"""

    new_segment = """  const { teamId } = req.body as { teamId?: string | null };
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

    if old_segment in c:
        c = c.replace(old_segment, new_segment)
        
        # Add the closing catch safety block right before the route block terminates
        c = c.replace(
            '  res.json({ message: "Team updated" });\n});',
            '  res.json({ message: "Team updated" });\n  } catch (err: any) { res.status(500).json({ message: err.message || "Failed to update team" }); }\n});'
        )
        open(users_path, 'w', encoding='utf-8').write(c)
        print("Successfully injected error validation into PATCH /users/:id/team!")
    else:
        print("PATCH pattern mismatch in users.ts. Check if already modified.")

print("Done modification operations.")