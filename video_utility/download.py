from fastapi import FastAPI, HTTPException
import aiohttp
import tempfile





async def download_file(url: str, suffix: str) -> str:
    """Download file from URL and save to temporary file"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise HTTPException(status_code=400, detail="Failed to download file")
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
                tmp_file.write(await response.read())
                return tmp_file.name