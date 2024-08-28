import logging
from fastapi import FastAPI, Request, Form, BackgroundTasks
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import asyncio

from src.scrapers.professor_scraper import ProfessorScraper
from src.cold_emailer import ColdEmailer
from src.config import OPENAI_API_KEY, VECTOR_DB_PATH
from src.database.vector_db import VectorDB
from src.embedders.interest_embedder import InterestEmbedder

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

api_keys = {
    'openai': OPENAI_API_KEY
}

scraper = ProfessorScraper()
emailer = ColdEmailer(api_keys)
interest_embedder = InterestEmbedder()

vector_db = None

async def initialize_vector_db(vector_db, scraper, embedder, max_retries=1):
    universities = ["Stanford University", "MIT", "Harvard University"]
    total_professors = 0
    for university in universities:
        #professors = await scrape_professors_with_retry(scraper, university, max_retries)
        professors = [{'name': 'David H. Autor', 'email': 'a@a.com', 'interests': ["NLP"], 'affiliation': 'MIT'}]
        print(professors)
        for prof in professors:
            interests = ", ".join(prof.get('interests', []))
            if interests:
                try:
                    embedding = await asyncio.to_thread(embedder.embed, interests)
                    vector_db.add(embedding, prof)
                    total_professors += 1
                except Exception as e:
                    logger.error(f"Error adding professor {prof['name']}: {str(e)}")
    
    if total_professors == 0:
        logger.error("No professors were added to the VectorDB. Check the scraping process.")
    else:
        logger.info(f"Initialized VectorDB with {total_professors} professors")
        vector_db.save(VECTOR_DB_PATH)

async def scrape_professors_with_retry(scraper, university, max_retries):
    for attempt in range(max_retries):
        logger.info(f"Scraping professors from {university} (Attempt {attempt + 1})")
        professors = await asyncio.to_thread(scraper.search_professors, university, max_professors=10)
        logger.info(f"Found {len(professors)} professors from {university}")
        if professors:
            return professors
        if attempt < max_retries - 1:
            logger.warning(f"No professors found for {university}. Retrying...")
            await asyncio.sleep(5)  # Wait 5 seconds before retrying
    return []

async def initialize_vector_db_background():
    global vector_db
    try:
        vector_db = VectorDB.load(VECTOR_DB_PATH)
        logger.info("VectorDB loaded successfully")
        if len(vector_db.professors) == 0:
            logger.warning("VectorDB is empty, initializing with scraped data")
            await initialize_vector_db(vector_db, scraper, interest_embedder)
    except FileNotFoundError:
        logger.warning("VectorDB not found, initializing new one with scraped data")
        vector_db = VectorDB(dimension=384)
        await initialize_vector_db(vector_db, scraper, interest_embedder)
    except Exception as e:
        logger.error(f"Error loading or initializing VectorDB: {str(e)}")
        vector_db = None  # Set to None to indicate initialization failure

@app.on_event("startup")
async def startup_event():
    background_tasks = BackgroundTasks()
    background_tasks.add_task(initialize_vector_db_background)
    # Don't wait for the background task to complete
    asyncio.create_task(background_tasks())

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate_email", response_class=HTMLResponse)
async def generate_email(
    request: Request,
    name: str = Form(...),
    interests: str = Form(...),
    achievements: str = Form(...)
):
    try:
        logger.info(f"Generating email for {name} with interests: {interests}")
        
        if vector_db is None or len(vector_db.professors) == 0:
            logger.error("VectorDB is not initialized or empty. No professors available.")
            return templates.TemplateResponse(
                "result.html",
                {
                    "request": request,
                    "error": "No professors available in the database. Please try again later."
                }
            )

        logger.info("Embedding interests...")
        interest_embedding = interest_embedder.embed(interests)
        logger.info(f"Interest embedding generated with shape: {interest_embedding.shape}")

        logger.info("Searching for similar professors...")
        similar_professors = vector_db.search(interest_embedding, k=5)
        logger.info(f"Found {len(similar_professors)} similar professors")

        if not similar_professors:
            logger.warning("No similar professors found")
            return templates.TemplateResponse(
                "result.html",
                {
                    "request": request,
                    "error": "No similar professors found. Please try different interests."
                }
            )

        logger.info(f"Fetching publications for {similar_professors[0]['name']}")
        try:
            publications = await scraper.get_publications(similar_professors[0]['name'])[:5]
            logger.info(f"Fetched {len(publications)} publications")
        except Exception as e:
            logger.error(f"Error fetching publications: {str(e)}")
            publications = []

        logger.info("Generating cold email...")
        try:
            cold_email = emailer.generate_cold_email(
                name=name,
                prof_name=similar_professors[0]['name'],
                interest=interests,
                achievements=achievements,
                publications=publications
            )
            logger.info("Cold email generated successfully")
        except Exception as e:
            logger.error(f"Error generating cold email: {str(e)}")
            return templates.TemplateResponse(
                "result.html",
                {
                    "request": request,
                    "error": "Error generating email. Please try again later."
                }
            )

        return templates.TemplateResponse(
            "result.html",
            {
                "request": request,
                "professors": [p['name'] for p in similar_professors],
                "email": cold_email
            }
        )
    except Exception as e:
        logger.error(f"Unexpected error in generate_email: {str(e)}", exc_info=True)
        return templates.TemplateResponse(
            "result.html",
            {
                "request": request,
                "error": "An unexpected error occurred. Please try again later."
            }
        )
@app.get("/status")
async def get_status():
    global vector_db
    if vector_db is None:
        return {"status": "initializing"}
    elif len(vector_db.professors) == 0:
        return {"status": "empty"}
    else:
        return {"status": "ready", "professor_count": len(vector_db.professors)}
    


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)