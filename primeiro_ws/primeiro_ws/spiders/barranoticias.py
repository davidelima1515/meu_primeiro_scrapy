import scrapy

class BarraSpider(scrapy.Spider):
    name = "barra__noticias"
    start_urls= [

        "https://www.barradocordanoticia.com/"
       
        ]

    def parse(self, response):
        links = response.xpath('//h1/a/@href').getall()
        for link in links:
            yield scrapy.Request(
                response.urljoin(link), 
                callback= self.parse_new
                ) 
        
        next_page = response.css('a.larger::attr(href)').extract_first() 
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(
                next_page,
                callback=self.parse
            )
        
    def parse_new(self, response):
        titulo = response.css('header h1::text').extract_first() 
        data = response.css('span a time::text').extract_first()
        autor = response.css('span a::Text').extract_first()
        
        yield {

            'autor':autor,
            'data':data,
            'titulo':titulo

        }

    