import urllib.request
from bs4 import BeautifulSoup



def get_description(url):
    req = urllib.request.Request(url, headers={'User-Agent': "Magic Browser"})
    page = urllib.request.urlopen(req)
    soup = BeautifulSoup(page, 'html.parser')
    content_list = soup.select('.content')
    # content_str = ''
    # for x in content_list:
    #     content_str += x.text + '\n'
    # final = ''
    # for x in range(len(soup_str)):
    #     if ord(soup_str[x]) == 8217:
    #         if soup_str[x - 1] != ' ' and soup_str[x + 1] != ' ':
    #             final += "'"
    #     else:
    #         final += soup_str[x]
    # return final
    # return content_str
    return content_list

def main():
    url = "https://www.youtube.com/watch?v=7pUJuDtBZe8"
    print(get_description(url))

if __name__ == "__main__":
    main()