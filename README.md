# loginvsi

Objective/scenario: (pretend that) “We need to make sure the Selenium drivers we have available to the test automation host are up to date so the test automation can still function.<br />
If the Selenium version we have is older than the browser version installed on the test host then the automation might not run successfully.
If a newer Selenium web driver version exists online then we need to download it.”<br />

Write a script that:<br />

Looks at the version files in the Selenium zip folder’s nested folders, and logs these version numbers<br />
Locates and logs the newest version available link1 (the more basic page therein is link2)<br />
Compares the highest version number to what was in the Selenium zip folder<br />
Logs if the highest version numbers both from the Selenium zip folder and the website match or not<br />
If there is a newer version on the  website then download it, logging when the download is successful and complete<br />
If there isn’t a newer version then log that there isn’t a newer version.<br />


link1 - https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/

link2 - https://msedgewebdriverstorage.z22.web.core.windows.net/
