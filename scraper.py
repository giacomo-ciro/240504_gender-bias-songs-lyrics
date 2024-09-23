import pandas as pd
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ChartScraper:
        """
        
        A webscraper for the Italian music charts.
        
        """
        def __init__(self):

              self.df = pd.DataFrame({'Year': [], 'Week':[], 'Position':[], 'Title':[], 'Artist':[]})

              return


        def get_chart(self, Year, Week):
            """
            
            Fetches the HTML for the Italian music charts for a given
            year and week and returns a <Pandas.DataFrame>.

            """
            # Get HTML
            driver = webdriver.Chrome()
            driver.get(f"https://www.fimi.it/top-of-the-music/classifiche.kl#/charts/1/{Year}/{Week}")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "chart-section-table")))
            driver.find_element(By.XPATH, '//button[contains(text(), "Consenti tutti")]').click()
            driver.find_element(By.XPATH, '//a[contains(text(), "Singoli")]').click()
            outerHTML = driver.find_element(By.XPATH, '//div[@class = "tab-pane active"]').get_attribute('outerHTML')
            driver.quit()
            soup = BeautifulSoup(outerHTML)

            # Get DF
            df = pd.DataFrame({'Year': [], 'Week':[], 'Position':[], 'Title':[], 'Artist':[]})
            for i in soup.find_all(class_ = 'chart-section-element'):
                new_entry = {
                            'Year': Year,
                            'Week': Week,
                            'Position': i.find(class_='c4').contents[0],
                            'Title': i.find(class_='chart-section-element-title').contents[0],
                            'Artist': i.find(class_='chart-section-element-author').contents[0]
                            }
                df = pd.concat([df, pd.DataFrame(new_entry, index = [0])], ignore_index=True)

            return df


        def scrape(self, startYear, endYear):
            """
            
            Scrapes the Italian music charts for a given range of years and returns a <Pandas.DataFrame>
            
            """
            years = [startYear] if startYear == endYear else list(range(startYear, endYear+1))

            for Year in years:
                print(Year)

                for Week in range(1, 53):
                    print(f'    {Week}')
                    try:
                        new_df = self.get_chart(Year, Week)
                        self.df = pd.concat([self.df, new_df], ignore_index=True)
                        print('Year {Year}, Week {Week} available. Fetching...')
                    except:
                         print('Error: Year {Year}, Week {Week} not available. Moving to the next.')

            print(f'Scraped {self.df.shape[0]} total songs')
            return self.df.head()