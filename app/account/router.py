from fastapi import APIRouter, Response, Form, Request
from .schemas import (
    CreateWorker, CreateTeam, AddWorkerToTeam,
    WorkersIdList
)
from .cosmogram import GetCosmogram, GetCompatibility
from .dao import WorkerDAO, TeamDAO, TeamMemberDAO
from app.authentication import (
    verify_access_token
)
from app.core import (
    ForbiddenException,
    IncorrectFormatException
)
from collections import defaultdict


account_router = APIRouter(prefix='/account', tags=['Аккаунт'])


@account_router.get('/')
async def home(
    request: Request
        ):
    token = request.cookies.get("access_token", None)
    if token is None:
        raise ForbiddenException

    payload = await verify_access_token(token)

    return {
        'message': 'Home',
        'first_name': payload['first_name'],
        'last_name': payload['last_name'],
        'company_name': payload['company_name'],
        'email': payload['email']
    }


@account_router.get('/all_worker')
async def get_all_workers(
    request: Request,
        ):
    token = request.cookies.get("access_token", None)
    if token is None:
        raise ForbiddenException

    payload = await verify_access_token(token)
    workers = await WorkerDAO.find(
        all=True,
        or_method=False,
        company_name=payload['company_name']
    )
    resp: dict = {'all_worker': []}
    for worker in workers:
        resp['all_worker'].append(
            {
                'id': worker.id,
                'first_name': worker.first_name,
                'last_name': worker.last_name,
                'patronymic': worker.patronymic,
                'position': worker.position,
                'company_name': worker.company_name,
                'team_name': worker.team_name,
                'date_of_birth': worker.date_of_birth,
            }
        )
    return resp


@account_router.get('/all_team')
async def get_all_team(
    request: Request,
        ):
    token = request.cookies.get("access_token", None)
    if token is None:
        raise ForbiddenException

    payload = await verify_access_token(token)
    teams = await TeamDAO.find(
        all=True,
        or_method=False,
        company_name=payload['company_name']
    )
    resp: dict = {'all_team': []}
    for team in teams:
        resp['all_team'].append(
            {
                'id': team.id,
                'company_name': team.company_name,
                'team_name': team.team_name,
            }
        )
    return resp


@account_router.get('/squad_list')
async def get_squad_list(
    request: Request,
        ):
    token = request.cookies.get("access_token", None)
    if token is None:
        raise ForbiddenException

    payload = await verify_access_token(token)
    results = await TeamMemberDAO.find_in(
        company_name=payload['company_name']
    )

    teams_workers = defaultdict(list)

# Обрабатываем результаты
    for worker, team in results:
        teams_workers[team.team_name].append({
            'id': worker.id,
            'first_name': worker.first_name,
            'last_name': worker.last_name,
            'patronymic': worker.patronymic,
            'position': worker.position,
            'company_name': worker.company_name,
            'date_of_birth': worker.date_of_birth,
            'zodiac_sign': worker.zodiac_sign,
        })
    return teams_workers


@account_router.post('/find_comp')
async def find_compatibility(
    request: Request,
    workers_id: WorkersIdList = Form(...)
        ):
    token = request.cookies.get("access_token", None)
    if token is None:
        raise ForbiddenException

    payload = await verify_access_token(token)
    workers = await WorkerDAO.find_in(
        map(int, workers_id.workers_id[0].split(',')),
        company_name=payload['company_name']
    )
    arr = []
    for worker in workers:
        arr.append(
            [
                worker.zodiac_sign,
                eval(worker.cosmogram_info)
            ]
        )
    score = GetCompatibility(arr).get_similarity()
    return {
        'score': str(score)
    }


@account_router.post('/create_team_member')
async def create_team_member(
    request: Request,
    info: AddWorkerToTeam = Form(...),
        ):
    token = request.cookies.get("access_token", None)
    if token is None:
        raise ForbiddenException

    payload = await verify_access_token(token)

    w_id = list(map(int, info.workers_id[0].split(',')))
    workers = await WorkerDAO.find_in(
        w_id,
        company_name=payload['company_name']
    )
    arr = []
    for worker in workers:
        arr.append(
            [
                worker.zodiac_sign,
                eval(worker.cosmogram_info)
            ]
        )
    score = GetCompatibility(arr).get_similarity()

    for id in w_id:
        await TeamMemberDAO.add(
            worker_id=int(id),
            team_id=info.team_id,
            similarity_coef=score
        )

    return {
        'message': 'Команда создана',
        'score': score
    }


@account_router.post('/create_worker')
async def create_worker(
    request: Request,
    worker: CreateWorker = Form(...),
        ):
    token = request.cookies.get("access_token", None)
    if token is None:
        raise ForbiddenException

    payload = await verify_access_token(token)
    try:
        cosmogram_modul = GetCosmogram(
            worker.date_of_birth,
            worker.addres_of_birth,
            worker.time_of_birth
        ).get_score()
        create_worker = await WorkerDAO.add(
            first_name=worker.first_name,
            last_name=worker.last_name,
            patronymic=worker.patronymic,
            company_name=payload['company_name'],
            position=worker.position,
            date_of_birth=worker.date_of_birth,
            zodiac_sign=cosmogram_modul[0],
            cosmogram_info=f'{cosmogram_modul[1]}'
        )
    except Exception:
        raise IncorrectFormatException

    return {
        'id': create_worker.id,
        'first_name': create_worker.first_name,
        'last_name': create_worker.last_name,
        'patronymic': create_worker.patronymic,
        'position': create_worker.position,
        'date_of_birth': create_worker.date_of_birth,
    }


@account_router.post('/create_team')
async def create_team(
    request: Request,
    team: CreateTeam = Form(...),
        ):
    token = request.cookies.get("access_token", None)
    if token is None:
        raise ForbiddenException

    payload = await verify_access_token(token)
    try:
        await TeamDAO.add(
            company_name=payload['company_name'],
            team_name=team.team_name,
        )

    except Exception:
        raise IncorrectFormatException

    return {
        'team_name': team.team_name
    }
