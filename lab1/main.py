import os
from lxml import etree


class Menu:
    def __init__(self, name, items=None):
        self.name = name
        self.items = items or []

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)

    def draw(self):
        print("\n"*2)
        print("-"*10, self.name, "-"*10)
        for item in self.items:
            item.draw()
        print("make your choice by typing a number below")

    def get_item(self, index):
        return self.items[index - 1]


class Item:
    def __init__(self, name, function=None):
        self.name = name
        self.function = function

    def draw(self):
        print("    " + self.name)


def scrawl_posolstva():
    print("start...")
    os.system("scrapy crawl posolstva")
    print("scrapy executed...")
    print("\n"*2)
    print("calculating max fragments on page: ")
    max_fragments = calculate_page_max_fragments('results/posolstva.xml')
    print('Maximum number of text fragments per page is %i' % max_fragments)
    print("\n" * 2)


def calculate_page_max_fragments(filename):
    root = None
    with open(filename, 'r', encoding="utf8") as file:
        root = etree.parse(file)

    max_fragments = 0
    for page in root.xpath('//page'):
        text_fragments_count = page.xpath('count(//fragment[@type="text"])')
        if text_fragments_count > max_fragments:
            max_fragments = text_fragments_count

    return max_fragments


def scrawl_odissey():
    remove_if_present("results/odissey.xml")
    print("start...")
    os.system("scrapy crawl odissey -o results/odissey.xml")
    print("scrapy executed...")
    save_to_html()
    print("saved to html!")
    print("\n" * 2)


def remove_if_present(filename):
    try:
        os.remove(filename)
    except OSError:
        print("%s not found" % filename)


def save_to_html():
    dom = etree.parse('results/odissey.xml')
    xslt = etree.parse('odissey.xslt')
    transform = etree.XSLT(xslt)
    newdom = transform(dom)
    with open('results/odissey.html', 'wb') as f:
        f.write(etree.tostring(newdom, pretty_print=True))


menu = Menu("Scrappy menu")
menu.add_item(Item("1.scrawl posolstva.org.ua", scrawl_posolstva))
menu.add_item(Item("2.scrawl odissey.kiev.ua", scrawl_odissey))
menu.add_item(Item("3.exit"))

isRunning = True
while isRunning:
    menu.draw()
    option = int(input())
    if option == 3:
        isRunning = False
        break
    menu.get_item(option).function()


