const puppeteer = require("puppeteer");
const createCsvWriter = require('csv-writer').createObjectCsvWriter;
const csvWriter = createCsvWriter({
  path: 'out2.csv',
  header: [
    {id: 'itemUrl', title: 'ItemUrl'}
  ]
});

const asyncPuppeteer = async () => {
    const browser = await puppeteer.launch({
        headless: false,
        slowMo: 250,
    });
    const page = await browser.newPage();
    await page.goto("https://www.ebay.com/sch/i.html?_from=R40&_nkw=nike+blazer+x+sacai+x+kaws+red+men%27s+shoes&_sacat=0&LH_TitleDesc=0&rt=nc&LH_Sold=1&LH_Complete=1");
  
    headings = await page.evaluate(() => {
        headings_elements = document.querySelectorAll("a.s-item__link");
        headings_array = Array.from(headings_elements);
        headings_array.map(heading => {
            var dict = {};
            return dict['itemUrl'] = heading.href;
        });
    });
    console.log(headings);
    await browser.close();
  };



(async () => {
    const data = await asyncPuppeteer();
    console.log(data);
    await csvWriter
    .writeRecords(data)
    .then(()=> console.log('The CSV file was written successfully'));
})();