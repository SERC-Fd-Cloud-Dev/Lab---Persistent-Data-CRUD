from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException, Response
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.database import get_session
from app.schemas import GuessWrite, GuessRead
from app.answers import ANSWERS, check_guess
from app.models import Guess
from sqlalchemy import select

def create_app():
    app = FastAPI(title='Movie Clue Game')
    app.state.history_cache = {}  # Optional stretch only.
    public = Path(__file__).resolve().parents[1] / 'frontend'
    app.mount('/static', StaticFiles(directory=public), name='static')

    @app.get('/', include_in_schema=False)
    def home():
        return FileResponse(public / 'index.html')

    @app.get('/health')
    def health():
        return {'status': 'ok'}

    @app.post('/guesses', status_code=201, response_model=GuessRead)
    def guess(data: GuessWrite, session=Depends(get_session)):
        if data.clue_id not in ANSWERS:
            raise HTTPException(404, 'Unknown clue')
        # TODO: check the title using check_guess, save a Guess and return it.
        raise NotImplementedError('Implement persistent guess creation')

    @app.get('/guesses', response_model=list[GuessRead])
    def history(player: str, response: Response, session=Depends(get_session)):
        # TODO: select only this exact player, ordered by Guess.id.
        raise NotImplementedError('Implement persistent player history')

    return app

app = create_app()
