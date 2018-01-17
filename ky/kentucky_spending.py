import requests
from requests.adapters import HTTPAdapter
from scrapy import Selector
import csv

#--------------------define variables-------------------
OUTPUT_FILE = 'kentucky_spending.csv'
MAX_ROWS = [
    {'year': '2007'},
    {'year': '2008'},
    {'year': '2009'},
    {'year': '2010'},
    {'year': '2011'},
    {'year': '2012'},
    {'year': '2013'},
    {'year': '2014'},
    {'year': '2015'},
    {'year': '2016'},
    {'year': '2017'},
    {'year': '2018'}
]
START_YEAR = '2007'
START_ROW = 1
#-------------------------------------------------------

#--------------------define global functions------------
def makeCookieString(cookie_dic):
    return "; ".join([str(key) + "=" + str(cookie_dic[key]) for key in cookie_dic]) + ';'

# -----------------------------------------------------------------------------------------------------------------------

class KansasSalariesScraper:
    def __init__(self,
                 base_url='https://transparency.ky.gov/Pages/default.aspx',
                 data_url='https://secure.kentucky.gov/OpenDoorWebApi/v1/SpendingAndVendorDetail/Get'
                 ):
        # define session object
        self.session = requests.Session()
        self.session.mount('https://', HTTPAdapter(max_retries=4))

        # set proxy
        # self.session.proxies.update({'http': 'http://127.0.0.1:40328'})

        # define urls
        self.base_url = base_url
        self.data_url = data_url

    def GetSpendingData(self, year, start, limit=10000):
        # set post data
        params = {}
        params['dataGroupingView'] = 'BranchView'
        params['requestYear'] = year
        params['branchCode'] = ''
        params['cabinetCode'] = ''
        params['departmentCode'] = ''
        params['classCode'] = ''
        params['objectCode'] = ''
        params['vendorName'] = ''
        params['beginDate'] = ''
        params['endDate'] = ''
        params['maxReturnRows'] = str(limit)
        params['startingIndex'] = str(start)

        # set url
        url = self.data_url

        # get request
        ret = self.session.get(url, params=params)

        if ret.status_code == 200:
            # print(ret.json())
            return(ret.json())
        else:
            print('fail to get spending data')
            return None

    def WriteHeader(self):
        # set headers
        header_info = []
        header_info.append('name')
        header_info.append('date_of_service')
        header_info.append('year')
        header_info.append('cabinet')
        header_info.append('department')
        header_info.append('classification')
        header_info.append('item_name')
        header_info.append('amount')

        # write header into output csv file
        writer = csv.writer(open(OUTPUT_FILE, 'w'), delimiter=',', lineterminator='\n')
        writer.writerow(header_info)

    def WriteData(self, data):
        # write data into output csv file
        writer = csv.writer(open(OUTPUT_FILE, 'a'), delimiter=',', lineterminator='\n')
        writer.writerow(data)

    def Start(self):
        # write header into output csv file
        self.WriteHeader()

        flag = False
        limit = 10000
        for one in MAX_ROWS:
            year = one['year']

            start = 1
            if year == START_YEAR:
                start = START_ROW
                flag = True

            if flag == False: continue

            while(True):
                # get salary data
                print('getting %s spending data from %s for %s...' % (str(limit), start, year))
                ret = self.GetSpendingData(year, start, limit)
                spending_data = ret["spendingVendorDetails"]
                max_count = ret["totalVendorRecordCount"]

                if len(spending_data) <= 0: break

                print(len(spending_data))

                for spending_info in spending_data:
                    # write data into output csv file
                    data = []
                    data.append(spending_info['vendorName'])
                    data.append(spending_info['dateOfServiceFormated'])
                    data.append(spending_info['fiscalYear'])
                    data.append(spending_info['cabinetName'])
                    data.append(spending_info['departmentName'])
                    data.append(spending_info['className'])
                    data.append(spending_info['objectName'])
                    data.append('$' + str(spending_info['amount']))
                    self.WriteData(data)

                start += limit
                if start > max_count: break

#------------------------------------------------------- main -------------------------------------------------------

def main():
    # create scraper object
    scraper = KansasSalariesScraper()

    # start to scrape
    scraper.Start()

if __name__ == '__main__':
    main()
