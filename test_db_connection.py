#! /usr/bin/python3
if __name__ == '__main__':
    import re
    import sys
    import db

    if len(sys.argv) != 2:
        print('Expected table name as argument')
        sys.exit(1)

    table_name = sys.argv[1]
    if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', table_name):
        print('Invalid table name')
        sys.exit(1)

    db.connect()
    data = db.execute(f'SELECT * FROM "{table_name}"').fetchall()
    print('%d results ...' % len(data))
    for d in data:
        print([(c, d[c]) for c in d.keys()])
    db.close()
