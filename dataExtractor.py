# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 00:09:26 2018

@author: arash
"""
from selenium import webdriver
import pandas as pd
import ast
from operator import itemgetter


class DataExtractor:

    def __init__(self):
        self.ready = False
        self.monthsToNum = {'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05', 'June': '06', 'July': '07',
          'August': '08', 'September': '09', 'October': '10', 'November': '11', 'December': '12'}
    def extractData(self,browser):

        if (browser == 'Firefox'):
            print('Running Geckodriver')
            self.driver = webdriver.Firefox(executable_path='/home/arash/cMod/drivers/linux64/geckodriver')
        else:
            self.driver = webdriver.Chrome()
        self.grid = [[{},{},{},{},{}],[{},{},{},{},{}],[{},{},{},{},{}],[{},{},{},{},{}],[{},{},{},{},{}]]
        self.matrix = [[[],[],[],[],[],],[[],[],[],[],[],],[[],[],[],[],[],],[[],[],[],[],[],],[[],[],[],[],[],]]
        print('loading webpage..')
        self.driver.get("https://www.nytimes.com/crosswords/game/mini")
        print('webpage loaded')
        print('clicking the buttons')
        self.driver.find_element_by_css_selector('.buttons-modalButton--1REsR').click()
        self.driver.find_element_by_css_selector('li.Tool-button--39W4J:nth-child(2) > button:nth-child(1)').click()
        self.driver.find_element_by_css_selector('li.Tool-button--39W4J:nth-child(2) > ul:nth-child(2) > li:nth-child(3) > a:nth-child(1)').click()
        self.driver.find_element_by_css_selector('button.buttons-modalButton--1REsR:nth-child(2)').click()

        print('getting across clues')
        self.across = self.getClue('div.ClueList-wrapper--3m-kd:nth-child(1) > ol:nth-child(2)')
        print('getting down clues')
        self.down = self.getClue('div.ClueList-wrapper--3m-kd:nth-child(2) > ol:nth-child(2)')
        print('getting date')
        self.getDateOnline()
        self.across_dict = self.getDict(self.across)
        self.down_dict = self.getDict(self.down)
        print('extracting grid')
        self.extractGrid()
        print('saving')
        self.save()
        print('ready')
        self.ready = True

    def getDateOnline(self):
        self.full_date = self.driver.find_element_by_css_selector('.PuzzleDetails-date--1HNzj').text
        self.day = self.driver.find_element_by_css_selector('.PuzzleDetails-date--1HNzj > span:nth-child(1)').text
        self.date = self.full_date.replace(self.day + " ", "")
        self.temp = self.date.split(" ")[0]
        self.date = self.date.replace(self.temp, self.monthsToNum[self.temp])
        self.date = self.date.replace(" ","-").replace(",","")

    def getDateCSV(self,filePath):
        temp = filePath.split('/')[1]
        self.full_date = temp.split('_')[1].replace('.csv','')
        self.date = temp.split('_')[0]
        self.day = self.full_date.split(" ")[0]



    def getClue(self, selector):
        el = self.driver.find_element_by_css_selector(selector)
        el = el.find_elements_by_class_name('Clue-li--1JoPu')
        clue = []
        for i in range (0,len(el)):
            span = el[i].find_elements_by_tag_name('span')
            clue.append({'number' : int(span[0].text), 'clue' : span[1].text})
        clue = sorted(clue, key=itemgetter('number'))
        return clue

    def getDict(self, arr):
        clue = {}
        for i in arr:
            clue[i['number']] = i['clue']
        return clue

    def extractGrid(self):
        # add this - get a collection of all the cell elements
        cell_grid = self.driver.find_elements_by_css_selector('#xwd-board > g:nth-child(3) g')
        for i in range(1, 26):
            el = cell_grid[i - 1]  # change to this
            r = el.find_elements_by_tag_name('text')
            ## notes on data
            # len(r) == 0: it's a blank cell
            # len(r) == 1: it's cell without clue number. you can get the letter using r[0].text
            # len(r) == 2: it's cell with a clue number. r[1].text gives the letter, r[0].text gives the clue number

            row = (i - 1) // 5
            column = (i - 1) % 5
            if len(r) == 0:
                self.grid[row][column]['letter'] = '-'
                self.matrix[row][column] = '-'
            elif len(r) == 1:
                self.grid[row][column]['letter'] = str(r[0].text)
                self.matrix[row][column] = str(r[0].text)
            else:
                n = int(r[0].text)
                self.grid[row][column]['letter'] = str(r[1].text)
                self.matrix[row][column] = str(r[1].text)
                self.grid[row][column]['number'] = n

    def loadCSV(self,file):
        across = []
        down = []
        d = pd.read_csv(file, sep="&", encoding='utf-8', header=None )

        matrix = [[[],[],[],[],[],],[[],[],[],[],[],],[[],[],[],[],[],],[[],[],[],[],[],],[[],[],[],[],[],]]
        grid = [[{},{},{},{},{}],[{},{},{},{},{}],[{},{},{},{},{}],[{},{},{},{},{}],[{},{},{},{},{}]]
        for i in range (0,5):
            for j in range (0,5):
                x = ast.literal_eval(d[j][i])
                d[j][i] = x
                grid[i][j]['letter'] = x['letter']
                matrix[i][j] = x['letter']
                if 'number' in x:
                    grid[i][j]['number'] = x['number']
                    if 'across' in x:
                        across.append({'number' : x['number'], 'clue': x['across'], })
                    if 'down' in x:
                        down.append({'number' : x['number'], 'clue': x['down'], })

        down = sorted(down, key=itemgetter('number'))
        across = sorted(across, key=itemgetter('number'))

        self.data = d

        self.getDateCSV(file)
        self.grid = grid
        self.across = across
        self.down = down
        self.across_dict = self.getDict(self.across)
        self.down_dict = self.getDict(self.down)
        self.ready = True
        self.matrix = matrix

    def encode(self):
        data = [[{},{},{},{},{}],[{},{},{},{},{}],[{},{},{},{},{}],[{},{},{},{},{}],[{},{},{},{},{}]]
        for i in range (0,5):
            for j in range (0,5):
                data[i][j]['letter'] = self.grid[i][j]['letter']
                if 'number' in self.grid[i][j]:
                    n = self.grid[i][j]['number']
                    data[i][j]['number'] = n
                    if n in self.across_dict:
                        data[i][j]['across'] = self.across_dict[n]
                    if n in self.down_dict:
                        data[i][j]['down'] = self.down_dict[n]
        return data


    def save(self):
        data = self.encode()
        df = pd.DataFrame(data, dtype=None, copy=False)
        path = 'stored_crosswords/' + self.date + '_' + self.full_date + '.csv'
        df.to_csv(path, sep='&', encoding='utf-8', header=None, index =None )



