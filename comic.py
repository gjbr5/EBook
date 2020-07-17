from abc import *
from db import database
import os
from natsort import natsorted

db = database()

class comic(metaclass=ABCMeta):

    @abstractmethod
    def _get_table_name(self):
        pass

    @abstractmethod
    def get_comic_imgs(self, comic_type, id, episode=None):
        pass

    @abstractmethod
    def get_img_path(self, id, img_name, episode=None):
        pass

    def get_page_list(self, present_page):
        table_name = self._get_table_name()
        comic_count = db.execute('select count(*) from ' + table_name).fetchone()[0]
        total_page = comic_count // 10 + 1 if comic_count % 10 > 0 else comic_count // 10
        if present_page < 3:
            range_from = 1
            range_to = min(total_page, 5) + 1
        else:
            range_from = present_page - 2
            range_to = min(present_page + 2, total_page) + 1
        return range(range_from, range_to)
        
    def get_comic_list(self, limit=10, offset=0, desc=False):
        table_name = self._get_table_name()
        sql = 'select * from ' + table_name + ' order by id'
        if desc:
            sql += ' desc'
        if limit:
            sql += ' limit ' + str(limit)
        if offset:
            sql += ' offset ' + str(offset)
        comic_list = []
        cursor = db.execute(sql)
        title = [i[0] for i in cursor.description]
        for row in cursor:
            comic = {}
            for i in range(len(title)):
                comic[title[i]] = row[i]
            comic_list.append(comic)
        return comic_list
        
    def get_comic_info(self, id):
        table_name = self._get_table_name()
        sql = 'select * from ' + table_name + ' where id=' + str(id)
        cursor = db.execute(sql)
        title = [i[0] for i in cursor.description]
        row = cursor.fetchone()
        comic = {title[i]: str(row[i]) for i in range(len(title))}
        return comic

    
class hitomi(comic):

    def get_img_path(self, id, img_name, episode=None):
        return 'comic/manga/' + str(id) + '/' + img_name
        
    def _get_table_name(self):
        return 'manga'
        
    def get_comic_imgs(self, id, episode=None):
        return natsorted(os.listdir("static/comic/manga/" + str(id) + "/"))

class manamoa(comic):
    
    def get_img_path(self, id, img_name, episode=None):
        episode = os.listdir("static/comic/manamoa/" + str(id) + "/")[episode - 1]
        return 'comic/manamoa/' + str(id) + '/' + episode + '/' + img_name
        
    def _get_table_name(self):
        return 'manamoa'
        
    def get_comic_imgs(self, id, episode):
        episode_list = os.listdir("static/comic/manamoa/" + str(id) + "/")
        is_last = episode == len(episode_list)
        episode = episode_list[episode - 1]
        return episode.split(" - ")[1], natsorted(os.listdir("static/comic/manamoa/" + str(id) + "/" + episode + "/")), is_last
        
class webtoon(comic):
    
    def get_img_path(self, id, img_name, episode=None):
        episode = os.listdir("static/comic/webtoon/" + str(id) + "/")[episode - 1]
        return 'comic/webtoon/' + str(id) + '/' + episode + '/' + img_name
        
    def _get_table_name(self):
        return 'webtoon'
        
    def get_comic_imgs(self, id, episode):
        episode_list = os.listdir("static/comic/webtoon/" + str(id) + "/")
        is_last = episode == len(episode_list)
        episode = episode_list[episode - 1]
        return episode.split(" - ")[1], natsorted(os.listdir("static/comic/webtoon/" + str(id) + "/" + episode + "/")), is_last
