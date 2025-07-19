# Frequently Asked Questions and Common Issues

## Issues with Toctree

If errors occur in your `.md` files, you might see the following unexpected line:

`<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">`

This usually appears right after the last link in your `toctree`, and it's caused by a `toctree` block that is not properly closed.

Make sure to close the `toctree` using triple backticks: "```".  
If the block ends with an `.md` file and is not properly closed, the issue will persist.

## Build Function Errors

If you encounter the error:

`[WinError 32] The process cannot access the file because it is being used by another process`

during the build phase, ensure that the Windows command prompt hosting your Python server is closed.

Simply close the command prompt window and rerun the build command.  
The tool needs exclusive access to certain folders while running.