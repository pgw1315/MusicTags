# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@项目 :  MusicTags
@文件 :  MusicTag.py
@时间 :  2021/11/06 10:08
@作者 :  will
@版本 :  1.0
@说明 :   

'''
import os

import eyed3
import music_tag
from eyed3.id3.frames import ImageFrame
from mutagen.mp4 import MP4, MP4Cover


class MusicTag(object):

    def __init__(self):
        pass

    def edit_tag(self, music):
        music_file = music_tag.load_file(music['path'])
        music_file['title'] = music.get('title', "")
        music_file['artist'] = music.get('artist', "")
        music_file['album'] = music.get('album', "")
        music_file['genre'] = music.get('genre', "")
        music_file['lyrics'] = music.get('lyrics', "")
        music_file.save()
        # print("音乐文件的标签修改完成")

    def add_cover(self, music_path, cover_path):
        """
    给音乐文件添加封面图片
        Args:
            music_path: 音乐文件的路径
            cover_path: 封面图片所在的路径
        """
        if os.path.isfile(music_path):
            if os.path.isfile(cover_path):
                try:
                    if music_path[-3:] == "m4a":
                        # m4a格式文件
                        video = MP4(music_path)
                        with open(cover_path, "rb") as f:
                            video["covr"] = [
                                MP4Cover(f.read(), imageformat=MP4Cover.FORMAT_JPEG)
                            ]
                        video.save()
                        return True
                    elif music_path[-3:] == "mp3":
                        # mp3文件格式
                        file = eyed3.load(music_path)
                        if file.tag == None:
                            file.initTag()
                        file.tag.images.set(ImageFrame.FRONT_COVER, open(cover_path, 'rb').read(), 'image/jpeg')
                        file.tag.save()

                    else:
                        return False
                        pass
                    os.remove(cover_path)
                    return True
                except Exception as e:
                    print("Oops:歌曲添加专辑封面失败啦：", e)
                    return False
                    pass

            else:
                print(cover_path + "封面图片文件文件不存在！")
                return False
        else:
            print(music_path + "音乐文件文件不存在！")
            return False
        pass
