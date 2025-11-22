from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

places_agent = Agent(
    name="places_agent",
    model=LiteLlm("openai/gpt-4o"),
    description="Suggests popular places to visit based on traveler type with ticket booking information.",
    instruction=(
        "Given a destination, travel dates, budget, and traveler type (nature lover, activity lover, etc.), "
        "suggest 5-7 must-visit places. For each place, provide: name, brief description, why it matches the traveler type, "
        "approximate ticket price, and official ticket booking website URL. Format the response clearly with each place "
        "as a numbered item. If the traveler is a nature lover, focus on parks, gardens, natural landmarks, and scenic spots. "
        "If activity lover, focus on adventure activities, sports venues, entertainment centers, and interactive experiences."
    )
)

session_service = InMemorySessionService()
runner = Runner(
    agent=places_agent,
    app_name="places_app",
    session_service=session_service
)

USER_ID = "user_places"
SESSION_ID = "session_places"

# Create session at module load time
try:
    session_service.create_session_sync(
        app_name="places_app",
        user_id=USER_ID,
        session_id=SESSION_ID
    )
except Exception:
    pass  # Session might already exist

async def execute(request):
    # Ensure session exists before running - use sync version
    try:
        session_service.create_session_sync(
            app_name="places_app",
            user_id=USER_ID,
            session_id=SESSION_ID
        )
    except Exception as e:
        # Try to get session to verify it exists
        try:
            session_service.get_session_sync(
                app_name="places_app",
                user_id=USER_ID,
                session_id=SESSION_ID
            )
        except Exception:
            # If get also fails, try creating again
            session_service.create_session_sync(
                app_name="places_app",
                user_id=USER_ID,
                session_id=SESSION_ID
            )

    traveler_type = request.get('traveler_type', 'general traveler')
    
    prompt = (
        f"User is visiting {request['destination']} from {request['start_date']} to {request['end_date']}, "
        f"with a budget of ${request['budget']}. The traveler is a {traveler_type}. "
        f"Suggest 5-7 must-visit places that match their interests. For each place, provide: "
        f"1. Name, 2. Brief description, 3. Why it matches a {traveler_type}, "
        f"4. Approximate ticket price, 5. Official ticket booking website URL. "
        f"Format each place clearly as a numbered item."
    )

    message = types.Content(role="user", parts=[types.Part(text=prompt)])

    async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=message):
        if event.is_final_response():
            return {"places": event.content.parts[0].text}

