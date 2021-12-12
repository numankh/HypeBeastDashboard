const puppeteer = require("puppeteer");
 
(async () => {
  const browser = await puppeteer.launch({
      headless: false,
      slowMo: 250,
  });
  const page = await browser.newPage();
//   await page.goto("https://www.ebay.com/sch/i.html?_from=R40&_nkw=nike+blazer+x+sacai+x+kaws+red+men%27s+shoes&_sacat=0&LH_TitleDesc=0&rt=nc");
 
  await page.goto("https://www.ebay.com/sch/i.html?_from=R40&_nkw=nike+blazer+x+sacai+x+kaws+red+men%27s+shoes&_sacat=0&LH_TitleDesc=0&rt=nc&LH_Sold=1&LH_Complete=1");
  // await page.goto("https://www.ebay.com/itm/265443428876?hash=item3dcda94a0c:g:~7EAAOSwRCthsWaD");


  headings = await page.evaluate(() => {
    // headings_elements = document.querySelectorAll("li.s-item.s-item__pl-on-bottom");
    // headings_elements = document.querySelectorAll("span.POSITIVE");
    headings_elements = document.querySelectorAll("a.s-item__link");
    // headings_elements = document.querySelectorAll("span.vi-inl-lnk.vi-original-listing");

    headings_array = Array.from(headings_elements);
    return headings_array.map(heading => heading.href);
  });
  console.log(headings);
  await browser.close();
})();