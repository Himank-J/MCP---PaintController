import pyautogui
import subprocess
import sys, time, math
from mcp.types import TextContent
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

# instantiate an MCP server client
mcp = FastMCP("Freeform Drawer")

@mcp.tool()
def strings_to_chars_to_int(string: str) -> list[int]:
    """Return the ASCII values of the characters in a word"""
    print("CALLED: strings_to_chars_to_int(string: str) -> list[int]:")
    return [int(ord(char)) for char in string]

@mcp.tool()
def int_list_to_exponential_sum(int_list: list) -> float:
    """Return sum of exponentials of numbers in a list"""
    print("CALLED: int_list_to_exponential_sum(int_list: list) -> float:")
    return sum(math.exp(i) for i in int_list)

@mcp.tool()
def fibonacci_numbers(n: int) -> list:
    """Return the first n Fibonacci Numbers"""
    print("CALLED: fibonacci_numbers(n: int) -> list:")
    if n <= 0:
        return []
    
    fib_sequence = [0, 1]
    for _ in range(2, n):
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence[:n]

# tool for opening freeform, creating rectangle and writing text to it
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
        
        return {
            "content": [
                TextContent(
                    type="text",
                    text="Freeform board created with rectangle and text"
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error creating Freeform board: {str(e)}"
                )
            ]
        }

@mcp.prompt()
def debug_error(error: str) -> list[base.Message]:
    return [
        base.UserMessage("I'm seeing this error:"),
        base.UserMessage(error),
        base.AssistantMessage("I'll help debug that. What have you tried so far?"),
    ]

if __name__ == "__main__":
    # Check if running with mcp dev command
    print("STARTING")
    if len(sys.argv) > 1 and sys.argv[1] == "dev":
        mcp.run()  # Run without transport for dev server
    else:
        mcp.run(transport="stdio")  # Run with stdio for direct execution
