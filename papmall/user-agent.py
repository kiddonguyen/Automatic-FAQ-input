from seleniumbase import SB

with SB(uc=True) as sb:
    sb.open("https://www.google.com/gmail/about/")
    sb.click('a[data-action="sign in"]')
    sb.type('input[type="email"]', "NAME@gmail.com")
    sb.click('button:contains("Next")')
    sb.type('input[type="password"]', PASSWORD)
    sb.click('button:contains("Next")')
    sb.sleep(5)
