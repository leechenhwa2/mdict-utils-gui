
import sqlite3

from mdict_utils.base.readmdict import MDX
from tqdm import tqdm


def unpack_to_db_huadict(db_name, source, encoding='', substyle=False, passcode=None):
    with sqlite3.connect(db_name) as conn:
        if source.endswith('.mdx'):
            mdx = MDX(source, encoding, substyle, passcode)
            print('encoding = ' + mdx._encoding)

            conn.execute('DROP TABLE IF EXISTS info')
            conn.execute('CREATE TABLE info (id INTEGER PRIMARY KEY AUTOINCREMENT, word text, content text, word1 text)')
            meta = {}
            for key, value in mdx.header.items():
                key = key.decode(mdx._encoding).lower()
                value = '\r\n'.join(value.decode(mdx._encoding).splitlines())
                meta[key] = value

            conn.executemany('INSERT INTO info(word, content) VALUES (?,?)', meta.items())
            conn.commit()

            conn.execute('DROP TABLE IF EXISTS dict')
            conn.execute('CREATE TABLE dict (id INTEGER PRIMARY KEY AUTOINCREMENT, word text, content text, word1 text, word2 text)')

            bar = tqdm(total=len(mdx), unit='rec')
            max_batch = 1024
            count = 0
            entries = []
            for key, value in mdx.items():
                if not value.strip():
                    continue
                count += 1
                key = key.decode(mdx._encoding)
                value = value.decode(mdx._encoding)
                entries.append((key, value))
                if count > max_batch:
                    conn.executemany('INSERT INTO dict(word, content) VALUES (?,?)', entries)
                    conn.commit()
                    count = 0
                    entries = []
                bar.update(1)

            if entries:
                conn.executemany('INSERT INTO dict(word, content) VALUES (?,?)', entries)
                conn.commit()
            bar.close()
            conn.execute('CREATE INDEX idx_dict ON dict (word)')

        elif source.endswith('.mdd'):
            print('[Note] mdd ignored by huadict')
