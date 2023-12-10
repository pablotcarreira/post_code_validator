from contextlib import asynccontextmanager
from uuid import uuid4

import uvicorn
from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel, Field
from starlette.requests import Request
from starlette.responses import JSONResponse

from libs.app_init import get_logger
from libs.app_init import load_post_codes_cache
from libs.uk_post_code_validator import validate_post_code


logger = get_logger()
post_code_cache = set()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """App lifecycle."""
    # startup
    global post_code_cache
    try:
        post_code_cache = await load_post_codes_cache(
            "https://api.os.uk/downloads/v1/products/CodePointOpen/downloads?area=GB&format=CSV&redirect",
            "./Data/CSV",
            "libs/post_codes.txt",
            logger,
            allow_fallback=True
        )
    except:
        logger.error("Failed loading the post code cache.", exc_info=True)
        raise RuntimeError("Failed loading the post code cache.")
    yield
    # teardown
    logger.info("App shutdown successfully.")


app = FastAPI(lifespan=lifespan)


class ValidateModel(BaseModel):
    # Although postcodes can vary from 6-8 chars we'll allow extra room for user mistakes like leading or trailing spaces.
    post_code: str = Field(..., min_length=6, max_length=12, description="The post code to be validated/formatted.")
    strict: bool = Field(default=True, description="Assert the postcode is present in the Code-Point Open database or a custom subset.")


@app.post("/v1/validate")
async def validate(request: Request, params: ValidateModel):
    """Format and validate a post code.
            - Special characters and extra whitespaces are stripped.
            - If strict mode is enabled, check if the postcode really exist against a cache (generally generated from Code-Point Open db).
            - If strict mode is disabled, only check the post code validity.
            - Return the well formatted post code or None: {valid: true|false, post_code: post code|null}

    """
    correlation_id = request.headers.get("X-Correlation-Id", str(uuid4()))
    logger.debug(f" Validating item: {params} Correlation_Id: {correlation_id}")

    try:
        result = validate_post_code(params.post_code, params.strict, post_code_cache)
    except:
        logger.exception(f"Error while validating item: {params} Correlation_Id: {correlation_id}")
        raise HTTPException(status_code=500, detail="Error validating post code.")

    return JSONResponse(content={
        "valid": bool(result),
        "post_code": result if result else None,
    }, headers={"X-Correlation-Id": correlation_id})


@app.get("/health")
async def health_check():
    logger.debug("Ping")
    return {"status": "healthy"}


if __name__ == "__main__":
    # For dev purpose, run this file directly. When on dev, remember to disable loading the remote cache to avoid being blacklisted by code point.
    uvicorn.run("main:app", host="0.0.0.0", port=3500, log_level="info", reload=True)
