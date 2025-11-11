from time import sleep

from playwright.sync_api import Playwright, expect
from pytest_playwright.pytest_playwright import browser


def test_playwright_element_level_locators(playwright:Playwright):
	browser = playwright.chromium.launch(headless=False)
	browser.new_context()
	page = browser.new_page()
	page.goto("https://rahulshettyacademy.com/loginpagePractise/")
	page.get_by_label("Username:").fill("rahulshettyacademy")
	page.get_by_label("Password:").fill("learning")
	page.get_by_role("combobox").select_option("consult")
	page.locator("#terms").check()
	page.get_by_role("button", name="Sign In").click()

	#With the above code, we would have logged into the page.

	iphone_card = page.locator("app-card").filter(has_text="iphone X")
	iphone_card.get_by_role("button").click()

	blackberry_card = page.locator("app-card").filter(has_text="Blackberry")
	blackberry_card.get_by_role("button").click()

	"""In the website, there are 4 products displayed with card elements. I've located tehm using locator method &
	applied 'filter' method which gives exactly the one/ ones we want. I've used 'has_text' parameter here so 
	iphone_card	variable will have the card object with 'iphone X' text & blackberry_card variable will have the card 
	object with 'Blackberry' text.
	
	Once, we get our hands on the needed cards, I've used get_by_role method on the cards - THIS IS LOCATING CHILD 
	ELEMENTS WITHIN A PARENT ELEMENT SCOPE.
	When we use a locating strategy like get_by_text on a page, it gets searched throughout the webpage.
	When we use a locating strategy like get_by_text on an element, it gets searched within that element's children."""
	# input()
	page.get_by_text("Checkout").click()
	"""Webpage by now would have Checkout ( 2 ) as we've added 2 items into the cart but I'm here only providing 
	'Checkout' as the argument to the get_by_text instead of the whole thing 'Checkout ( 2 )' to locate the element 
	with that text- get_by_text will still work as it only needs partial text to locate an element."""

	# expect(page.locator(".media-body")).to_have_count(2)
	"""This is straight forward what's happening here so I don't need to explain. One thing I wanna say is I've used
	SelectorsHub - a plugin on Chrome that counts the no of times a class is used with this I made sure added items in
	the cart is 2 as both the added items have this class - '.media-body'."""

	expect(page.locator("h4")).to_have_text(["iphone X", "Blackberry"])
	"""This verifies that 'iphone X' & 'Blackberry' are added to the cart. To see the fail scenario, uncomment the
	 commented input()"""
	input("Blocking so the browser window doesn't disappear like Vaama Minnalu. Press Enter")

def test_playwright_child_windows_tabs(playwright:Playwright):
	browser = playwright.chromium.launch(headless=False)
	browser.new_context()
	page = browser.new_page()
	page.goto("https://rahulshettyacademy.com/loginpagePractise/")

	with page.expect_popup() as new_tab_info:
		page.locator(".blinkingText").click()
		new_tab = new_tab_info.value
		text = new_tab.locator(".red").text_content()
		# print(text.split(" "))
		text_list = text.split(" ")
		email = text_list[4]
		print(email)
		assert email == "mentor@rahulshettyacademy.com" #Pass Scenario
		# assert email == " mentor@rahulshettyacademy.com" #Fail Scenario

	"""We've seen opening a new webpage in the same window/ tab of the browser we could still access the elements of the
	newly opened webpage in the same window/ tab using the og page object.
	
	But to access the elements of the webpage opened in the new window/ tab, a new pge object should be created.
	Playwright provides a event listener to listen for new popups in the current page we can do this using 
	page.expect_popup() method, it is best to use this in the with context in python like I've done here.
	
	In the code below the with context, it keeps on listening for new popups once a new popup/ page gets opened in a 
	new window/ tab, the new window/ tab info gets loaded on the given variable here - new_tab_info, from that we can 
	access value property to get the new window/ tab object with which we can access elements of the new window/ tab."""

	# input("Blocking so the browser window doesn't disappear like Vaama Minnalu. Press Enter")
	sleep(5)

def test_playwright_placeholder_locator(playwright:Playwright):
	browser = playwright.chromium.launch(headless=False)
	browser.new_context()
	page = browser.new_page()
	page.goto("https://rahulshettyacademy.com/AutomationPractice/")

	expect(page.get_by_placeholder("Hide/Show Example")).to_be_visible() #Asserting that the text box is visible.
	"""get_by_placeholder is an another Playwright locator that locates an element using the placeholder text. Here the
	'Hide/Show Example' is a placeholder text for a textbox. I'm asserting that it's visible on the webpage with
	expect function."""

	page.get_by_role("button", name="Hide").click() #Hiding the text box.
	expect(page.get_by_placeholder("Hide/Show Example")).to_be_hidden() #Asserting that the text box is hidden.

def test_playwright_handling_alerts(playwright:Playwright):
	browser = playwright.chromium.launch(headless=False)
	browser.new_context()
	page = browser.new_page()
	page.goto("https://rahulshettyacademy.com/AutomationPractice/")

	page.on("dialog", lambda dialog : dialog.accept())
	"""In Playwright, 'on' method of the page object is used to handle alerts in the browsers, we know in JavaScript
	we can raise alerts like this alert("Something to be shown); this is outside of the webpage thus this is beyond the
	scope of Automation frameworks like Playwright & Selenium. But Playwright offers a neat trick to handle the alerts
	with this on method. Playwright doesn't offer any validation methods to validate the alerts but we can still 
	develop logic hmm something like taking a screenshot to make sure alert popped up??
	
	Anyway, back to on method, this method is set before as an event listener, it takes 2 arguments - event & the
	callback function/ eventhandler function that should be called when event occurs.
	
	Alerts are dialog boxes, so dialog is given as str for event & to shorten the function code - lambda expression is 
	used/
	
	Lambda expression is used in Python to create anonymous/ no name functions that take parameter and then runs just 
	like any other function syntax:- lambda <parameter>: <code to be executed>
	
	Here on method is set on the page to accept any alerts that may appear on this page."""
	page.get_by_role("button", name="Confirm").click() #Triggers the alert

def test_playwright_handling_frames(playwright:Playwright):
	browser = playwright.chromium.launch(headless=False)
	browser.new_context()
	page = browser.new_page()
	page.goto("https://rahulshettyacademy.com/AutomationPractice/")

	frame = page.frame_locator("#courses-iframe")
	frame.get_by_role("link", name="Learning paths").click()
	expect(frame.locator("body")).to_contain_text("SDET Automation Engineer – PYTHON")

	"""In websites, frames are webpage embedded inside a webpage. In Playwright to locate the frame, 'frame_locator' method of the
	page object should be used which will return that frame & that frame object can be used to access elements
	inside that frame."""


def test_playwright_handling_hover_button_click(playwright:Playwright):
	browser = playwright.chromium.launch(headless=False)
	browser.new_context()
	page = browser.new_page()
	page.goto("https://rahulshettyacademy.com/AutomationPractice/")

	mouse_hover_button = page.locator("#mousehover")
	mouse_hover_button.hover()
	"""In Playwright, hover method is user to hover over a method."""
	page.get_by_role("link", name="Top").click()
	input("Blocking so the browser window doesn't disappear like Vaama Minnalu. Press Enter")


def test_playwright_handling_tables(playwright:Playwright):
	browser = playwright.chromium.launch(headless=False)
	browser.new_context()
	page = browser.new_page()
	page.goto("https://rahulshettyacademy.com/seleniumPractise/#/offers")

	print(f'th_count: {page.locator("th").count()}')

	header_list = page.locator("th").all_text_contents()
	print(f"header_list: {header_list}")

	veg_fruit_name_index = header_list.index("Veg/fruit name")
	print(f"veg_fruit_name_index: {veg_fruit_name_index}")

	price_index = header_list.index("Price")
	print(f"price_index: {price_index}")

	# tr_objects_inside_tbody = page.locator("tbody").locator("tr")
	# tr_objects_inside_tbody_count = tr_objects_inside_tbody.count()
	# print(f"tr_objects_inside_tbody_count: {tr_objects_inside_tbody_count}")
	#
	# rice_amount_validated = False
	# for index in range(tr_objects_inside_tbody_count):
	# 	print(index)
	#
	# 	td_objects = tr_objects_inside_tbody.nth(index).locator("td")
	# 	td_objects_count = td_objects.count()
	#
	# 	for i in range(td_objects_count):
	# 		# print(td_objects.nth(i).text_content())
	#
	# 		# if i == 0:
	# 		if i == veg_fruit_name_index:
	# 			veg_fruit_name = td_objects.nth(i).text_content()
	# 			print(f"veg_fruit_name: {veg_fruit_name}")
	# 			if veg_fruit_name != "Rice":
	# 				break
	#
	# 		# if i == 1:
	# 		if i == price_index:
	#
	# 			# rice_amount = td_objects.nth(i)
	# 			rice_amount = td_objects.nth(i).text_content()
	# 			print(f"rice_amount: {rice_amount}")
	#
	# 			expect(td_objects.nth(i)).to_have_text("37") #Pass Scenario
	# 			# expect(td_objects.nth(i)).to_have_text("34") #Fail Scenario
	# 			print("Execution Came Here")
	# 			rice_amount_validated = True
	#
	# 	if rice_amount_validated:
	# 		break

	rice_row = page.locator("tr").filter(has_text="Rice")
	print(rice_row)


	td_object = rice_row.locator("td")
	"""Once, we locate the rice_row which is a <tr> tag in html source code of the webpage & has 3 <td> tags, we're 
	limiting the scope of the search by calling .locator("td") on the rice_row, so basically the playwright tries to 
	find <td> tag inside rice_row <tr> tag only."""

	print(f"td_object: {td_object}")
	print(f"td_object_type: {type(td_object)}")
	print(f"Rice's Price: {td_object.nth(price_index).text_content()}")
	# expect(td_object.nth(price_index)).to_have_text("37") #Pass Scenario
	expect(td_object.nth(price_index)).to_have_text("34") #Fail Scenario

	"""Here, td_object is a Locator object which has nth method which will give the item from the Locator object. Here, 
	td_object has 3 items we're accessing 2nd item with price_index - 1 which is the value of the Price column for the
	rice row, we get that text & compare it with expected text."""


"""Playwright offers a code generator tool in which we can perform actions on the browser like usual, playwright will
record and generate code for our actions, we can use that code to run automation tests. But in most cases, it will be
static so we will be developing the logic & everything so it can be used to get some locators. 

'playwright codegen' is the command for this. This is similar to Appium Inspector where we can perform actions & it'll
generate code for us."""