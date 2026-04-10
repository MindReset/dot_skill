# Authentication

## Overview

All Dot Skill requests require authentication using a Bearer token in the Authorization header.

## Getting an API Key

1. Open the Dot. App
2. Go to the "More" tab
3. Tap on "API Keys"
4. Tap "Create API Key"
5. Save the key securely - the app will not show it again

## Using the API Key

Include the API key in the Authorization header:

```http
Authorization: Bearer dot_app_<your_api_key>
```

Example:

```bash
curl -X GET \
  https://dot.mindreset.tech/api/authV2/open/devices \
  -H 'Authorization: Bearer dot_app_UlSpzXNEXhYZIAFakHLCkMVVBLbsBIWxaRMVaJZGUOYKhDoDRZwLLvLujAIwQxbY'
```

## Security Best Practices

1. **Keep your API key secret**: Do not share it or commit it to version control
2. **Use environment variables**: Store the key in `.env` files or environment variables
3. **Rotate keys regularly**: Delete and recreate keys if you suspect compromise
4. **Delete unused keys**: Remove keys that are no longer needed

## Environment Variable

For convenience, you can set the API key as an environment variable:

```bash
export DOT_API_KEY="dot_app_<your_api_key>"
```

Then use it in scripts:

```python
import os
api_key = os.environ.get('DOT_API_KEY')
```
