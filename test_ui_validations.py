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
		assert email == " mentor@rahulshettyacademy.com" #Fail Scenario





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
	#With the above code, we would have logged into the page.