import os

class Config:
    APP_ID          = os.environ.get("MicrosoftAppId",       "760c7ee4-624a-4ee7-bc8f-04df094ae339")
    APP_PASSWORD    = os.environ.get("MicrosoftAppPassword",  "TWy8Q~16vnkxGiaaXhmyhqflJFjK3Q3DqvKpgbDy")
    APP_TENANT_ID   = os.environ.get("MicrosoftAppTenantId",  "35013e61-d285-4f21-9b33-4c601cc1d8ce")
    H2OGPTE_URL     = os.environ.get("H2OGPTE_URL",           "https://h2ogpte.cloud-dev.h2o.dev/")
    H2OGPTE_API_KEY = os.environ.get("H2OGPTE_API_KEY",       "sk-6uXOhlmyJkFbY3TTiJz62i0BTAkO0PJ5ppXgIXAzHq0gkmvg")
    PORT            = int(os.environ.get("PORT", "8000"))
