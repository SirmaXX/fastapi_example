# FASTAPİ EXAMPLE

Example  service for job applyment





## Completed tasks


1.  ◦ Host the API on a serverless platform like Cloudflare Workers, Azure Functions, or Google Cloud Functions using free tiers.(another project:https://gloww-test.azurewebsites.net/)
2.  ◦ The endpoint should accept a query parameter "stream" that can be set to "true" or "false".

3. ◦ The request must include an Authorization header with a bearer token in the format "USER{XXX}" where XXX is a 3-digit numeric ID. Return a 401 Unauthorized response if no valid token is provided. Any token starting with "USER" followed by a 3-digit number is acceptable.

4. The API response payload should be a JSON object with the following properties:
   1.    ▪ "message": A customized welcome message including the user ID and incremental visit number. Example: "Welcome USER_123, this is your visit #456"
   2. "group": A hashed integer between 1-10 derived from the user ID. This should be consistent for a given user, always mapping them to the same group.

5. Exceeded response on the 5th request within the window.
6.  Rate limit each user ID to 4 requests per minute. Return a 429 Rate Limit
7. If multiple concurrent streams occur for one user, they should share the same rate limit but have independent visit counts and stream sequence numbers.

       

       


## Uncompleted tasks
 1.  When "stream=false", respond immediately with a single payload including "stream_seq=0".




