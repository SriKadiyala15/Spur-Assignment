from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine, SessionLocal
from models import Conversation, Message
from schemas import ChatRequest
from ai_service import generate_reply
import uuid

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Backend is running!"}


# Fetch chat history
@app.get("/chat/history/{session_id}")
def get_chat_history(session_id: str):
    db = SessionLocal()

    try:
        messages = db.query(Message).filter(
            Message.conversation_id == session_id
        ).order_by(Message.timestamp).all()

        history = []
        for msg in messages:
            history.append({
                "sender": msg.sender,
                "text": msg.text
            })

        return history

    except Exception as e:
        print("HISTORY ERROR:", e)
        return []

    finally:
        db.close()


# Send message to AI
@app.post("/chat/message")
def chat(request: ChatRequest):
    db = SessionLocal()
    session_id = None

    try:
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")

        session_id = request.sessionId or str(uuid.uuid4())

        conversation = db.query(Conversation).filter(
            Conversation.id == session_id
        ).first()

        if not conversation:
            conversation = Conversation(id=session_id)
            db.add(conversation)
            db.commit()

        # Save user message
        user_message = Message(
            conversation_id=session_id,
            sender="user",
            text=request.message
        )
        db.add(user_message)
        db.commit()

        # Generate AI reply
        ai_reply = generate_reply(request.message)

        # Save AI reply
        ai_message = Message(
            conversation_id=session_id,
            sender="ai",
            text=ai_reply
        )
        db.add(ai_message)
        db.commit()

        return {
            "reply": ai_reply,
            "sessionId": session_id
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        print("BACKEND ERROR:", e)
        return {
            "reply": "Sorry, something went wrong on our side.",
            "sessionId": session_id
        }

    finally:
        db.close()
