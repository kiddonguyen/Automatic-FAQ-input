const {
  Builder,
  By,
  Key,
  until,
  WebElement,
  ExpectedConditions,
  wait,
} = require("selenium-webdriver");
const assert = require("assert");

// (async function example() {
//   let driver = await new Builder().forBrowser('chrome').build();
//   try {
//     await driver.get('http://www.google.com/ncr');
//     await driver.findElement(By.name('q')).sendKeys('webdriver', Key.RETURN);
//     await driver.wait(until.titleIs('webdriver - Google Search'), 1000);
//   } finally {
//     await driver.quit();
//   }
// })();

async function login() {
  let driver = await new Builder().forBrowser("chrome").build();
  driver.manage().window().maximize();
  let dashboardURL = "https://www.thecanadianimmigration.org/dashboard/";
  try {
    await driver.get(dashboardURL);
    await driver.findElement(By.id("email"));
    // let username = await driver.findElement(By.id("email"));
    // driver.findElement(By.id('password'));
    // WebElement password = driver.findElement(By.id("password"));
    let username = await driver.wait(
      until.elementLocated(By.id("email")),
      10000
    );
    // await driver.wait(until.elementIsVisible(By.id('email')), 10000)
    await username.sendKeys("thanhnguyen@mobcec.com");

    await driver.findElement(By.id("password"));
    let password = await driver.wait(
      until.elementLocated(By.id("password")),
      10000
    );
    await password.sendKeys("0967614208nN@");

    await driver.findElement(By.id("btn-login"));
    let btnlogin = await driver.wait(
      until.elementLocated(By.id("btn-login")),
      10000
    );
    await btnlogin.click();

    await driver.get(`${dashboardURL}cloud-upload`);
    await driver.findElement(By.id("upload-files"));
    let btnUpload = await driver.wait(
      until.elementLocated(By.id("upload-files")),
      100009
    );
    await btnUpload.sendKeys(
      "D:/Workspace/LEARNING-GITHUB/New folder/selenium/beautiful-view-at-the-elephant-rock-alula-saudi-arabia-h2-658x435.img \n D:/Workspace/LEARNING-GITHUB/New folder/selenium/1.txt"
    );

    await driver.findElement(By.xpath("//button[@type='submit']"));
    let btnUploadFiles = await driver.wait(
      until.elementLocated(By.xpath("//button[@type='submit']")),
      100000
    );
    await btnUploadFiles.click();

    await driver.findElements(By.xpath("//div[@class='alert-success']/a"));
    let allImgLinks = await driver.wait(
      until.elementLocated(By.xpath("//div[@class='alert-success']/a")),
      100000
    );
    // await console.log(allImgLinks)
    let result = await allImgLinks.map((index, link) => {
      return link.getAttribute("href");
    });
    /* 
      let result = document.querySelectorAll('.alert-success');
let arr = [];
let random = result.forEach((link, index) => {
    if (index > 0) {
        arr.push(link);
    }
})
console.log(arr);
    */
    // console.log(result);
    // driver.execute_script(`console.log('${result}');`)
    driver.execute_script(`console.log(1);`);
    /* 
      [' https://dwukht46mtp9x.cloudfront.net/uploads/beau…rock-alula-saudi-arabia-h2-658x435-1678813502.img', ' https://dwukht46mtp9x.cloudfront.net/uploads/1-1678813503.txt']
    
    */

    // let input = await driver.findElement(By.id("upload-files"));
    // console.log(input);

    // wait.until(ExpectedConditions.visibilityOfElementLocated(By.xpath("//input[@type='password']")));
    // WebElement elementpwd = driver.findElement(By.xpath("//input[@type='password']"));
    // elementpwd.sendKeys("123");
    /* 
      driver.manage().window().maximize();
    driver.get("http://www.gmail.c‌​om"); 
    WebElement elementid = driver.findElement(By.id("identifierId")); 
    elementid.sendKeys(""); 
    WebElement elementnxt = driver.findElement(By.id("identifierNext")); 
    elementnxt.click();
    WebDriverWait wait = new WebDriverWait(driver, 100);
    wait.until(ExpectedConditions.presenceOfElementLocated(By.xpath("//input[@type='password']")));
    wait.until(ExpectedConditions.visibilityOfElementLocated(By.xpath("//input[@type='password']")));
    WebElement elementpwd = driver.findElement(By.xpath("//input[@type='password']"));
    elementpwd.sendKeys("123");
    */
    // username.sendKeys('thanhnguyen@mobcec.com');
    // password.sendKeys('your_password');
    // login.click();
  } finally {
    // await driver.quit();
  }
}
login();
