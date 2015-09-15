#!/usr/bin/env python2
import os
import locale
import re

locale.setlocale(locale.LC_ALL, "cs_CZ.UTF-8")

LYRICS_DIR = './pisne/'
DATA_DIR = './data/'


class Output:
    out = ''
    songs = []

    def __init__(self, songs):
        self.songs = songs

        out = open(DATA_DIR + 'template.tex').read()
        out = out.replace("%CONTENT%", self.getContent())

        self.out = out

    def getContent(self):
        ret = ''
        template = open(DATA_DIR + '/song.tex').read()

        for song in self.songs:
            cret = template.replace("%NAME%", song.name)
            cret = cret.replace("%AUTHOR%", song.author)
            cret = cret.replace("%LYRICS%", song.lyrics)
            ret += cret

        return ret

    def get(self):
        return self.out


class Lyrics:
    name = ''
    lyrics = ''
    author = ''
    RE_NAME = re.compile(r'(.*)\[(.*)\]$')

    def __init__(self, content):
        name = self.RE_NAME.split(content.readline().strip())
        if len(name) == 1:
            self.name = name[0]
        else:
            self.name, self.author = name[1:-1]

        content.readline()

        l = content.read()
        l = l.replace("#", "\#")
        l = l.replace("[", "\ch{")
        l = l.replace("]", "}")
        l = l.replace("\n", "\\\\\n")

        self.lyrics = l

    def get(self):
        return self.name


if __name__ == "__main__":
    songs = []
    for file in os.listdir(LYRICS_DIR):
        filePath = LYRICS_DIR + '/' + file
        print(file)

        if os.path.isfile(filePath) and file.split('.')[1] == "txt":
            content = open(filePath)
            songs.append(Lyrics(content))

    songs.sort(key=lambda song: song.name, cmp=locale.strcoll)

    for song in songs:
        print(song.get())

    save = open('./output/zpevnik.tex', 'w')
    save.write(Output(songs).get())
