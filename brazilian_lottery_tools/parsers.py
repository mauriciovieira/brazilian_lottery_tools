#!/usr/bin/env python3
# coding: utf-8

from html.parser import HTMLParser
import json

class LoteriasParser(HTMLParser):
    title = "Resultado"
    concursos = []
    headers = []
    in_headers = False

    def __init__(self,page):
        page = open(page, encoding = 'iso-8859-1').read()
        HTMLParser.__init__(self)
        self.feed(page)

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        if tag == 'tr':
            self.line = []
        elif tag == 'th':
            self.in_headers = True

    def handle_endtag(self, tag):
        if tag == 'tr':
            conc = dict(zip(self.headers, self.line))
            self.concursos.append(conc)
        elif tag == 'th':
            self.in_headers = False
        self.current_tag = None

    def handle_data(self, data):
        if self.current_tag == 'title':
            self.title = data
        elif self.current_tag == 'font' and self.in_headers:
            self.headers.append(data)
        elif self.current_tag == 'td':
            self.line.append(data)
        else:
            pass

    def to_json(self):
        return json.dumps(self.concursos)

    def sorteados(self, num):
        """Apostas sorteadas para o concurso num"""
        apostas = self.apostas or []
        concurso = {} if num>=len(self.concursos) else self.concursos[num]
        return set([concurso.get(x,0) for x in apostas])

    def confere(self, num, apostas):
        res = []
        if num >= len(self.concursos):
            res.append("Concurso %d - não aconteceu" % num )
        else:
            res.append("Concurso: %d - %s" % (num, self.concursos[num]['Data Sorteio']))
            res.append("\tJogos sorteados: %s" % (" ".join(sorted(self.sorteados(num)))))
            res.append("\tJogos    feitos: %s" % (" ".join(apostas)))
            acertos = self.sorteados(num).intersection(apostas)
            res.append("\t%d acertos - %s" % (len(acertos), " ".join(sorted(acertos))))
        return "\n".join(res)


class MegasenaParser(LoteriasParser):
    apostas = [ x for x in map(lambda s: "%dª Dezena" %s, range(1,7)) ]
    def __init__(self,page="./D_MEGA.HTM"):
        LoteriasParser.__init__(self,page)


class LotofacilParser(LoteriasParser):
    apostas = [ x for x in map(lambda s: "Bola%d" % s, range(1,16)) ]
    def __init__(self,page="./D_LOTFAC.HTM"):
        LoteriasParser.__init__(self,page)


if __name__ == '__main__':
    mp = MegasenaParser()
    from pprint import pprint
    pprint(mp.concursos)
    lp = LotofacilParser()
    pprint(lp.concursos)

