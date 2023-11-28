from controller.core import transaction


@transaction
async def create_indexes(tx):
    await tx.execute_write("""
                        CREATE FULLTEXT INDEX StatementsFulltext IF NOT EXISTS
                        FOR (n:Statement)
                        ON EACH [n.value]
                        OPTIONS {
                              indexConfig: {
                                `fulltext.analyzer`: 'standard',
                                `fulltext.eventually_consistent`: true
                              }
                        }
                        """)
    await tx.execute_write("""
                        CREATE FULLTEXT INDEX TagsFulltext IF NOT EXISTS
                        FOR (n:Tag)
                        ON EACH [n.value]
                        OPTIONS {
                              indexConfig: {
                                `fulltext.analyzer`: 'standard',
                                `fulltext.eventually_consistent`: true
                              }
                        }
                        """)

@transaction
async def create_constraints(tx):

    await tx.execute_write("""
            CREATE CONSTRAINT StatementId IF NOT EXISTS
            FOR (a:Statement) REQUIRE a.id IS UNIQUE """)

    await tx.execute_write("""
            CREATE CONSTRAINT TagId IF NOT EXISTS
            FOR (a:Tag) REQUIRE a.id IS UNIQUE """)

    await tx.execute_write("""
            CREATE CONSTRAINT ConnectionId IF NOT EXISTS
            FOR (a:Connection) REQUIRE a.id IS UNIQUE """)

    await tx.execute_write("""
            CREATE CONSTRAINT Username IF NOT EXISTS
            FOR (a:User) REQUIRE a.id IS UNIQUE """)