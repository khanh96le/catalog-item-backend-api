# Flask rest API

## Rest principles

#### What is a REST API?
- It's a way of thinking how a server response requests
- It doesn't respond with just data
- It responds with resources

#### Stateless
- One request cannot depend on other requests
- The server only know about the current request, and not any previous requests
- For example: 
    - POST /item/chair -> Server does not know the item is exist
    - The server must check every requests from client.


