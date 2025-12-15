import os, requests, msal

def _get_graph_token() -> str:
    app = msal.ConfidentialClientApplication(
        client_id=os.environ["MS_CLIENT_ID"],
        client_credential=os.environ["MS_CLIENT_SECRET"],
        authority=f"https://login.microsoftonline.com/{os.environ['MS_TENANT_ID']}",
    )
    result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    if "access_token" not in result:
        raise RuntimeError(f"Token error: {result}")
    return result["access_token"]

def send_outlook_html(to_email: str, subject: str, html: str):
    token = _get_graph_token()
    sender = os.environ["OUTLOOK_SENDER_UPN"]

    url = f"https://graph.microsoft.com/v1.0/users/{sender}/sendMail"
    payload = {
        "message": {
            "subject": subject,
            "body": {"contentType": "HTML", "content": html},
            "toRecipients": [{"emailAddress": {"address": to_email}}],
        },
        "saveToSentItems": True,
    }
    r = requests.post(url, json=payload, headers={"Authorization": f"Bearer {token}"})
    r.raise_for_status()
    return r.status_code   
