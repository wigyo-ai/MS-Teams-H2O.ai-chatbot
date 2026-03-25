import os

class Config:
    APP_ID          = os.environ.get("MicrosoftAppId")
    APP_PASSWORD    = os.environ.get("MicrosoftAppPassword")
    APP_TENANT_ID   = os.environ.get("MicrosoftAppTenantId")
    H2OGPTE_URL     = os.environ.get("H2OGPTE_URL")
    H2OGPTE_API_KEY = os.environ.get("H2OGPTE_API_KEY")
    PORT            = int(os.environ.get("PORT", "8000"))
