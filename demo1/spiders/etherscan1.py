# -*- coding: utf-8 -*-
import scrapy


# global sc_name1

class etherscan1Spider(scrapy.Spider):
    name = "etherscan1"

    # sc_name="default.sol"

    def __init__(self, name="etherscan1", sc_name="default.sol", sc_content="test"):
        self.name = name
        self.sc_name = sc_name
        self.sc_content = sc_content

    def start_requests(self):
        pre_url = 'https://etherscan.io/contractsVerified'
        contract_start_page = 2
        contract_end_page = 8
        for i in range(contract_start_page, contract_end_page):
            url = '{}/{}'.format(pre_url, i)
            # print(url)
            print("Adding page %s" % i + " for downloading!")
            # yield scrapy.Request(url=url, callback=self.parse)
            yield scrapy.Request(url=url, meta={
                'dont_redirect': True,
                'handle_httpstatus_list': [302]
            }, callback=self.parse)

    # def parse(self, response):
    #     for href in response.css("ul.directory.dir-col > li > a::attr('href')"):
    #         url = response.urljoin('https://etherscan.io', href.extract())
    #         print(url)
    #         yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse(self, response):
        page = response.url.split("/")[-1]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        # self.log('Saved file %s' % filename)

        addr_list = response.xpath('//td[1]/a[1]/@href').extract()
        addl_list = response.xpath('//td[1]/a[1]/text()').extract()
        name_list = response.xpath('//td[2]/text()').extract()

        baseurl = 'https://etherscan.io'
        # https: // etherscan.io / address / 0x3c200bf4ec426236f8b042f0f1380315aee4c7d1  # code
        urllist = []
        i = 0
        for addr in addr_list:
            filename = "SC" + "_" + name_list[i] + "_P" + page + "_" + addl_list[i] + ".sol"
            self.log('save file %s' % filename)
            newurl = '{}{}'.format(baseurl, addr)
            # nonlocal sc_name
            self.sc_name = filename
            # global sc_name1
            # sc_name1=filename
            # yield response.follow(newurl, self.parse_sc)
            yield scrapy.Request(url=newurl, meta={
                'dont_redirect': True,
                'handle_httpstatus_list': [302]
            }, callback=self.parse_sc)

            urllist.append(newurl)
            i = i + 1

        #print(urllist)

    def parse_sc(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        # print (response)
        sc_content = response.xpath('//div[@id=\'dividcode\']//pre[1]/text()').extract()
        # sc_content = response.xpath('//div[@id=\'dividcode\']').extract()
        # print (sc_content)
        sc_abstract = response.xpath('//pre[@id=\'js-copytextarea2\']/text()').extract()
        sc_name0 = response.xpath(
            '//div[@id=\'ContentPlaceHolder1_contractCodeDiv\']/div[2]/table/tr[1]/td[2]/text()').extract()
        # print(sc_name0)
        if (sc_name0 == []):
            print("error")
            sc_name = "err"
        else:
            sc_name = sc_name0[0].replace("\n", "")
        sc_addr = response.xpath('//*[@id="mainaddress"]/text()').extract()

        if (sc_addr == []):
            sc_addr0 = "erra"
            print("addr error")
        else:
            sc_addr0 = sc_addr[0]

        filename1 = "./sol/sc_" + sc_name + "_" + sc_addr0 + ".sol"
        filename2 = "./sol/sc_" + sc_name + "_" + sc_addr0 + ".ifsol"
        # if len(sc_content):
        with open(filename1, 'w') as f:
            if len(sc_content):
                f.write(sc_content[0])
                # f.write(sc_content[0])

        with open(filename2, 'w') as f:
            if len(sc_abstract):
                f.write(sc_abstract[0])
                # f.write(sc_abstract[0])

        self.log("writing " + filename1)
        # print(sc_addr,sc_name,sc_content,sc_abstract)
