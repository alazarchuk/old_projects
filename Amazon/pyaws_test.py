from pprint import pprint
import ecs

def get_infos(books):
 book_info = dict()
 for book in books:
     book_info[book.ASIN] = dict()
     for mtd in dir(book):
         if mtd[0] != '_':
             book_info[book.ASIN][mtd] = eval('book.%s' % mtd)
 return book_info

if __name__ == "__main__":
    ecs.setLicenseKey('0J356Z09CN88KB743582')
    #books = ecs.ItemSearch('python', SearchIndex='Books')
    books = ecs.ItemSearch('0465027814', SearchIndex='Books', ResponseGroup='TagsSummary,Tags,ItemAttributes,EditorialReview,Images,Similarities,PromotionalTag')
    pprint(get_infos(books))








