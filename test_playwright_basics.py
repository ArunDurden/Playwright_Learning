from playwright.sync_api import Playwright, Page, expect

"""playwright & page are global fixtures defined in the Playwright & Page classes respectively, since they are 
global fixtures they need not be imported but the reason I've imported them is to get the suggestions of the object
they return in the test functions - To get playwright. & page. suggestions."""

def test_browser_launcher(playwright:Playwright):
	browser = playwright.chromium.launch(headless=False)
	browser.new_context()
	page = browser.new_page()
	page.goto("https://www.wikipedia.org/")
	input("Blocking so the browser window doesn't disappear like Vaama Minnalu. Press Enter")

	"""playwright:Playwright indicates that the playwright fixture comes from the Playwright class.
	headless=False runs automation with the window, headless=True which is the default option 
	runs automation without the window.
	Flow:
	Browser object created --> A context inside that browser object created to work --> In the browser object, 
	page object gets created & finally URL is searched.
	
	FYI, new_context() method creates a new temporary browsing session"""

def test_browser_launcher_shortcut(page:Page):
	page.goto("https://www.wikipedia.org/")
	input("Blocking so the browser window doesn't disappear like Vaama Minnalu. Press Enter")

	"""page fixture is the shortcut for the code inside the above test_browser_launcher function cause it simplifies
	the process of creating a browser, context & page object but the downside is it creates the browser object with Chromium
	engine which can only run automation on Chrome & MS Edge and can also run only on headless mode/ No window - if this is 
	your requirement this can be used or else the above function is preferred. But still this can be run with modified 
	configuration by clicking on the run icon besides the test function in the IDE or by doing something like this -
	'pytest test_playwright_basics.py::test_browser_launcher_shortcut -s --headed' """

def test_playwright_locators(playwright:Playwright):
	browser = playwright.chromium.launch(headless=False)
	browser.new_context()
	page = browser.new_page()
	page.goto("https://rahulshettyacademy.com/loginpagePractise/")

	page.get_by_label("Username:").fill("rahulshettyacademy")
	page.get_by_label("Password:").fill("learning")
	"""get_by_label is one of the locator strategies in Playwright with this label tag element can be located &
	through that the associated textbox can be located and the fill method is used on the returned object to fill 
	the textbox. There is a downside to this as for this get_by_label to work the intended label element should have the
	input tag element inside it in the webpage like this - <label>Username <input></label> so that the textbox can be 
	filled.
	 
	Or for attribute of the label element should be same as the id attribute of the input element so that the two 
	elements are associated like this - 
	<label for="username">Username</label>
	<input id="username">
	
	AND OFCOURSE INSPECT TOOL IS USED TO VIEW THE HTML HIERARCHY & WHAT NOT."""

	page.get_by_role("combobox").select_option("consult")
	"""get_by_role is an another locator strategy in Playwright with this we can locate an element using its role/ type
	Here I'm trying to locate a combobox, once located using select_option method on the returned object to select the 
	'Consultant' option - 'Consultant' is what shown on the UI but to select that option the value attribute of the said 
	option should be used as the argument here."""

	# page.locator(".text-info").check()
	page.locator("#terms").check()
	"""locator is an another locator strategy in Playwright and arguably very usable one so this lets us locate elements 
	using the CSS locators like class, id, tag etc.
	Here I've used the id to locate the checkbox and used check method on that to check the checkbox."""

	page.get_by_role("button", name="Sign In").click()
	"""When we use some locator strategies to locate a particular element, we might come across many elements. Typically
	a webpage might have more than 1 button in such case to access the intended element we should use name parameter
	to precisely locate the intended element"""
	input("Blocking so the browser window doesn't disappear like Vaama Minnalu. Press Enter")

def test_playwright_autowait(playwright:Playwright):
	browser = playwright.chromium.launch(headless=False)
	browser.new_context()
	page = browser.new_page()
	page.goto("https://rahulshettyacademy.com/loginpagePractise/")
	page.get_by_label("Username:").fill("rahulshettyacademy")
	page.get_by_label("Password:").fill("leaninggh")
	# page.get_by_label("Password:").fill("learning")
	page.get_by_role("combobox").select_option("consult")
	page.locator("#terms").check()
	page.get_by_role("button", name="Sign In").click()
	expect(page.get_by_text("Incorrect username/password.")).to_be_visible()

	"""So what I've done here is purposefully gave the wrong credential so that login fails which brings up the label -
	Incorrect username/password. after some time, so we have to wait before asserting that it has shown up. With 
	Selenium/ Appium that's what we do. 
	
	But Playwright offers a very powerful feature - Auto Wait that waits till a 
	default timeout of 5 seconds - 
	1. before performing an action on the found element
	2. when verifying a condition.
	
	1. Auto Wait feature when performing an action - this actually depends on the action, according to the action that's 
	going to be performed on the found elements - checks performed on the element changes,
	For a click action, Playwright uses the Auto Wait feature & waits till the following checks are satisfied before it 
	performs the action
	1. element is Visible
	2. element is Stable, as in not animating or completed animation
    3. element Receives Events, as in not obscured by other elements
	4. element is Enabled
	
	And this varies depending on the action that's going to be performed.
	We've seen this every time we locate elemnt & perfomr some kinda action.
	
	2. Auto Wait feature when verifying a condition - Playwright auto waits before verifying a condition & internally
	makes assertion using 'expect'. In this case, we've 
	expect(page.get_by_text("Incorrect username/password.")).to_be_visible()
	
	This tries to locate the element with text 'Incorrect username/password.' & waits for it be visible till the timeout.
	Once timed out, verifies the element is present & visible - If it is, PASS. Else, it is FAIL.
	
	If you run this function, test will pass as wrong login would be attempted & the 'Incorrect username/password.' 
	message will show up on the webpage.
	
	To check out the fail scenario, uncomment out the commented line & run the function.
	Also I've introduced new locator strategy here - get_by_text which locates an element using its text.
	
"""
	input("Blocking so the browser window doesn't disappear like Vaama Minnalu. Press Enter")

def test_playwright_firefox(playwright:Playwright):
	firefox_browser = playwright.firefox.launch(headless=False)
	firefox_browser.new_context()
	page = firefox_browser.new_page()
	page.goto("https://rahulshettyacademy.com/loginpagePractise/")
	page.get_by_label("Username:").fill("rahulshettyacademy")
	page.get_by_label("Password:").fill("learning")
	page.get_by_role("combobox").select_option("consult")
	page.locator("#terms").check()
	page.get_by_role("button", name="Sign In").click()
	input("Blocking so the browser window doesn't disappear like Vaama Minnalu. Press Enter")

	"""playwright.firefox.launch is used to launch firefox browser like how playwright.chromium.launch
	is used to launch Chrome & MS Edge browsers."""
