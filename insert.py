from os import listdir
from os import rename
from natsort import natsorted
import re
import sys
import sqlite3

pattern_manga = re.compile(r'\[(.*)\] (.*) \｜ (.*) \((.*)\)')
pattern_cartoon = re.compile(r'\[(.*)\] (.*) \((.*)\)')

def get_data(comic_type, comic_path):
    if comic_type == 'manga':
        res = pattern_manga.match(comic_path)
        if res:
            return 'Type1', (res.group(1), res.group(2), res.group(3), res.group(4))
    res = pattern_cartoon.match(comic_path)
    if res:
        return 'Type2', (res.group(1), res.group(2), res.group(3))
    return None, None
    
def insert_db(table, id, author, orgn_name, kor_name=None):
    conn = sqlite3.connect('list.db')
    c = conn.cursor()
    if kor_name:
        sql = 'insert into {} values ({}, "{}", "{}", "{}");'.format(table, id, author, orgn_name, kor_name)
    else:
        sql = 'insert into {} values ({}, "{}", "{}");'.format(table, id, author, orgn_name)
    print(sql)
    c.execute(sql)
    conn.commit()
    conn.close()

def main(comic_type, comic_path):
    if comic_type not in ['manga', 'manamoa', 'webtoon']:
        print('타입 오류')
        return
    pattern_type, data = get_data(comic_type, comic_path)
    if not pattern_type:
        print('구문 분석 오류')
        return
    if pattern_type == 'Type1':
        author, orgn_name, kor_name, id = data
        insert_db('manga', id, author, orgn_name, kor_name)
    else:
        author, orgn_name, id = data
        insert_db(comic_type, id, author, orgn_name)
    rename(comic_path, id)
    print('Confirmed')


if __name__ == '__main__':
    comic_type = sys.argv[1]
    comic_path = sys.argv[2].replace('\\', '/').split('/')[-1]
    main(comic_type, comic_path)