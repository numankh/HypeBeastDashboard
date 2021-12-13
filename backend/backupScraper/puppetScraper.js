const puppeteer = require("puppeteer");
 
(async () => {
  const browser = await puppeteer.launch({
      headless: false,
      slowMo: 7000,
  });
  const page = await browser.newPage();
  var res = [];

  for (let pageNumber = 2; pageNumber < 4; pageNumber++) {
    console.log("Page number: " + pageNumber);
    let url = "https://www.ebay.com/sch/i.html?_from=R40&_nkw=nike+blazer+x+sacai+x+kaws+red+men%27s+shoes&_sacat=0&LH_TitleDesc=0&rt=nc&LH_Sold=1&LH_Complete=1%22&_pgn=";
    await page.goto(url.concat(pageNumber));
    
    headings = await page.evaluate(() => {
      // headings_elements = document.querySelectorAll("li.s-item.s-item__pl-on-bottom");
      // headings_elements = document.querySelectorAll("span.POSITIVE");
      // headings_elements = document.querySelectorAll("span.vi-inl-lnk.vi-original-listing");
      headings_elements = document.querySelectorAll("a.s-item__link");

      // total items where bid was offered: span.s-item__bids.s-item__bidCount
      // total items where offer or buy it now was offered: span.s-item__purchase-options.s-item__purchaseOptions

      headings_array = Array.from(headings_elements);
      return headings_array.map(heading => heading.href);
    });
    console.log(headings);
    res.concat(headings);
  }
  console.log(res);
  await browser.close();
})();