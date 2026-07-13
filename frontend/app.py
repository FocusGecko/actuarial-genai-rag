"""Chainlit frontend for the actuarial chatbot."""

import chainlit as cl
import httpx

API_BASE_URL = "http://localhost:8000"


@cl.set_chat_profiles
async def chat_profile():
    return [
        cl.ChatProfile(name="Actuariat", markdown_description="Assistant actuariel généraliste"),
    ]


@cl.set_starters
async def set_starters():
    return [
        cl.Starter(
            label="Solvabilité 2",
            message="Qu'est-ce que le cadre Solvabilité 2 et quels sont ses 3 piliers ?",
            icon="/public/icons/shield.svg",
        ),
        cl.Starter(
            label="Provisions techniques",
            message="Comment calcule-t-on les provisions techniques en assurance non-vie ?",
            icon="/public/icons/chart.svg",
        ),
        cl.Starter(
            label="Tables de mortalité",
            message="Quelles sont les principales tables de mortalité utilisées en France ?",
            icon="/public/icons/table.svg",
        ),
        cl.Starter(
            label="SCR",
            message="Comment est calculé le SCR en formule standard ?",
            icon="/public/icons/calculator.svg",
        ),
    ]


@cl.on_chat_start
async def on_chat_start():
    await cl.Message(
        content="Bonjour ! Je suis votre assistant actuariel. "
        "Posez-moi une question ou choisissez un sujet ci-dessus."
    ).send()


@cl.on_message
async def on_message(message: cl.Message):
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{API_BASE_URL}/api/chat",
            json={"question": message.content},
        )

    if response.status_code != 200:
        await cl.Message(content="Erreur lors de la communication avec le serveur.").send()
        return

    data = response.json()
    answer = data["answer"]

    # Display sources if any (for future RAG integration)
    elements = []
    for source in data.get("sources", []):
        elements.append(cl.Text(name=source["title"], content=source["excerpt"], display="side"))

    await cl.Message(content=answer, elements=elements).send()
