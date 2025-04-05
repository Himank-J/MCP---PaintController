## Overview

MCP - PaintController, an innovative painting application that combines a user-friendly drawing interface with the power of the Model Context Protocol (MCP). This project allows users to create flows/diagrams using intuitive controls while leveraging MCP to integrate AI-driven features.

## Project

- Using MCP, we use LLMs and prompting to generate output in iterations. 
- The aim is to to manually convert an LLM into an Agent without using any framework. Using iterative prmpting we get an answer to query in 3 steps. 
- In the end the output is to be pasted an application controlled via MCP. 
- In our case we have used FreeForm (for Macos; could be MS Paint for Windows). 
- We prompt our LLM to use right tools to open FreeFrom app, apply shapes, input text field and then finally right the output.

## Demo


## Code Details

[Get Coordinates](get-coordinates.py)

We use below code to get the coordinates of the mouse pointer. This helps us determine where and what shapes to click when FreeForm app is open.

```python
try:
    while True:
        x, y = pyautogui.position()
        print(f"Mouse position: x={x}, y={y}")
        time.sleep(1)
except KeyboardInterrupt:
    listener.stop()
    print('\nDone.')
```    

[MCP Server](mcp_server_gmail.py)

This is the server file that enlists all the tools that our LLM can use. Below is the main code that opens FreeForm app, creates a rectangle and adds text inside it.

```python
@mcp.tool()
async def open_freeform_and_create(text: str) -> dict:
    """Open Freeform app, create a rectangle and add text inside it"""
    try:
        # Ensure safe mouse movements
        pyautogui.FAILSAFE = True
        
        # Open Freeform using subprocess
        subprocess.run(['open', '-a', 'Freeform'])
        time.sleep(2)
        
        # Move to File menu and click
        pyautogui.moveTo(140, 6.25, duration=0.5)
        pyautogui.click()
        
        # Move to "New Board" option and click
        pyautogui.moveTo(144, 39, duration=0.5)
        pyautogui.click()
        time.sleep(1)
        
        # Select shape tool
        pyautogui.moveTo(908, 45, duration=0.5)
        pyautogui.click()
        
        # Select rectangle
        pyautogui.moveTo(909, 219, duration=0.5)
        pyautogui.click()
        
        # Move to rectangle
        pyautogui.moveTo(951, 409, duration=0.5)
        
        # Type the text
        time.sleep(0.5)
        pyautogui.typewrite(text)
```

[MCP Client](mcp_client_gmail.py)

This is the client file that uses MCP to send the query to the server.
