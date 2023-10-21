from starlette.testclient import TestClient

from main import app

client = TestClient(app=app,root_path="/connection")


async def test_create():
    pass

async def test_weight():
    pass

async def test_delete():
    pass


"""
router = APIRouter(prefix="/connection")

@router.post("/", response_model=Response[Connection])
async def create(current_user: Annotated[User, Depends(get_current_active_user)], body: RequestConnectionCreate):
    print(f"CREATE CONNECTION \nBy: {current_user}\nBody: {body}")

    async with Db.session() as session:
        r = await session.execute_write(connection_create_tx, start_id=body.child_id,
                                        stop_id=body.parent_id,
                                        is_support=body.supports,
                                        username=current_user.username)
    return r


@router.post("/vote", response_model=Response)
async def weight(
        current_user: Annotated[User, Depends(get_current_active_user)],
        body: RequestConnectionVote):
    print(f"VOTE CONNECTION \nBy: {current_user}\nBody: {body}")
    async with Db.session() as session:
        r = await session.execute_write(
            connection_weight_tx, connection_id=body.id,
            weight=body.value,
            username=current_user.username)
    return r


@router.delete("/", response_model=Response)
async def delete(
        current_user: Annotated[User, Depends(get_current_active_user)],
        id: str = ""):
    print(f"DELETE CONNECTION \nBy: {current_user}\nid: {id}")
    async with Db.session() as session:
        r = await session.execute_write(
            connection_delete_tx, connection_id=id,
            username=current_user.username)
    return r

"""