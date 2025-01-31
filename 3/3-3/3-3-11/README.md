# TASK DESCRIPTION

Your task is to create a **FastAPI** application that demonstrates how to work with **request headers**. Follow these steps to complete the task:

- Create an endpoint in `/headers` that accepts **GET** requests.

- At the `/headers` endpoint, extract the following **headers** from the incoming request:

  - `"User-agent"`: The client browser user agent string or the user's custom agent.

  - `"Accept-Language"`: The client's preferred language for content negotiation.

- Return a **JSON** response containing the extracted headers and their values.

## Example

**GET** request to `/headers` with the following headers:

```markdown
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36

    Accept-Language: en-US,en;q=0.9,es;q=0.8
```

The **JSON** response should be:

```json
    {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9,es;q=0.8"
    }
```

- Implement error handling to return an appropriate response with status code `400 (Bad Request)` if the required headers are missing.

- Optional: Add a check to see if the `"Accept-Language"` header is in the correct format (e.g. "en-US,en;q=0.9,es;q=0.8"). If it is not in the correct format, return an error response with status code `400 (Bad Request)`.

> Hint: Use the `request.headers` attribute to access the headers of incoming requests.
