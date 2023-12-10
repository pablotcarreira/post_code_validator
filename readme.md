
# Post Code Validator

## How to use

- Build with `make build`
- Run/Start with `make start`
- Stop with `make stop`

Try a request, for example:

```bash
curl -X POST --location "http://0.0.0.0:3500/v1/validate" \
    -H "Content-Type: application/json" \
    -d '{
          "post_code": "DA6 8HD",
          "strict": true
        }'
```

Some basic autodocs can be found at `/docs`


## The library
The validador library located in `libs.uk_post_code_validator` is the core library used by this API and can be detached and used in other projects. 
The library perform two tasks:

1. Clean and format the post code if possible: It removes all special characters and spaces and then insert the space separator between the outward and inward codes. 
2. Check if the postcode is valid, with two distinct possible methodologies:
   1. Structure check: Check if the post code structure and characters are valid and correct.
   2. Strict check: Check if the post code is acceptable based on a set of acceptable post codes.

The strict mode is in place to avoid the acceptance of nonexistent post codes that has a valid structure.

Both modes are fast, the structure validation can perform around 1.8 million validations per second and the strict mode around 2.5 million validations per second on a modern computer. The strict mode lookup complexity is O(1) and it's not affected by the size of the set.

If the postcode is valid, it returns the well formatted post code, if not, it returns False.

## The API / service

The API exposes the `validate` endpoint accepting the post code to be validated and the mode (optional).

If strict mode is used, it'll use an internal cache of postcodes for comparison. 

This cache is populated during service startup by downloading a database of existing postcodes. It's currently using the Code-Point Open service, but can be configured to use other URLs, a S3 bucket for example.

If the download fails, the service will fallback to a static set of post codes previously obtained from Code-Point Open.

The internal cache can be updated by restarting the service. 

### Performance

A Locust test was performed with requests interval between 5 to 15 seconds and only one uvicorn worker. The service performed well up to 1930 concurrent users and had a peak of 190 requests per seconds before it started to behave erratically. 

The locustfile and the report are in the project folder.



