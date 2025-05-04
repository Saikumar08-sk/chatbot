import openai
from wyn_agent_x.helper import (
    load_metadata,
    detect_intent,
    fill_parameters,
    FUNCTION_REGISTRY
)

class AgentX:
    def __init__(self, api_key, account_sid, auth_token,
                 serpapi_key=None, email_key=None, claude_api_key=None,
                 protocol="You are a helpful assistant."):
        self.api_key = api_key
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.serpapi_key = serpapi_key
        self.email_key = email_key
        self.claude_api_key = claude_api_key
        self.protocol = protocol
        self.metadata = load_metadata()
        self.event_stream = []

        from wyn_agent_x.helper import FUNCTION_REGISTRY
        print(f"[DEBUG] Registered functions: {list(FUNCTION_REGISTRY.keys())}")

        # ✅ OpenAI 1.0+ client
        self.client = openai.OpenAI(api_key=self.api_key)

    def process_message(self, message: str) -> str:
        # Step 1: Check for API-triggering intent
        intent = detect_intent(message, self.metadata)

        if intent:
            sample_payload = self.metadata[intent]["sample_payload"]
            payload = fill_parameters(sample_payload, {"message": message})

            secrets = {
                "account_sid": self.account_sid,
                "auth_token": self.auth_token,
                "serpapi_key": self.serpapi_key,
                "email_key": self.email_key,
                "claude_api_key": self.claude_api_key,
            }

            try:
                result = FUNCTION_REGISTRY[intent](payload, secrets, self.event_stream)
                return str(result)
            except Exception as e:
                return f"🚨 Intent Error: {str(e)}"

        # Step 2: Default to OpenAI chat
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.protocol},
                    {"role": "user", "content": message}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ OpenAI Error: {str(e)}"
