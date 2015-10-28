from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector, Selector
from scrapy.spider import BaseSpider
from scrapy.http import Request
from outdoortravelgear.items import BigCItem
import urlparse ,re, json, unicodecsv,csv
from scrapy.http.request import Request
f = open("Product_urls1.csv")
csv_file =  csv.reader(f)
urllist = []
catlist = []

for row in csv_file:
    urllist.append(row[0])
    catlist.append(row[1])

output = open("OutdoorGearStore.csv","wb")
mywriter = unicodecsv.writer(output)
header = ('Item Type','Product ID','Product Name','Brand Name','Price','Retail Price','Sale Price','Product Description','Product Code/SKU','Bin Picking Number','Category',
                 'Option Set','Product Availability','Current Stock Level','Free Shipping','Sort Order','Meta Description','Page Title',''
             'Product Image Description - 1','Product Image Is Thumbnail - 1',''
             'Track Inventory','Product Image Sort - 1','Product Image Sort - 2','Product Image Sort - 3','Product Image Sort - 4','Product Image Sort-5','Product Image Sort-6','Product Image Sort-7','Product Image Sort-8',
             'Product Image File - 1','Product Image File - 2','Product Image File - 3','Product Image File - 4','Product Image File - 5 ',
    'Product Image File - 6','Product Image File - 7','Product Image File - 8')
mywriter.writerow(header)
class OutdoorGear(CrawlSpider):
    
    name = "outdoortravelgear"
    allowed_domains = ["outdoortravelgear.com"]
    start_urls = [
        
        url for url in urllist
##        "http://www.outdoortravelgear.com/product-detail/dry-inside-sport-fit-short-sleeve-shirt-2012/dark-grey",
##        "http://www.outdoortravelgear.com/product-detail/trimm-direct-pants/khaki-black",        
    ]

    def parse(self, response):
       sel = Selector(response)
       for i in range(len(urllist)):
           if urllist[i] == response.url:
               category = catlist[i]
               break
            
       item = BigCItem()
       pname = sel.xpath("//div/div/h2/text()").extract()[1]       
       brandlist = sel.xpath("//select[@id='ctl00_uctrlHeader_selBrand']/option/text()").extract()[1:]
       for i in brandlist:           
           if i.lower() in pname.strip().lower():
               brandname = i
               break
       imagedescription = "Buy "+pname+" Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
       metadescription = "Get your hands on the "+pname +". Buy it Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"       
       mrp = sel.xpath("//div[@class='left mrpfont']/span[2]/text()").extract()[0].strip()
       sp = sel.xpath("//div[@class='left mrpfont']/span[2]/text()").extract()
       if sp:
           sp = sel.xpath("//div[@class='left mrpfont']/span[2]/text()").extract()[0].strip()
       else:
           sp = ''
       sku = sel.xpath("//div[@class='left']/text()").extract()[0].strip()+"ODTG"
       description = sel.xpath("//div[@class='product_content_left']").extract()[0]
       images = sel.xpath("//div[@id='Carousel']/ul/li/a/img/@src").extract()       
       sizelist = sel.xpath("//div[@id='ctl00_cphBody_divSize']/a/div[not(contains(@class,'Nosstock'))]/div/text()").extract()      
       colorlist = sel.xpath("//div[@class='color_list']/a/@href").extract()
       if len(colorlist)>1 or len(sizelist)>1:
           trackinventory = "By Option"
       else:
           trackinventory = "By Product"
       sortorder = -180-(float(mrp.replace(",",""))/100)       
       tup = ("Product","",pname,brandname,
           mrp,mrp,sp, #price
           description,sku,"OUTDOORTRAVELGEAR",category,pname,"7-10 Working days","100","N",sortorder,
           metadescription,imagedescription,imagedescription,"Y",trackinventory,
           "1","2","3","4","5","6","7","8")
       obj = list(tup)
       for url in images:
           obj.append("http://www.outdoortravelgear.com/"+url)    
       row = tuple(obj)
       mywriter.writerow(row)
       #printing first of the colors
       color = response.url.split("/")[-1].replace("-"," ")
       for size in sizelist:           
           row = ('SKU','','[S]Size= '+size +',[S]Color= '+color,"","","","","",
                  sku+color.replace(" ","")+size+"ODTG",'OUTDOORTRAVELGEAR',
                  "","","","100","","","","","","","","","","","","","","")

           ruletup = ('Rule','','[S]Size= '+size +',[S]Color= '+color,"","","","","",
                      sku+color.replace(" ","")+size+"ODTG",'OUTDOORTRAVELGEAR',
                  "","","","100","","","","","","","","","","","","","","")
           obj = list(ruletup)
           for url in images:
               obj.append("http://www.outdoortravelgear.com/"+url)        
           rulerow = tuple(obj)
           mywriter.writerow(row)
           mywriter.writerow(rulerow)
           