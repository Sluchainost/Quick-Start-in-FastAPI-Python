# TASK DESCRIPTION

1) Create an **html** file (e.g. "index.html"), in the text of which write:

    ```html
    <!DOCTYPE html>

    <html lang="en">
    <head>
    
    <meta charset="UTF-8">

    <title> Example of a simple html page </title>
    </head>
    
    <body>
    
    I AM UNREALLY COOL AND MY RESPECT IS WITHOUT MEASURE :)
    </body>
    
    </html>
    ```

2) Create a **FastAPI** application that accepts a **GET** request to the default endpoint (route, page address) `/` and returns an **html** page.
3) Save the file and run the application with `uvicorn`:

    ```bash
    uvicorn main:app --reload
    ```

Open <http://localhost:8000> in your web browser.
