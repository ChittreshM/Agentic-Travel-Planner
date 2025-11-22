from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import json

photos_agent = Agent(
    name="photos_agent",
    model=LiteLlm("openai/gpt-4o"),
    description="Provides photographs and Google Maps locations for popular places in a destination.",
    instruction=(
        "Given a destination, provide information about 5 popular places including: "
        "1. Place name, 2. Brief description, 3. Google Maps location (as a searchable address or coordinates), "
        "4. A description of what the place looks like (for photo reference). "
        "Format the response as JSON with a 'places' array, where each place has: "
        "'name', 'description', 'google_maps_location', and 'photo_description'. "
        "The google_maps_location should be a full address or coordinates that can be used in Google Maps."
    )
)

session_service = InMemorySessionService()
runner = Runner(
    agent=photos_agent,
    app_name="photos_app",
    session_service=session_service
)

USER_ID = "user_photos"
SESSION_ID = "session_photos"

# Create session at module load time
try:
    session_service.create_session_sync(
        app_name="photos_app",
        user_id=USER_ID,
        session_id=SESSION_ID
    )
except Exception:
    pass  # Session might already exist

async def execute(request):
    # Ensure session exists before running - use sync version
    try:
        session_service.create_session_sync(
            app_name="photos_app",
            user_id=USER_ID,
            session_id=SESSION_ID
        )
    except Exception as e:
        # Try to get session to verify it exists
        try:
            session_service.get_session_sync(
                app_name="photos_app",
                user_id=USER_ID,
                session_id=SESSION_ID
            )
        except Exception:
            # If get also fails, try creating again
            session_service.create_session_sync(
                app_name="photos_app",
                user_id=USER_ID,
                session_id=SESSION_ID
            )

    prompt = (
        f"User is visiting {request['destination']} from {request['start_date']} to {request['end_date']}. "
        f"Provide information about 5 popular and photogenic places in {request['destination']}. "
        f"For each place, provide: name, brief description, Google Maps location (full address or coordinates), "
        f"and a description of what makes it photogenic. "
        f"Respond in JSON format with a 'places' array, where each place object contains: "
        f"'name', 'description', 'google_maps_location', and 'photo_description'. "
        f"Make sure the JSON is valid and properly formatted."
    )

    message = types.Content(role="user", parts=[types.Part(text=prompt)])

    async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=message):
        if event.is_final_response():
            response_text = event.content.parts[0].text
            try:
                # Try to parse as JSON
                parsed = json.loads(response_text)
                if "places" in parsed and isinstance(parsed["places"], list):
                    return {"places": parsed["places"]}
                else:
                    print("❌ 'places' key missing or not a list in response JSON")
                    return {"places": response_text}  # fallback to raw text
            except json.JSONDecodeError as e:
                print("❌ JSON parsing failed:", e)
                print("Response content:", response_text)
                # Try to extract JSON from markdown code blocks if present
                import re
                json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response_text, re.DOTALL)
                if json_match:
                    try:
                        parsed = json.loads(json_match.group(1))
                        if "places" in parsed and isinstance(parsed["places"], list):
                            return {"places": parsed["places"]}
                    except:
                        pass
                return {"places": response_text}  # fallback to raw text

