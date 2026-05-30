from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import Flowable

W, H = A4

# ── Colors ──────────────────────────────────────────────────────────────────
TEAL      = colors.HexColor("#0F6E56")
TEAL_LT   = colors.HexColor("#E1F5EE")
AMBER     = colors.HexColor("#854F0B")
AMBER_LT  = colors.HexColor("#FAEEDA")
RED       = colors.HexColor("#A32D2D")
RED_LT    = colors.HexColor("#FCEBEB")
GRAY_DK   = colors.HexColor("#2C2C2A")
GRAY_MID  = colors.HexColor("#5F5E5A")
GRAY_LT   = colors.HexColor("#F1EFE8")
WHITE     = colors.white
CODE_BG   = colors.HexColor("#F1EFE8")
BLUE_DK   = colors.HexColor("#042C53")
BLUE_LT   = colors.HexColor("#E6F1FB")

# ── Styles ───────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def S(name, **kw):
    return ParagraphStyle(name, **kw)

cover_title = S("cover_title", fontSize=36, leading=44, textColor=WHITE,
                fontName="Helvetica-Bold", alignment=TA_CENTER)
cover_sub   = S("cover_sub",   fontSize=16, leading=24, textColor=colors.HexColor("#9FE1CB"),
                fontName="Helvetica", alignment=TA_CENTER)
cover_meta  = S("cover_meta",  fontSize=11, leading=16, textColor=colors.HexColor("#5DCAA5"),
                fontName="Helvetica", alignment=TA_CENTER)

sec_head    = S("sec_head",  fontSize=18, leading=24, textColor=WHITE,
                fontName="Helvetica-Bold", spaceBefore=6, spaceAfter=4)
sub_head    = S("sub_head",  fontSize=13, leading=18, textColor=TEAL,
                fontName="Helvetica-Bold", spaceBefore=10, spaceAfter=4)
q_style     = S("q_style",   fontSize=11, leading=16, textColor=GRAY_DK,
                fontName="Helvetica-Bold", spaceBefore=6, spaceAfter=2)
body        = S("body",      fontSize=10, leading=15, textColor=GRAY_DK,
                fontName="Helvetica", spaceAfter=4)
code_style  = S("code",      fontSize=8.5, leading=13, textColor=GRAY_DK,
                fontName="Courier", spaceAfter=2)
tip_style   = S("tip",       fontSize=9.5, leading=14, textColor=colors.HexColor("#085041"),
                fontName="Helvetica-Oblique", spaceAfter=4)
toc_style   = S("toc",       fontSize=11, leading=18, textColor=GRAY_DK,
                fontName="Helvetica")
badge_easy  = S("b_easy",    fontSize=8, textColor=colors.HexColor("#3B6D11"),
                fontName="Helvetica-Bold")
page_num    = S("page_num",  fontSize=9,  textColor=GRAY_MID,
                fontName="Helvetica", alignment=TA_RIGHT)

# ── Helpers ──────────────────────────────────────────────────────────────────
def code_block(text):
    lines = text.strip().split("\n")
    data = [[Paragraph(l.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;"), code_style)] for l in lines]
    t = Table(data, colWidths=[16.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0),(-1,-1), CODE_BG),
        ("BOX",        (0,0),(-1,-1), 0.5, colors.HexColor("#B4B2A9")),
        ("TOPPADDING",   (0,0),(-1,-1), 6),
        ("BOTTOMPADDING",(0,0),(-1,-1), 6),
        ("LEFTPADDING",  (0,0),(-1,-1), 10),
        ("RIGHTPADDING", (0,0),(-1,-1), 6),
        ("ROWBACKGROUNDS",(0,0),(-1,-1),[CODE_BG]),
    ]))
    return t

def tip_box(text):
    t = Table([[Paragraph("💡  " + text, tip_style)]], colWidths=[16.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0),(-1,-1), TEAL_LT),
        ("BOX",        (0,0),(-1,-1), 0.5, TEAL),
        ("TOPPADDING",   (0,0),(-1,-1), 7),
        ("BOTTOMPADDING",(0,0),(-1,-1), 7),
        ("LEFTPADDING",  (0,0),(-1,-1), 10),
        ("RIGHTPADDING", (0,0),(-1,-1), 10),
    ]))
    return t

def warn_box(text):
    t = Table([[Paragraph("⚡  " + text, S("wt", fontSize=9.5, leading=14,
               textColor=RED, fontName="Helvetica-Oblique"))]], colWidths=[16.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0),(-1,-1), RED_LT),
        ("BOX",        (0,0),(-1,-1), 0.5, RED),
        ("TOPPADDING",   (0,0),(-1,-1), 7),
        ("BOTTOMPADDING",(0,0),(-1,-1), 7),
        ("LEFTPADDING",  (0,0),(-1,-1), 10),
        ("RIGHTPADDING", (0,0),(-1,-1), 10),
    ]))
    return t

def section_header(title, subtitle=""):
    rows = [[Paragraph(title, sec_head)]]
    if subtitle:
        rows.append([Paragraph(subtitle, S("sh_sub", fontSize=10, textColor=colors.HexColor("#9FE1CB"),
                                           fontName="Helvetica"))])
    t = Table(rows, colWidths=[17.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), TEAL),
        ("TOPPADDING",   (0,0),(-1,-1), 10),
        ("BOTTOMPADDING",(0,0),(-1,-1), 10),
        ("LEFTPADDING",  (0,0),(-1,-1), 14),
        ("RIGHTPADDING", (0,0),(-1,-1), 14),
        ("ROWBACKGROUNDS",(0,0),(-1,-1),[TEAL]),
    ]))
    return t

def badge(text, level="easy"):
    colors_map = {"easy": (TEAL_LT, TEAL), "medium": (AMBER_LT, AMBER), "hard": (RED_LT, RED)}
    bg, fg = colors_map.get(level, (GRAY_LT, GRAY_DK))
    style = S(f"b_{level}", fontSize=8, textColor=fg, fontName="Helvetica-Bold")
    t = Table([[Paragraph(text.upper(), style)]], colWidths=[1.4*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), bg),
        ("TOPPADDING",   (0,0),(-1,-1), 2),
        ("BOTTOMPADDING",(0,0),(-1,-1), 2),
        ("LEFTPADDING",  (0,0),(-1,-1), 5),
        ("RIGHTPADDING", (0,0),(-1,-1), 5),
    ]))
    return t

def q_row(question, level):
    lvl_map = {"easy":"easy","medium":"medium","hard":"hard"}
    b = badge(level, lvl_map.get(level,"easy"))
    q = Paragraph(question, q_style)
    t = Table([[b, q]], colWidths=[1.6*cm, 15.1*cm])
    t.setStyle(TableStyle([
        ("VALIGN",       (0,0),(-1,-1), "TOP"),
        ("LEFTPADDING",  (0,0),(-1,-1), 0),
        ("RIGHTPADDING", (0,0),(-1,-1), 0),
        ("TOPPADDING",   (0,0),(-1,-1), 0),
        ("BOTTOMPADDING",(0,0),(-1,-1), 0),
    ]))
    return t

def hr():
    return HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#D3D1C7"), spaceAfter=6, spaceBefore=6)

def sp(n=6):
    return Spacer(1, n)

# ── Cover Page ────────────────────────────────────────────────────────────────
class ColorRect(Flowable):
    def __init__(self, w, h, color):
        Flowable.__init__(self)
        self.w, self.h, self.color = w, h, color
    def draw(self):
        self.canv.setFillColor(self.color)
        self.canv.rect(0, 0, self.w, self.h, fill=1, stroke=0)
    def wrap(self, *args):
        return self.w, self.h

# ── Page numbering ────────────────────────────────────────────────────────────
def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(GRAY_MID)
    canvas.drawString(1.5*cm, 1.0*cm, "Senior Python Backend Interview Guide  ·  FastAPI · PostgreSQL · System Design")
    canvas.drawRightString(W - 1.5*cm, 1.0*cm, f"Page {doc.page}")
    canvas.restoreState()

def on_cover(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(TEAL)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    canvas.restoreState()

# ── BUILD ─────────────────────────────────────────────────────────────────────
story = []

# COVER
story.append(Spacer(1, 4.5*cm))
story.append(Paragraph("Senior Python Backend", cover_title))
story.append(Paragraph("Interview Prep Guide", cover_title))
story.append(Spacer(1, 0.6*cm))
story.append(Paragraph("FastAPI · PostgreSQL · SQLAlchemy · System Design", cover_sub))
story.append(Spacer(1, 2*cm))
story.append(HRFlowable(width="60%", thickness=1, color=colors.HexColor("#5DCAA5"), hAlign="CENTER"))
story.append(Spacer(1, 2*cm))
story.append(Paragraph("LearnTube  ·  10-Minute Assessment Format", cover_meta))
story.append(Paragraph("Complete study guide — all questions with answers &amp; code", cover_meta))
story.append(Spacer(1, 1*cm))
story.append(Paragraph("Good luck, Utkrusht! 🚀", cover_meta))
story.append(PageBreak())

# ── SECTION 1: FastAPI ────────────────────────────────────────────────────────
story.append(section_header("1. FastAPI", "Core framework, routing, auth, async"))
story.append(sp(10))

# Q1
story.append(q_row("What is FastAPI? Why choose it over Flask or Django?", "easy"))
story.append(body.clone("b1") and Paragraph(
    "FastAPI is a modern ASGI-based Python web framework built on <b>Starlette</b> (routing/middleware) and "
    "<b>Pydantic</b> (validation). Key advantages:", body))
items = [
    ["Auto-generates interactive OpenAPI docs at /docs and /redoc"],
    ["Native async/await support — far better I/O throughput than Flask"],
    ["Type-hint-driven validation — no manual parsing of request data"],
    ["~300% faster than Flask in benchmarks (Uvicorn + async)"],
    ["Lighter than Django — ideal for microservices and APIs"],
]
t = Table(items, colWidths=[16.5*cm])
t.setStyle(TableStyle([
    ("FONTNAME",     (0,0),(-1,-1), "Helvetica"),
    ("FONTSIZE",     (0,0),(-1,-1), 10),
    ("TEXTCOLOR",    (0,0),(-1,-1), GRAY_DK),
    ("LEADING",      (0,0),(-1,-1), 15),
    ("LEFTPADDING",  (0,0),(-1,-1), 20),
    ("ROWBACKGROUNDS",(0,0),(-1,-1),[WHITE, GRAY_LT]),
    ("TOPPADDING",   (0,0),(-1,-1), 4),
    ("BOTTOMPADDING",(0,0),(-1,-1), 4),
]))
story.append(t)
story.append(tip_box("Interview tip: Say 'ASGI vs WSGI' — FastAPI uses ASGI which enables true async, Flask uses WSGI (sync)."))
story.append(hr())

# Q2
story.append(q_row("Explain Dependency Injection with Depends(). Show an example.", "medium"))
story.append(Paragraph("Depends() lets you declare reusable logic (DB sessions, auth, config) that FastAPI resolves per-request automatically.", body))
story.append(code_block("""from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db          # yield = generator-based dependency
    finally:
        db.close()        # always runs, even on exception

@app.get("/users/{id}")
def get_user(id: int, db: Session = Depends(get_db)):
    return db.query(User).filter(User.id == id).first()

# Testing: override dependencies easily
app.dependency_overrides[get_db] = lambda: mock_db_session"""))
story.append(tip_box("Dependencies can be async, nested (Depends inside Depends), and scoped (request, lifespan)."))
story.append(hr())

# Q3
story.append(q_row("How do you implement JWT authentication in FastAPI?", "medium"))
story.append(Paragraph("Use <b>python-jose</b> for JWT encoding/decoding + <b>passlib</b> for password hashing. Inject via OAuth2PasswordBearer dependency.", body))
story.append(code_block("""from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
SECRET_KEY = "your-secret"
ALGORITHM = "HS256"

def create_access_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
    except JWTError:
        raise HTTPException(401, "Invalid token")
    return get_user(user_id)

@app.get("/me")
async def me(user = Depends(get_current_user)):
    return user"""))
story.append(tip_box("Flow: POST /token → return {access_token, token_type} → client sends 'Authorization: Bearer <token>' → verify in Depends."))
story.append(hr())

# Q4
story.append(q_row("What are Background Tasks? When to use vs Celery?", "medium"))
tbl_data = [
    [Paragraph("<b>Background Tasks</b>", body), Paragraph("<b>Celery</b>", body)],
    ["Runs in same process", "Separate worker processes"],
    ["No setup needed", "Needs Redis/RabbitMQ broker"],
    ["Light tasks: send email, log", "Heavy: video encode, reports"],
    ["No retry on failure", "Built-in retry, scheduling"],
    ["Dies with server crash", "Survives server crash"],
]
bt = Table(tbl_data, colWidths=[8*cm, 8.5*cm])
bt.setStyle(TableStyle([
    ("BACKGROUND",   (0,0),(-1,0), TEAL),
    ("TEXTCOLOR",    (0,0),(-1,0), WHITE),
    ("FONTNAME",     (0,0),(-1,0), "Helvetica-Bold"),
    ("FONTNAME",     (0,1),(-1,-1), "Helvetica"),
    ("FONTSIZE",     (0,0),(-1,-1), 9.5),
    ("GRID",         (0,0),(-1,-1), 0.5, colors.HexColor("#D3D1C7")),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE, GRAY_LT]),
    ("TOPPADDING",   (0,0),(-1,-1), 5),
    ("BOTTOMPADDING",(0,0),(-1,-1), 5),
    ("LEFTPADDING",  (0,0),(-1,-1), 8),
]))
story.append(bt)
story.append(sp(6))
story.append(code_block("""@app.post("/send-email")
async def send(background_tasks: BackgroundTasks, email: str):
    background_tasks.add_task(send_email_func, email)
    return {"message": "Email queued"}"""))
story.append(tip_box("LearnTube likely uses Celery for video transcoding — mentioning this shows domain awareness."))
story.append(hr())

# Q5
story.append(q_row("Explain request validation. What happens on validation failure?", "easy"))
story.append(Paragraph("FastAPI uses Pydantic models for automatic request validation. Define a model as the body parameter type:", body))
story.append(code_block("""from pydantic import BaseModel, Field, validator

class CourseCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    price: float = Field(..., gt=0)
    category_id: int

    @validator("title")
    def title_must_not_be_blank(cls, v):
        if not v.strip():
            raise ValueError("Title cannot be blank")
        return v

@app.post("/courses")
def create_course(course: CourseCreate):  # FastAPI validates automatically
    ...
# On failure → 422 Unprocessable Entity with field-level error details"""))
story.append(hr())

# Q6
story.append(q_row("Write a middleware that logs request method, path, and duration.", "medium"))
story.append(code_block("""import time
from fastapi import Request

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = round((time.time() - start_time) * 1000, 2)
    print(f"{request.method} {request.url.path} "
          f"→ {response.status_code} [{duration}ms]")
    return response

# Other common middleware:
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_methods=["*"], allow_headers=["*"])"""))
story.append(hr())

# Q7
story.append(q_row("How do you structure a large FastAPI app with multiple routers?", "medium"))
story.append(code_block("""# app/routers/courses.py
from fastapi import APIRouter
router = APIRouter(prefix="/courses", tags=["courses"])

@router.get("/")
async def list_courses(): ...

@router.post("/")
async def create_course(): ...

# app/main.py
from app.routers import courses, users, auth
app.include_router(auth.router)
app.include_router(users.router, prefix="/api/v1")
app.include_router(courses.router, prefix="/api/v1")

# Recommended folder structure:
# app/
#   main.py, routers/, models/, schemas/, services/, db/, core/"""))
story.append(hr())

# Q8
story.append(q_row("How do you write unit tests for FastAPI routes?", "medium"))
story.append(code_block("""from fastapi.testclient import TestClient
from app.main import app
from app.db import get_db

def mock_db():
    yield fake_session  # your mock session

app.dependency_overrides[get_db] = mock_db  # override dependency

client = TestClient(app)

def test_get_course():
    response = client.get("/courses/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_create_course_validation():
    response = client.post("/courses", json={"price": -10})
    assert response.status_code == 422  # validation failure"""))
story.append(sp(8))
story.append(PageBreak())

# ── SECTION 2: PostgreSQL ─────────────────────────────────────────────────────
story.append(section_header("2. PostgreSQL", "Queries, indexes, optimization, transactions"))
story.append(sp(10))

story.append(q_row("Explain INNER JOIN vs LEFT JOIN vs FULL OUTER JOIN.", "easy"))
story.append(code_block("""-- INNER JOIN: only rows with match in BOTH tables
SELECT u.name, o.total FROM users u
INNER JOIN orders o ON u.id = o.user_id;

-- LEFT JOIN: ALL rows from left + matching right (NULL if no match)
SELECT u.name, o.total FROM users u
LEFT JOIN orders o ON u.id = o.user_id;
-- Users with no orders will appear with NULL total

-- FULL OUTER JOIN: ALL rows from BOTH tables
SELECT u.name, o.total FROM users u
FULL OUTER JOIN orders o ON u.id = o.user_id;"""))
story.append(hr())

story.append(q_row("What are indexes? Composite index vs Partial index?", "medium"))
story.append(Paragraph("Indexes speed up queries by avoiding full table scans. PostgreSQL supports B-tree (default), GIN, GiST, Hash.", body))
story.append(code_block("""-- Standard index
CREATE INDEX idx_courses_category ON courses(category_id);

-- Composite index: good for queries filtering BOTH columns
-- Rule: leftmost prefix — (a,b) helps filter on 'a' alone, NOT 'b' alone
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- Partial index: adds WHERE clause — smaller, faster for targeted queries
CREATE INDEX idx_active_orders ON orders(user_id)
WHERE status = 'active';  -- only indexes active orders

-- Check if index is used:
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 5 AND status = 'active';"""))
story.append(tip_box("Partial indexes are often overlooked but can be 10x smaller and faster than full indexes for filtered queries."))
story.append(hr())

story.append(q_row("What is EXPLAIN ANALYZE? How do you optimize a slow query?", "medium"))
story.append(code_block("""EXPLAIN ANALYZE SELECT * FROM courses WHERE category_id = 3;
-- Look for:
-- Seq Scan (bad on large tables) → add index
-- High 'rows' estimate vs actual → run ANALYZE to update stats
-- Nested Loop on large sets → may need Hash Join
-- High 'cost' → examine subqueries, joins

-- Step-by-step approach:
-- 1. EXPLAIN ANALYZE to find bottleneck
-- 2. Check for missing indexes
-- 3. Run VACUUM ANALYZE if stats are stale
-- 4. Rewrite subqueries as JOINs or CTEs
-- 5. Consider materialized views for complex aggregations"""))
story.append(hr())

story.append(q_row("Explain PostgreSQL isolation levels.", "hard"))
iso_data = [
    [Paragraph("<b>Level</b>", body), Paragraph("<b>Dirty Read</b>", body), Paragraph("<b>Non-repeat Read</b>", body), Paragraph("<b>Phantom</b>", body)],
    ["Read Committed (default)", "No", "Possible", "Possible"],
    ["Repeatable Read", "No", "No", "No*"],
    ["Serializable", "No", "No", "No"],
]
it = Table(iso_data, colWidths=[5.5*cm, 3.5*cm, 4*cm, 3.5*cm])
it.setStyle(TableStyle([
    ("BACKGROUND",   (0,0),(-1,0), TEAL),
    ("TEXTCOLOR",    (0,0),(-1,0), WHITE),
    ("FONTNAME",     (0,0),(-1,0), "Helvetica-Bold"),
    ("FONTNAME",     (0,1),(-1,-1), "Helvetica"),
    ("FONTSIZE",     (0,0),(-1,-1), 9.5),
    ("GRID",         (0,0),(-1,-1), 0.5, colors.HexColor("#D3D1C7")),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE, GRAY_LT]),
    ("TOPPADDING",   (0,0),(-1,-1), 5),
    ("BOTTOMPADDING",(0,0),(-1,-1), 5),
    ("LEFTPADDING",  (0,0),(-1,-1), 8),
    ("ALIGN",        (1,0),(-1,-1), "CENTER"),
]))
story.append(it)
story.append(sp(4))
story.append(Paragraph("* PostgreSQL's Repeatable Read also prevents phantoms due to MVCC snapshot implementation.", 
             S("note", fontSize=9, textColor=GRAY_MID, fontName="Helvetica-Oblique")))
story.append(hr())

story.append(q_row("What is a deadlock? How does PostgreSQL handle it?", "hard"))
story.append(code_block("""-- Deadlock: TX1 holds lock on A, waits for B
--            TX2 holds lock on B, waits for A  → circular wait

-- PostgreSQL DETECTS deadlocks automatically and raises:
-- ERROR 40P01: deadlock detected — one TX is rolled back

-- Prevention strategies:
-- 1. Always lock tables in the SAME ORDER across transactions
-- 2. Keep transactions SHORT
-- 3. Use SELECT FOR UPDATE SKIP LOCKED for queue-style processing:
SELECT id FROM tasks
WHERE status = 'pending'
ORDER BY created_at
LIMIT 1
FOR UPDATE SKIP LOCKED;  -- skip rows locked by other workers"""))
story.append(tip_box("SKIP LOCKED is ideal for job queues — each worker picks a different task without deadlocking."))
story.append(hr())

story.append(q_row("How do you implement efficient pagination in PostgreSQL?", "medium"))
story.append(code_block("""-- ❌ OFFSET pagination — SLOW for large pages (scans all prior rows)
SELECT * FROM courses ORDER BY id LIMIT 20 OFFSET 10000;

-- ✅ Keyset (cursor) pagination — FAST regardless of depth
SELECT * FROM courses
WHERE id > :last_seen_id    -- last id from previous page
ORDER BY id
LIMIT 20;

-- For the API:
# GET /courses?after_id=500&limit=20
@app.get("/courses")
async def list_courses(after_id: int = 0, limit: int = 20, db = Depends(get_db)):
    return db.query(Course).filter(Course.id > after_id).limit(limit).all()"""))
story.append(hr())

story.append(q_row("What are Window Functions? Write a query for top 3 courses per category.", "hard"))
story.append(code_block("""-- Window functions: compute across a set of rows related to current row
-- RANK(), ROW_NUMBER(), DENSE_RANK(), LAG(), LEAD(), SUM() OVER(...)

-- Top 3 most-enrolled courses per category:
SELECT category, course_id, title, enrollments FROM (
    SELECT
        c.category,
        c.id AS course_id,
        c.title,
        c.enrollments,
        RANK() OVER (
            PARTITION BY c.category      -- restart ranking per category
            ORDER BY c.enrollments DESC  -- rank by most enrolled
        ) AS rk
    FROM courses c
) ranked
WHERE rk <= 3
ORDER BY category, rk;

-- Other useful window functions:
-- Running total: SUM(revenue) OVER (ORDER BY date)
-- Row number:    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at)"""))
story.append(hr())

story.append(q_row("Explain JSONB in PostgreSQL. When would you use it?", "medium"))
story.append(code_block("""-- JSON: stores raw text
-- JSONB: stores parsed binary → faster queries, supports GIN index
-- Use JSONB for dynamic/schemaless attributes

-- GIN index for JSONB
CREATE INDEX idx_metadata ON users USING GIN(metadata);

-- Query JSONB
SELECT * FROM users WHERE metadata->>'plan' = 'pro';
SELECT * FROM users WHERE metadata @> '{"role": "admin"}';
SELECT metadata->'preferences'->'theme' FROM users WHERE id = 1;

-- Real use case: user preferences, course tags, feature flags
ALTER TABLE users ADD COLUMN metadata JSONB DEFAULT '{}';"""))
story.append(sp(8))
story.append(PageBreak())

# ── SECTION 3: SQLAlchemy / ORM ───────────────────────────────────────────────
story.append(section_header("3. SQLAlchemy & ORM", "Models, relationships, async, migrations"))
story.append(sp(10))

story.append(q_row("What is the N+1 query problem? How do you fix it?", "medium"))
story.append(code_block("""# ❌ N+1 problem: 1 query for users + N queries for each user's courses
users = db.query(User).all()
for user in users:
    print(user.courses)  # triggers a new query per user = N+1 total!

# ✅ Fix with eager loading (joinedload = single JOIN query)
from sqlalchemy.orm import joinedload, selectinload

users = db.query(User).options(
    joinedload(User.courses)  # single query with JOIN
).all()

# For large collections, selectinload is better (avoids JOIN blowup)
users = db.query(User).options(
    selectinload(User.courses)  # emits 2 queries: one for users, one IN query
).all()"""))
story.append(warn_box("N+1 is one of the most common production performance bugs. Interviewers love this question."))
story.append(hr())

story.append(q_row("How do you manage async database sessions in FastAPI?", "hard"))
story.append(code_block("""from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

# Use asyncpg driver
DATABASE_URL = "postgresql+asyncpg://user:password@localhost/db"
engine = create_async_engine(DATABASE_URL, pool_size=10, max_overflow=20)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@app.get("/courses")
async def list_courses(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).where(Course.active == True))
    return result.scalars().all()

# For writes:
@app.post("/courses")
async def create(data: CourseCreate, db: AsyncSession = Depends(get_db)):
    course = Course(**data.dict())
    db.add(course)
    await db.commit()
    await db.refresh(course)
    return course"""))
story.append(hr())

story.append(q_row("How do you define models and relationships in SQLAlchemy?", "easy"))
story.append(code_block("""from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, DeclarativeBase
from datetime import datetime

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id         = Column(Integer, primary_key=True, index=True)
    email      = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    courses    = relationship("Enrollment", back_populates="user")

class Course(Base):
    __tablename__ = "courses"
    id          = Column(Integer, primary_key=True)
    title       = Column(String(200), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    category    = relationship("Category", back_populates="courses")
    enrollments = relationship("Enrollment", back_populates="course")

class Enrollment(Base):
    __tablename__ = "enrollments"
    user_id    = Column(Integer, ForeignKey("users.id"), primary_key=True)
    course_id  = Column(Integer, ForeignKey("courses.id"), primary_key=True)
    progress   = Column(Integer, default=0)  # 0-100"""))
story.append(hr())

story.append(q_row("How do you run database migrations with Alembic?", "easy"))
story.append(code_block("""# 1. Initialize
alembic init alembic

# 2. Configure alembic.ini
sqlalchemy.url = postgresql://user:pass@localhost/dbname

# 3. Update env.py to import your models
from app.models import Base
target_metadata = Base.metadata

# 4. Autogenerate migration
alembic revision --autogenerate -m "add courses table"

# 5. Review generated migration file! (always review before applying)

# 6. Apply migration
alembic upgrade head

# 7. Rollback
alembic downgrade -1

# 8. Check current version
alembic current"""))
story.append(sp(8))
story.append(PageBreak())

# ── SECTION 4: Python Core ────────────────────────────────────────────────────
story.append(section_header("4. Python Core Concepts", "Async, GIL, decorators, Pydantic"))
story.append(sp(10))

story.append(q_row("Explain Python's GIL and its impact on FastAPI.", "hard"))
story.append(Paragraph("The Global Interpreter Lock (GIL) prevents multiple threads from executing Python bytecode simultaneously in CPython.", body))
story.append(code_block("""# GIL impact:
# CPU-bound tasks: GIL blocks parallelism → use multiprocessing
# I/O-bound tasks: GIL RELEASES during I/O waits → async works perfectly

# FastAPI's async def routes run on the event loop
# When you 'await' a DB call, the event loop handles other requests
# This is why FastAPI is fast for I/O-heavy APIs (like a backend serving courses)

import asyncio

async def fetch_user(db, user_id):    # GIL released during await
    return await db.execute(...)

async def fetch_course(db, course_id):
    return await db.execute(...)

# Run concurrently — both DB calls run "at the same time"
user, course = await asyncio.gather(
    fetch_user(db, 1),
    fetch_course(db, 42)
)"""))
story.append(tip_box("Key answer: 'FastAPI with async and asyncpg effectively bypasses GIL issues for I/O because GIL is released during network/disk waits.'"))
story.append(hr())

story.append(q_row("What is the difference between async def and def routes in FastAPI?", "medium"))
story.append(code_block("""# async def → runs in the event loop (use for async DB calls, HTTP requests)
@app.get("/users")
async def list_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))  # non-blocking
    return result.scalars().all()

# Regular def → FastAPI runs in a thread pool automatically (doesn't block event loop)
@app.get("/sync-users")
def list_users_sync(db: Session = Depends(get_db)):
    return db.query(User).all()  # blocking, but in threadpool — OK

# ❌ WRONG: sync blocking code inside async def
@app.get("/bad")
async def bad_endpoint():
    time.sleep(5)  # blocks event loop! All requests stall
    return {}

# ✅ CORRECT: use run_in_executor for sync blocking in async context
import asyncio
@app.get("/ok")
async def ok_endpoint():
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, blocking_function)
    return result"""))
story.append(hr())

story.append(q_row("Write a caching decorator using functools.lru_cache and one with Redis.", "medium"))
story.append(code_block("""# Simple in-memory cache (single process only)
from functools import lru_cache

@lru_cache(maxsize=128)
def get_category(category_id: int):
    return db.query(Category).filter_by(id=category_id).first()

# Redis cache decorator for distributed caching
import redis, json, functools
r = redis.Redis(host='localhost', port=6379)

def redis_cache(ttl=300):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            key = f"{func.__name__}:{args}:{kwargs}"
            cached = r.get(key)
            if cached:
                return json.loads(cached)
            result = await func(*args, **kwargs)
            r.setex(key, ttl, json.dumps(result))
            return result
        return wrapper
    return decorator

@redis_cache(ttl=600)
async def get_popular_courses():
    ...  # expensive DB query, cached for 10 mins"""))
story.append(hr())

story.append(q_row("What is Pydantic v2? How does it differ from dataclasses?", "easy"))
story.append(code_block("""from pydantic import BaseModel, Field, field_validator
from typing import Optional

class CourseResponse(BaseModel):
    id: int
    title: str
    price: float = Field(gt=0, description="Must be positive")
    instructor: Optional[str] = None

    @field_validator("title")
    @classmethod
    def strip_title(cls, v: str) -> str:
        return v.strip()

    model_config = {"from_attributes": True}  # replaces orm_mode in v1

# vs dataclasses: no runtime validation, no JSON schema, no coercion
# Pydantic v2: Rust core (pydantic-core) → 5-50x faster than v1
# Use model_validate(obj) instead of from_orm(obj) in v2"""))
story.append(sp(8))
story.append(PageBreak())

# ── SECTION 5: System Design ──────────────────────────────────────────────────
story.append(section_header("5. System Design", "Scale, caching, search, architecture"))
story.append(sp(10))

story.append(q_row("Design a course progress tracking system for 1M+ users.", "hard"))
story.append(Paragraph("<b>Schema design:</b>", body))
story.append(code_block("""-- Core tables
CREATE TABLE progress (
    user_id    INT REFERENCES users(id),
    lesson_id  INT REFERENCES lessons(id),
    completed  BOOLEAN DEFAULT FALSE,
    pct        SMALLINT DEFAULT 0,  -- 0-100
    updated_at TIMESTAMP,
    PRIMARY KEY (user_id, lesson_id)
);

-- Partial index for fast "in-progress" queries
CREATE INDEX idx_active_progress ON progress(user_id, lesson_id)
WHERE completed = FALSE;

-- Course completion summary (denormalized for performance)
CREATE TABLE course_progress (
    user_id           INT,
    course_id         INT,
    completed_lessons INT DEFAULT 0,
    total_lessons     INT,
    pct               SMALLINT DEFAULT 0,
    PRIMARY KEY (user_id, course_id)
);"""))
story.append(Paragraph("<b>Architecture for scale:</b>", body))
story.append(code_block("""# High write volume strategy:
# 1. Client sends progress events → FastAPI endpoint (lightweight)
# 2. Batch events in Redis: LPUSH progress:events {user_id, lesson_id, pct}
# 3. Celery worker processes batch every 30s → bulk upsert to Postgres
# 4. Cache course_progress in Redis (read-heavy)

# Bulk upsert in PostgreSQL (efficient for batch writes):
INSERT INTO progress (user_id, lesson_id, pct, completed, updated_at)
VALUES (%s, %s, %s, %s, NOW())
ON CONFLICT (user_id, lesson_id)
DO UPDATE SET pct = EXCLUDED.pct, updated_at = NOW();"""))
story.append(tip_box("The key insight: 'write buffering with Redis + batch Postgres upserts' reduces write amplification by 100x."))
story.append(hr())

story.append(q_row("How would you implement rate limiting in a distributed FastAPI app?", "hard"))
story.append(code_block("""# Use Redis sliding window rate limiter (works across multiple servers)
import redis, time
r = redis.Redis()

def is_rate_limited(user_id: str, limit: int = 100, window: int = 60) -> bool:
    key = f"ratelimit:{user_id}"
    now = time.time()
    pipe = r.pipeline()
    # Remove old entries outside the window
    pipe.zremrangebyscore(key, 0, now - window)
    # Count current requests in window
    pipe.zcard(key)
    # Add current request
    pipe.zadd(key, {str(now): now})
    pipe.expire(key, window)
    _, count, *_ = pipe.execute()
    return count >= limit

# In FastAPI as a dependency:
async def rate_limit(request: Request, user=Depends(get_current_user)):
    if is_rate_limited(str(user.id)):
        raise HTTPException(429, "Too many requests")

# Library option: slowapi (Flask-Limiter port for FastAPI)
from slowapi import Limiter
from slowapi.util import get_remote_address
limiter = Limiter(key_func=get_remote_address, storage_uri="redis://localhost")

@app.get("/courses")
@limiter.limit("100/minute")
async def list_courses(request: Request): ..."""))
story.append(hr())

story.append(q_row("How would you add full-text search to a course catalog?", "medium"))
story.append(code_block("""-- Option 1: PostgreSQL full-text search (good for <100k courses)
ALTER TABLE courses ADD COLUMN search_vector tsvector;

UPDATE courses SET search_vector =
    to_tsvector('english', title || ' ' || coalesce(description, ''));

CREATE INDEX idx_courses_fts ON courses USING GIN(search_vector);

-- Search:
SELECT * FROM courses
WHERE search_vector @@ plainto_tsquery('english', 'python fastapi')
ORDER BY ts_rank(search_vector, plainto_tsquery('python fastapi')) DESC;

-- Option 2: Elasticsearch / Typesense (for scale + better relevance)
# Index courses on create/update → ES index
# FastAPI → ES client → ranked results with highlighting, fuzzy match, facets
# Typesense is simpler to self-host, great for <10M docs"""))
story.append(hr())

story.append(q_row("Design the API for a video streaming backend (like LearnTube).", "hard"))
story.append(code_block("""# Upload flow:
# POST /videos/upload → pre-signed S3 URL → client uploads directly to S3
# S3 event → Celery task → FFmpeg transcode to 360p, 720p, 1080p HLS
# Store manifest (.m3u8) and segments (.ts) back to S3/CDN

# Playback flow:
# GET /lessons/{id}/stream → generate signed CloudFront URL for .m3u8
# Client player requests segments (signed URLs auto-expire)

# Progress tracking (lightweight, high-frequency):
# POST /lessons/{id}/progress  body: {pct: 67, timestamp: 142.3}
# → buffer in Redis, batch write to Postgres

# Endpoints:
# POST   /courses/{id}/enroll
# GET    /courses/{id}/lessons     → ordered lesson list
# GET    /lessons/{id}/stream      → signed manifest URL
# POST   /lessons/{id}/progress    → lightweight event write
# GET    /users/me/progress        → cached from Redis"""))
story.append(sp(8))
story.append(PageBreak())

# ── SECTION 6: Quick Reference ────────────────────────────────────────────────
story.append(section_header("6. Quick Reference", "Cheatsheet for last-minute review"))
story.append(sp(10))

story.append(Paragraph("FastAPI Essential Patterns", sub_head))
story.append(code_block("""# App setup
from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup: init DB connections, caches
    yield
    # shutdown: close connections

app = FastAPI(title="LearnTube API", version="1.0", lifespan=lifespan)

# Common HTTP exceptions
raise HTTPException(status_code=404, detail="Course not found")
raise HTTPException(status_code=401, detail="Not authenticated")
raise HTTPException(status_code=403, detail="Not authorized")
raise HTTPException(status_code=422, detail="Validation error")  # auto
raise HTTPException(status_code=429, detail="Rate limit exceeded")"""))

story.append(Paragraph("PostgreSQL Quick Reference", sub_head))
cheat_data = [
    [Paragraph("<b>Task</b>", body), Paragraph("<b>SQL Pattern</b>", body)],
    ["Upsert",          "INSERT ... ON CONFLICT DO UPDATE SET ..."],
    ["Window rank",     "RANK() OVER (PARTITION BY x ORDER BY y DESC)"],
    ["Pagination",      "WHERE id > :last_id ORDER BY id LIMIT 20"],
    ["Full-text",       "WHERE col @@ plainto_tsquery('english', :q)"],
    ["JSON query",      "WHERE data->>'key' = 'value'"],
    ["SKIP LOCKED",     "SELECT ... FOR UPDATE SKIP LOCKED"],
    ["CTE",             "WITH cte AS (SELECT ...) SELECT * FROM cte"],
    ["Explain",         "EXPLAIN (ANALYZE, BUFFERS) SELECT ..."],
]
ct = Table(cheat_data, colWidths=[4.5*cm, 12*cm])
ct.setStyle(TableStyle([
    ("BACKGROUND",   (0,0),(-1,0), TEAL),
    ("TEXTCOLOR",    (0,0),(-1,0), WHITE),
    ("FONTNAME",     (0,0),(-1,0), "Helvetica-Bold"),
    ("FONTNAME",     (0,1),(-1,-1), "Courier"),
    ("FONTSIZE",     (0,0),(-1,0), 10),
    ("FONTSIZE",     (0,1),(-1,-1), 9),
    ("GRID",         (0,0),(-1,-1), 0.5, colors.HexColor("#D3D1C7")),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE, GRAY_LT]),
    ("TOPPADDING",   (0,0),(-1,-1), 5),
    ("BOTTOMPADDING",(0,0),(-1,-1), 5),
    ("LEFTPADDING",  (0,0),(-1,-1), 8),
    ("VALIGN",       (0,0),(-1,-1), "MIDDLE"),
]))
story.append(ct)
story.append(sp(10))

story.append(Paragraph("Interview Answer Framework (10-min format)", sub_head))
framework_data = [
    [Paragraph("<b>Step</b>", body), Paragraph("<b>What to say</b>", body), Paragraph("<b>Time</b>", body)],
    ["1. WHAT",    "Define the concept in one sentence",              "10 sec"],
    ["2. WHY",     "Explain when/why you'd use it",                  "20 sec"],
    ["3. HOW",     "Give a concrete code example or SQL",            "60 sec"],
    ["4. GOTCHA",  "Mention a tradeoff, edge case, or common mistake","20 sec"],
]
ft = Table(framework_data, colWidths=[2.5*cm, 10.5*cm, 3.5*cm])
ft.setStyle(TableStyle([
    ("BACKGROUND",   (0,0),(-1,0), TEAL),
    ("TEXTCOLOR",    (0,0),(-1,0), WHITE),
    ("FONTNAME",     (0,0),(-1,0), "Helvetica-Bold"),
    ("FONTNAME",     (0,1),(-1,-1), "Helvetica"),
    ("FONTSIZE",     (0,0),(-1,-1), 10),
    ("GRID",         (0,0),(-1,-1), 0.5, colors.HexColor("#D3D1C7")),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE, GRAY_LT]),
    ("TOPPADDING",   (0,0),(-1,-1), 6),
    ("BOTTOMPADDING",(0,0),(-1,-1), 6),
    ("LEFTPADDING",  (0,0),(-1,-1), 8),
    ("ALIGN",        (2,0),(-1,-1), "CENTER"),
]))
story.append(ft)
story.append(sp(10))

story.append(Paragraph("Top 10 Must-Know Topics for LearnTube Interview", sub_head))
must_know = [
    ["#", "Topic", "Why it matters for LearnTube"],
    ["1",  "Async FastAPI + asyncpg",         "High I/O throughput for course delivery"],
    ["2",  "N+1 query fix (selectinload)",     "ORM performance — common production bug"],
    ["3",  "Keyset pagination",                "Large course catalogs — OFFSET is too slow"],
    ["4",  "JWT auth flow",                    "Secure course access control"],
    ["5",  "Celery + Redis",                   "Video processing, email, background jobs"],
    ["6",  "PostgreSQL window functions",      "Analytics: top courses, user rankings"],
    ["7",  "Redis caching pattern",            "Read-heavy course content caching"],
    ["8",  "EXPLAIN ANALYZE",                  "Query optimization skills"],
    ["9",  "Alembic migrations",               "Schema management in production"],
    ["10", "Dependency injection (Depends)",   "Testable, clean FastAPI architecture"],
]
mt = Table(must_know, colWidths=[0.8*cm, 5.5*cm, 10.4*cm])
mt.setStyle(TableStyle([
    ("BACKGROUND",   (0,0),(-1,0), GRAY_DK),
    ("TEXTCOLOR",    (0,0),(-1,0), WHITE),
    ("FONTNAME",     (0,0),(-1,0), "Helvetica-Bold"),
    ("FONTNAME",     (0,1),(-1,-1), "Helvetica"),
    ("FONTSIZE",     (0,0),(-1,-1), 9.5),
    ("GRID",         (0,0),(-1,-1), 0.5, colors.HexColor("#D3D1C7")),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE, GRAY_LT]),
    ("TOPPADDING",   (0,0),(-1,-1), 5),
    ("BOTTOMPADDING",(0,0),(-1,-1), 5),
    ("LEFTPADDING",  (0,0),(-1,-1), 8),
    ("ALIGN",        (0,0),(0,-1), "CENTER"),
    ("FONTNAME",     (0,1),(0,-1), "Helvetica-Bold"),
    ("TEXTCOLOR",    (0,1),(0,-1), TEAL),
]))
story.append(mt)
story.append(sp(14))

# Final tip box
final = Table([[Paragraph(
    "You've got this, Utkrusht! Focus on the WHY behind each answer. "
    "Interviewers want to see how you think, not just what you've memorized. "
    "If you don't know something, say: 'I'd approach it by...' and reason through it. Good luck tonight! 🚀",
    S("final_tip", fontSize=11, leading=17, textColor=WHITE, fontName="Helvetica")
)]], colWidths=[16.5*cm])
final.setStyle(TableStyle([
    ("BACKGROUND",   (0,0),(-1,-1), TEAL),
    ("TOPPADDING",   (0,0),(-1,-1), 14),
    ("BOTTOMPADDING",(0,0),(-1,-1), 14),
    ("LEFTPADDING",  (0,0),(-1,-1), 16),
    ("RIGHTPADDING", (0,0),(-1,-1), 16),
    ("ROUNDEDCORNERS", [6]),
]))
story.append(final)

# ── Build ─────────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    "/mnt/user-data/outputs/LearnTube_Python_Interview_Guide.pdf",
    pagesize=A4,
    leftMargin=1.5*cm, rightMargin=1.5*cm,
    topMargin=1.5*cm, bottomMargin=1.8*cm,
)

def first_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(TEAL)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    canvas.restoreState()

def later_pages(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(GRAY_MID)
    canvas.drawString(1.5*cm, 1.0*cm,
        "Senior Python Backend Interview Guide  ·  FastAPI · PostgreSQL · System Design")
    canvas.drawRightString(W - 1.5*cm, 1.0*cm, f"Page {doc.page}")
    canvas.restoreState()

doc.build(story, onFirstPage=first_page, onLaterPages=later_pages)
print("PDF generated successfully!")
