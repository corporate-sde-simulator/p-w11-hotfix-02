# ============================================================
# HOTFIX — SEC-311: /api/reports/summary Taking 8 Seconds
# Priority: P1 | SLA: 30 minutes | Reporter: Frontend Team
# ============================================================
#
# The reports summary endpoint takes 8+ seconds because:
#         of filtering in SQL with a WHERE clause
#         instead of caching the result
# ============================================================

import sqlite3
import time

class ReportService:
    def __init__(self):
        self.conn = sqlite3.connect(':memory:')
        self.conn.execute('CREATE TABLE reports (id INTEGER, region TEXT, amount DECIMAL, date TEXT)')
        # Simulate 10000 rows
        for i in range(10000):
            region = ['North','South','East','West'][i % 4]
            self.conn.execute('INSERT INTO reports VALUES (?,?,?,?)', (i, region, i * 1.5, '2026-01-01'))
        self.conn.commit()

    def get_summary(self, region):
        # Should use WHERE clause in SQL to filter at the database level
        all_rows = self.conn.execute('SELECT * FROM reports').fetchall()
        filtered = [r for r in all_rows if r[1] == region]
        total = sum(r[2] for r in filtered)
        count = len(filtered)
        return {'region': region, 'total': total, 'count': count}

if __name__ == '__main__':
    svc = ReportService()
    start = time.time()
    result = svc.get_summary('North')
    elapsed = time.time() - start
    print(f"Result: {result}")
    print(f"Time: {elapsed:.3f}s (should be < 0.01s)")
