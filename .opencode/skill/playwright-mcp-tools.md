# Playwright MCP Tools

**Use this skill to check Playwright tools when needed, no need to query Playwright for checking tools if you have this skill.**

<details>
<summary><b>Core automation</b></summary>


- **browser_click**
  - Title: Click
  - Description: Perform click on a web page
  - Parameters:
    - `element` (string, optional): Human-readable element description used to obtain permission to interact with the element
    - `target` (string): Exact target element reference from the page snapshot, or a unique element selector
    - `doubleClick` (boolean, optional): Whether to perform a double click instead of a single click
    - `button` (string, optional): Button to click, defaults to left
    - `modifiers` (array, optional): Modifier keys to press
  - Read-only: **false**


- **browser_close**
  - Title: Close browser
  - Description: Close the page
  - Parameters: None
  - Read-only: **false**


- **browser_console_messages**
  - Title: Get console messages
  - Description: Returns all console messages
  - Parameters:
    - `level` (string): Level of the console messages to return. Each level includes the messages of more severe levels. Defaults to "info".
    - `all` (boolean, optional): Return all console messages since the beginning of the session, not just since the last navigation. Defaults to false.
    - `filename` (string, optional): File name to save the console messages to. Relative file names are resolved against the workspace root. If not provided, messages are returned as text.
  - Read-only: **true**


- **browser_drag**
  - Title: Drag mouse
  - Description: Perform drag and drop between two elements
  - Parameters:
    - `startElement` (string, optional): Human-readable source element description used to obtain the permission to interact with the element
    - `startTarget` (string): Exact target element reference from the page snapshot, or a unique element selector
    - `endElement` (string, optional): Human-readable target element description used to obtain the permission to interact with the element
    - `endTarget` (string): Exact target element reference from the page snapshot, or a unique element selector
  - Read-only: **false**


- **browser_drop**
  - Title: Drop files or data onto an element
  - Description: Drop files or MIME-typed data onto an element, as if dragged from outside the page. At least one of "paths" or "data" must be provided.
  - Parameters:
    - `element` (string, optional): Human-readable element description used to obtain permission to interact with the element
    - `target` (string): Exact target element reference from the page snapshot, or a unique element selector
    - `paths` (array, optional): Absolute paths to files to drop onto the element.
    - `data` (object, optional): Data to drop, as a map of MIME type to string value (e.g. {"text/plain": "hello", "text/uri-list": "https://example.com"}).
  - Read-only: **false**


- **browser_emulate_media**
  - Title: Emulate media features
  - Description: Emulate CSS media features for the page, for example switch between the light and dark color scheme. Omitted parameters are left unchanged; null clears an override.
  - Parameters:
    - `colorScheme` (optional): Emulates the prefers-color-scheme media feature
    - `reducedMotion` (optional): Emulates the prefers-reduced-motion media feature
    - `forcedColors` (optional): Emulates the forced-colors media feature
    - `contrast` (optional): Emulates the prefers-contrast media feature
    - `media` (optional): Changes the CSS media type of the page
  - Read-only: **false**


- **browser_evaluate**
  - Title: Evaluate JavaScript
  - Description: Evaluate JavaScript expression on page or element
  - Parameters:
    - `element` (string, optional): Human-readable element description used to obtain permission to interact with the element
    - `target` (string, optional): Exact target element reference from the page snapshot, or a unique element selector
    - `function` (string): () => { /* code */ } or (element) => { /* code */ } when element is provided
    - `filename` (string, optional): File name to save the result to. Relative file names are resolved against the workspace root. If not provided, result is returned as text.
  - Read-only: **false**


- **browser_file_upload**
  - Title: Upload files
  - Description: Upload one or multiple files
  - Parameters:
    - `paths` (array, optional): The absolute paths to the files to upload. Can be single file or multiple files. If omitted, file chooser is cancelled.
  - Read-only: **false**


- **browser_fill_form**
  - Title: Fill form
  - Description: Fill multiple form fields
  - Parameters:
    - `fields` (array): Fields to fill in
  - Read-only: **false**


- **browser_find**
  - Title: Find in page snapshot
  - Description: Search the accessibility snapshot of the current page for text or a regular expression. Returns matching snapshot nodes with a few lines of surrounding context (like search snippets), each shown under its path from the root of the tree, which is cheaper than capturing the whole snapshot when you only need to locate an element and its ref.
  - Parameters:
    - `text` (string, optional): Plain text to search for in the page snapshot (case-insensitive substring match). Provide either text or regex, not both.
    - `regex` (string, optional): Regular expression to search for in the page snapshot. Matching is case-sensitive by default; wrap the pattern in slashes to add flags, e.g. "/error/i" for case-insensitive. Provide either text or regex, not both.
    - `filename` (string, optional): Save results to a file instead of returning them in the response. Relative file names are resolved against the workspace root.
  - Read-only: **true**


- **browser_handle_dialog**
  - Title: Handle a dialog
  - Description: Handle a dialog
  - Parameters:
    - `accept` (boolean): Whether to accept the dialog.
    - `promptText` (string, optional): The text of the prompt in case of a prompt dialog.
  - Read-only: **false**


- **browser_hover**
  - Title: Hover mouse
  - Description: Hover over element on page
  - Parameters:
    - `element` (string, optional): Human-readable element description used to obtain permission to interact with the element
    - `target` (string): Exact target element reference from the page snapshot, or a unique element selector
  - Read-only: **false**


- **browser_navigate**
  - Title: Navigate to a URL
  - Description: Navigate to a URL
  - Parameters:
    - `url` (string): The URL to navigate to
  - Read-only: **false**


- **browser_navigate_back**
  - Title: Go back
  - Description: Go back to the previous page in the history
  - Parameters: None
  - Read-only: **false**


- **browser_network_request**
  - Title: Show network request details
  - Description: Returns full details (headers and body) of a single network request, or a single part if `part` is set. Use the number from browser_network_requests.
  - Parameters:
    - `index` (integer): 1-based index of the request, as printed by browser_network_requests.
    - `part` (string, optional): Return only this part of the request. Omit to return full details.
    - `filename` (string, optional): File name to save the result to. Relative file names are resolved against the workspace root. If not provided, output is returned as text.
  - Read-only: **true**


- **browser_network_requests**
  - Title: List network requests
  - Description: Returns a numbered list of network requests since loading the page. Use browser_network_request with the number to get full details.
  - Parameters:
    - `static` (boolean): Whether to include successful static resources like images, fonts, scripts, etc. Defaults to false.
    - `filter` (string, optional): Only return requests whose URL matches this regexp (e.g. "/api/.*user").
    - `filename` (string, optional): File name to save the network requests to. Relative file names are resolved against the workspace root. If not provided, requests are returned as text.
  - Read-only: **true**


- **browser_press_key**
  - Title: Press a key
  - Description: Press a key on the keyboard
  - Parameters:
    - `key` (string): Name of the key to press or a character to generate, such as `ArrowLeft` or `a`
  - Read-only: **false**


- **browser_resize**
  - Title: Resize browser window
  - Description: Resize the browser window
  - Parameters:
    - `width` (number): Width of the browser window
    - `height` (number): Height of the browser window
  - Read-only: **false**


- **browser_run_code_unsafe**
  - Title: Run Playwright code (unsafe)
  - Description: Run a Playwright code snippet. Unsafe: executes arbitrary JavaScript in the Playwright server process and is RCE-equivalent.
  - Parameters:
    - `code` (string, optional): A JavaScript function containing Playwright code to execute. It will be invoked with a single argument, page, which you can use for any page interaction. For example: `async (page) => { await page.getByRole('button', { name: 'Submit' }).click(); return await page.title(); }`
    - `filename` (string, optional): Load code from the specified file. Relative file names are resolved against the workspace root. If both code and filename are provided, code will be ignored.
  - Read-only: **false**


- **browser_select_option**
  - Title: Select option
  - Description: Select an option in a dropdown
  - Parameters:
    - `element` (string, optional): Human-readable element description used to obtain permission to interact with the element
    - `target` (string): Exact target element reference from the page snapshot, or a unique element selector
    - `values` (array): Array of values to select in the dropdown. This can be a single value or multiple values.
  - Read-only: **false**


- **browser_snapshot**
  - Title: Page snapshot
  - Description: Capture accessibility snapshot of the current page, this is better than screenshot
  - Parameters:
    - `target` (string, optional): Exact target element reference from the page snapshot, or a unique element selector
    - `filename` (string, optional): Save snapshot to a file instead of returning it in the response. Relative file names are resolved against the workspace root.
    - `depth` (number, optional): Limit the depth of the snapshot tree
    - `boxes` (boolean, optional): Include each element's bounding box as [box=x,y,width,height] in the snapshot. Coordinates are viewport-relative, in CSS pixels (Element.getBoundingClientRect)
  - Read-only: **true**


- **browser_take_screenshot**
  - Title: Take a screenshot
  - Description: Take a screenshot of the current page. You can't perform actions based on the screenshot, use browser_snapshot for actions.
  - Parameters:
    - `element` (string, optional): Human-readable element description used to obtain permission to interact with the element
    - `target` (string, optional): Exact target element reference from the page snapshot, or a unique element selector
    - `type` (string, optional): Image format for the screenshot. If unset, inferred from the filename extension, otherwise png.
    - `filename` (string, optional): File name to save the screenshot to. Relative file names are resolved against the workspace root. If not specified, the screenshot is saved into the output directory as `page-{timestamp}.{png|jpeg|webp}`.
    - `fullPage` (boolean, optional): When true, takes a screenshot of the full scrollable page, instead of the currently visible viewport. Cannot be used with element screenshots.
    - `scale` (string): Image resolution scale. "css" produces a screenshot sized in CSS pixels (smaller, consistent across devices). "device" produces a high-resolution screenshot using device pixels (larger, accounts for the device pixel ratio). Default is css.
  - Read-only: **true**


- **browser_type**
  - Title: Type text
  - Description: Type text into editable element
  - Parameters:
    - `element` (string, optional): Human-readable element description used to obtain permission to interact with the element
    - `target` (string): Exact target element reference from the page snapshot, or a unique element selector
    - `text` (string): Text to type into the element
    - `submit` (boolean, optional): Whether to submit entered text (press Enter after)
    - `slowly` (boolean, optional): Whether to type one character at a time. Useful for triggering key handlers in the page. By default entire text is filled in at once.
  - Read-only: **false**


- **browser_wait_for**
  - Title: Wait for
  - Description: Wait for text to appear or disappear or a specified time to pass
  - Parameters:
    - `time` (number, optional): The time to wait in seconds, at most 30
    - `text` (string, optional): The text to wait for
    - `textGone` (string, optional): The text to wait for to disappear
  - Read-only: **false**

</details>

<details>
<summary><b>Tab management</b></summary>


- **browser_tabs**
  - Title: Manage tabs
  - Description: List, create, close, or select a browser tab.
  - Parameters:
    - `action` (string): Operation to perform
    - `index` (number, optional): Tab index, used for close/select. If omitted for close, current tab is closed.
    - `url` (string, optional): URL to navigate to in the new tab, used for new.
  - Read-only: **false**

</details>

<details>
<summary><b>Browser installation</b></summary>

</details>

<details>
<summary><b>Configuration (opt-in via --caps=config)</b></summary>


- **browser_get_config**
  - Title: Get config
  - Description: Get the final resolved config after merging CLI options, environment variables and config file.
  - Parameters: None
  - Read-only: **true**

</details>

<details>
<summary><b>Network (opt-in via --caps=network)</b></summary>


- **browser_network_state_set**
  - Title: Set network state
  - Description: Sets the browser network state to online or offline. When offline, all network requests will fail.
  - Parameters:
    - `state` (string): Set to "offline" to simulate offline mode, "online" to restore network connectivity
  - Read-only: **false**


- **browser_route**
  - Title: Mock network requests
  - Description: Set up a route to mock network requests matching a URL pattern
  - Parameters:
    - `pattern` (string): URL pattern to match (e.g., "**/api/users", "**/*.{png,jpg}")
    - `status` (number, optional): HTTP status code to return (default: 200)
    - `body` (string, optional): Response body (text or JSON string)
    - `contentType` (string, optional): Content-Type header (e.g., "application/json", "text/html")
    - `headers` (array, optional): Headers to add in "Name: Value" format
    - `removeHeaders` (string, optional): Comma-separated list of header names to remove from request
  - Read-only: **false**


- **browser_route_list**
  - Title: List network routes
  - Description: List all active network routes
  - Parameters: None
  - Read-only: **true**


- **browser_unroute**
  - Title: Remove network routes
  - Description: Remove network routes matching a pattern (or all routes if no pattern specified)
  - Parameters:
    - `pattern` (string, optional): URL pattern to unroute (omit to remove all routes)
  - Read-only: **false**

</details>

<details>
<summary><b>Storage (opt-in via --caps=storage)</b></summary>


- **browser_cookie_clear**
  - Title: Clear cookies
  - Description: Clear all cookies
  - Parameters: None
  - Read-only: **false**


- **browser_cookie_delete**
  - Title: Delete cookie
  - Description: Delete a specific cookie
  - Parameters:
    - `name` (string): Cookie name to delete
  - Read-only: **false**


- **browser_cookie_get**
  - Title: Get cookie
  - Description: Get a specific cookie by name
  - Parameters:
    - `name` (string): Cookie name to get
  - Read-only: **true**


- **browser_cookie_list**
  - Title: List cookies
  - Description: List all cookies (optionally filtered by domain/path)
  - Parameters:
    - `domain` (string, optional): Filter cookies by domain
    - `path` (string, optional): Filter cookies by path
  - Read-only: **true**


- **browser_cookie_set**
  - Title: Set cookie
  - Description: Set a cookie with optional flags (domain, path, expires, httpOnly, secure, sameSite)
  - Parameters:
    - `name` (string): Cookie name
    - `value` (string): Cookie value
    - `domain` (string, optional): Cookie domain
    - `path` (string, optional): Cookie path
    - `expires` (number, optional): Cookie expiration as Unix timestamp
    - `httpOnly` (boolean, optional): Whether the cookie is HTTP only
    - `secure` (boolean, optional): Whether the cookie is secure
    - `sameSite` (string, optional): Cookie SameSite attribute
  - Read-only: **false**


- **browser_localstorage_clear**
  - Title: Clear localStorage
  - Description: Clear all localStorage
  - Parameters: None
  - Read-only: **false**


- **browser_localstorage_delete**
  - Title: Delete localStorage item
  - Description: Delete a localStorage item
  - Parameters:
    - `key` (string): Key to delete
  - Read-only: **false**


- **browser_localstorage_get**
  - Title: Get localStorage item
  - Description: Get a localStorage item by key
  - Parameters:
    - `key` (string): Key to get
  - Read-only: **true**


- **browser_localstorage_list**
  - Title: List localStorage
  - Description: List all localStorage key-value pairs
  - Parameters: None
  - Read-only: **true**


- **browser_localstorage_set**
  - Title: Set localStorage item
  - Description: Set a localStorage item
  - Parameters:
    - `key` (string): Key to set
    - `value` (string): Value to set
  - Read-only: **false**


- **browser_sessionstorage_clear**
  - Title: Clear sessionStorage
  - Description: Clear all sessionStorage
  - Parameters: None
  - Read-only: **false**


- **browser_sessionstorage_delete**
  - Title: Delete sessionStorage item
  - Description: Delete a sessionStorage item
  - Parameters:
    - `key` (string): Key to delete
  - Read-only: **false**


- **browser_sessionstorage_get**
  - Title: Get sessionStorage item
  - Description: Get a sessionStorage item by key
  - Parameters:
    - `key` (string): Key to get
  - Read-only: **true**


- **browser_sessionstorage_list**
  - Title: List sessionStorage
  - Description: List all sessionStorage key-value pairs
  - Parameters: None
  - Read-only: **true**


- **browser_sessionstorage_set**
  - Title: Set sessionStorage item
  - Description: Set a sessionStorage item
  - Parameters:
    - `key` (string): Key to set
    - `value` (string): Value to set
  - Read-only: **false**


- **browser_set_storage_state**
  - Title: Restore storage state
  - Description: Restore storage state (cookies, local storage) from a file. This clears existing cookies and local storage before restoring.
  - Parameters:
    - `filename` (string): Path to the storage state file to restore from. Relative file names are resolved against the workspace root.
  - Read-only: **false**


- **browser_storage_state**
  - Title: Save storage state
  - Description: Save storage state (cookies, local storage) to a file for later reuse
  - Parameters:
    - `filename` (string, optional): File name to save the storage state to. Relative file names are resolved against the workspace root. If not specified, the storage state is saved into the output directory as `storage-state-{timestamp}.json`.
  - Read-only: **true**

</details>

<details>
<summary><b>DevTools (opt-in via --caps=devtools)</b></summary>


- **browser_annotate**
  - Title: Annotate the current page
  - Description: Open the Playwright Dashboard in annotation mode for the current page and wait for the user to draw annotations. Returns the annotated screenshot, ARIA snapshot, and the list of annotations.
  - Parameters: None
  - Read-only: **true**


- **browser_hide_highlight**
  - Title: Hide element highlight
  - Description: Remove a highlight overlay previously added for the element.
  - Parameters:
    - `element` (string, optional): Human-readable element description used when adding the highlight; must match the value passed to browser_highlight.
    - `target` (string, optional): Exact target element reference from the page snapshot, or a unique element selector
  - Read-only: **true**


- **browser_highlight**
  - Title: Highlight element
  - Description: Show a persistent highlight overlay around the element on the page.
  - Parameters:
    - `element` (string, optional): Human-readable element description used to obtain permission to interact with the element
    - `target` (string): Exact target element reference from the page snapshot, or a unique element selector
    - `style` (string, optional): Additional inline CSS applied to the highlight overlay, e.g. "outline: 2px dashed red".
  - Read-only: **true**


- **browser_resume**
  - Title: Resume paused script execution
  - Description: Resume script execution after it was paused. When called with step set to true, execution will pause again before the next action.
  - Parameters:
    - `step` (boolean, optional): When true, execution will pause again before the next action, allowing step-by-step debugging.
    - `location` (string, optional): Pause execution at a specific <file>:<line>, e.g. "example.spec.ts:42".
  - Read-only: **false**


- **browser_start_recording**
  - Title: Start recording user actions
  - Description: Start recording actions that the user performs in the browser as Playwright code. Use it when the user wants to demonstrate a flow manually. Call browser_stop_recording when the user says they are done to retrieve the recorded actions.
  - Parameters: None
  - Read-only: **true**


- **browser_start_tracing**
  - Title: Start tracing
  - Description: Start trace recording
  - Parameters: None
  - Read-only: **true**


- **browser_start_video**
  - Title: Start video
  - Description: Start video recording
  - Parameters:
    - `filename` (string, optional): File name to save the video to. Relative file names are resolved against the workspace root. If not specified, the video is saved into the output directory as `video-{timestamp}.webm`.
    - `size` (object, optional): Video size
    - `fps` (number, optional): Video frame rate in frames per second, defaults to 25
    - `cursor` (boolean, optional): Render an animated mouse cursor that travels to each action point. Paces actions by 800ms so that the cursor has time to travel.
  - Read-only: **true**


- **browser_stop_recording**
  - Title: Stop recording user actions
  - Description: Stop the recording started with browser_start_recording and return the recorded actions as Playwright code.
  - Parameters: None
  - Read-only: **true**


- **browser_stop_tracing**
  - Title: Stop tracing
  - Description: Stop trace recording
  - Parameters: None
  - Read-only: **true**


- **browser_stop_video**
  - Title: Stop video
  - Description: Stop video recording
  - Parameters: None
  - Read-only: **true**


- **browser_video_chapter**
  - Title: Video chapter
  - Description: Add a chapter marker to the video recording. Shows a full-screen chapter card with blurred backdrop.
  - Parameters:
    - `title` (string): Chapter title
    - `description` (string, optional): Chapter description
    - `duration` (number, optional): Duration in milliseconds to show the chapter card
  - Read-only: **true**


- **browser_video_hide_actions**
  - Title: Hide action overlays
  - Description: Stop annotating actions performed on the page.
  - Parameters: None
  - Read-only: **true**


- **browser_video_show_actions**
  - Title: Show action overlays
  - Description: Annotate subsequent actions performed on the page with a callout that names the action and, when styled, marks the action point and highlights the target element. Useful while video recording or screencasting.
  - Parameters:
    - `duration` (number, optional): How long each action annotation stays on screen, in milliseconds. Defaults to 500.
    - `position` (string, optional): Where to place the action title relative to the page. Defaults to top-right.
    - `cursor` (string, optional): Cursor decoration for pointer actions. "pointer" (default) animates a mouse pointer from the previous action point to the next one; "none" disables the cursor decoration.
    - `style` (object, optional): Styles of the action decorations.
  - Read-only: **true**

</details>

<details>
<summary><b>Coordinate-based (opt-in via --caps=vision)</b></summary>


- **browser_mouse_click_xy**
  - Title: Click
  - Description: Click mouse button at a given position
  - Parameters:
    - `x` (number): X coordinate
    - `y` (number): Y coordinate
    - `button` (string, optional): Button to click, defaults to left
    - `clickCount` (number, optional): Number of clicks, defaults to 1
    - `delay` (number, optional): Time to wait between mouse down and mouse up in milliseconds, defaults to 0
  - Read-only: **false**


- **browser_mouse_down**
  - Title: Press mouse down
  - Description: Press mouse down
  - Parameters:
    - `button` (string, optional): Button to press, defaults to left
  - Read-only: **false**


- **browser_mouse_drag_xy**
  - Title: Drag mouse
  - Description: Drag left mouse button to a given position
  - Parameters:
    - `startX` (number): Start X coordinate
    - `startY` (number): Start Y coordinate
    - `endX` (number): End X coordinate
    - `endY` (number): End Y coordinate
  - Read-only: **false**


- **browser_mouse_move_xy**
  - Title: Move mouse
  - Description: Move mouse to a given position
  - Parameters:
    - `x` (number): X coordinate
    - `y` (number): Y coordinate
  - Read-only: **false**


- **browser_mouse_up**
  - Title: Press mouse up
  - Description: Press mouse up
  - Parameters:
    - `button` (string, optional): Button to press, defaults to left
  - Read-only: **false**


- **browser_mouse_wheel**
  - Title: Scroll mouse wheel
  - Description: Scroll mouse wheel
  - Parameters:
    - `deltaX` (number): X delta
    - `deltaY` (number): Y delta
  - Read-only: **false**

</details>

<details>
<summary><b>PDF generation (opt-in via --caps=pdf)</b></summary>


- **browser_pdf_save**
  - Title: Save as PDF
  - Description: Save page as PDF
  - Parameters:
    - `filename` (string, optional): File name to save the pdf to. Relative file names are resolved against the workspace root. If not specified, the pdf is saved into the output directory as `page-{timestamp}.pdf`.
  - Read-only: **true**

</details>

<details>
<summary><b>Test assertions (opt-in via --caps=testing)</b></summary>


- **browser_generate_locator**
  - Title: Create locator for element
  - Description: Generate locator for the given element to use in tests
  - Parameters:
    - `element` (string, optional): Human-readable element description used to obtain permission to interact with the element
    - `target` (string): Exact target element reference from the page snapshot, or a unique element selector
  - Read-only: **true**


- **browser_verify_element_visible**
  - Title: Verify element visible
  - Description: Verify element is visible on the page
  - Parameters:
    - `role` (string): ROLE of the element. Can be found in the snapshot like this: `- {ROLE} "Accessible Name":`
    - `accessibleName` (string): ACCESSIBLE_NAME of the element. Can be found in the snapshot like this: `- role "{ACCESSIBLE_NAME}"`
  - Read-only: **false**


- **browser_verify_list_visible**
  - Title: Verify list visible
  - Description: Verify list is visible on the page
  - Parameters:
    - `element` (string): Human-readable list description
    - `target` (string): Exact target element reference that points to the list
    - `items` (array): Items to verify
  - Read-only: **false**


- **browser_verify_text_visible**
  - Title: Verify text visible
  - Description: Verify text is visible on the page. Prefer browser_verify_element_visible if possible.
  - Parameters:
    - `text` (string): TEXT to verify. Can be found in the snapshot like this: `- role "Accessible Name": {TEXT}` or like this: `- text: {TEXT}`
  - Read-only: **false**


- **browser_verify_value**
  - Title: Verify value
  - Description: Verify element value
  - Parameters:
    - `type` (string): Type of the element
    - `element` (string): Human-readable element description
    - `target` (string): Exact target element reference from the page snapshot
    - `value` (string): Value to verify. For checkbox, use "true" or "false".
  - Read-only: **false**

</details>