import asyncio

import dotenv

import load_env
import db
import api.routes.users as userroute
import api.routes.statements as statementroute
import api.routes.connections as connectionroute

# watch("neo4j", out=sys.stdout)

users = [userroute.RequestUserCreate(username=i, password=i) for i in "12345"]


async def create_all_user_user():
    for u in users:
        await userroute.create(u)


async def create_all_statements():
    statement_ids = {}
    for a in "ABCDEFG":
        response = await statementroute.create(current_user=users[0],
                                         body=statementroute.RequestStatementCreate(value=a, tags=[a.lower()]))
        statement_ids[a] = response["value"]["id"]
    return statement_ids


async def create_all_connections(statement_ids):
    # ABCDEFG
    # 0123456
    connections = {
        "B": [(True, "A")],
        "C": [(False, "A")],
        "A": [(True, "D")],
        "D": [(False, "E"), (False, "F")],
        "E": [(True, "G")],
        "F": [(False, "E")],
    }
    connection_ids = []
    for i in connections.keys():
        for con in connections[i]:
            child = statement_ids[i]
            parent = statement_ids[con[1]]
            supp = con[0]
            id = await connectionroute.create(current_user=users[0],
                                              body=connectionroute.RequestConnectionCreate(parent_id=parent,
                                                                                           child_id=child,
                                                                                           supports=supp))
            connection_ids.append(id["value"])
    return connection_ids


async def vote_all_statements(statement_ids):
    votes = {
        #     up  |  down
        0: ("ABCDEFG", ""),
        1: ("ACEG", "BDF"),
        2: ("EBGD", "CAF"),
        3: ("EDB", "CAFG"),
        4: ("EDFG", "BCA"),
    }

    for k in votes.keys():
        for i in "ABCDEFG":
            value = 1 if i in votes[k][0] else -1
            await statementroute.vote(current_user=users[k],
                                      body=statementroute.RequestStatementVote(id=statement_ids[i], value=value))


async def vote_all_connections(connection_ids):
    votes = {
        # connection_index: weight
        0: 0.7,
        1: 0.3,
        2: 0.5,
        3: 0.9,
        4: 0.77,
        5: 0.45,
        6: 0.27
    }

    for u in users:
        for k in votes.keys():
            con_id = connection_ids[k]
            val = votes[k]
            await connectionroute.weight(current_user=u,
                                         body=connectionroute.RequestConnectionVote(id=con_id, value=val))


async def _start():
    db.init()

    await create_all_user_user()
    stm_ids = await create_all_statements()
    await vote_all_statements(stm_ids)
    ctn_ids = await create_all_connections(stm_ids)
    await vote_all_connections(ctn_ids)

    try:
        pass
    except Exception as e:
        print(e)
    finally:
        await db.close()


def run(path_to_env):
    dotenv.load_dotenv(path_to_env)
    asyncio.run(_start())


if __name__ == '__main__':
    run(".env")
