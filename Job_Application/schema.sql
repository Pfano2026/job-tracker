-- Database for the Internship & Job Application Tracker (SQLite)
CREATE TABLE IF NOT EXISTS applications (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    company      TEXT NOT NULL,
    role         TEXT NOT NULL,
    date_applied TEXT NOT NULL,                       -- YYYY-MM-DD
    status       TEXT NOT NULL DEFAULT 'applied'
                 CHECK (status IN ('applied','interview','offer','rejected'))
);

-- Sample rows (delete these if you don't want them)
INSERT INTO applications (company, role, date_applied, status)
SELECT 'Example Corp', 'Software Intern', '2026-10-01', 'applied'
WHERE NOT EXISTS (SELECT 1 FROM applications);
