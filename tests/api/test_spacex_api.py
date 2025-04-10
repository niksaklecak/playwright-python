from data.graphql_queries import SPACE_X_CEO_QUERY


def test_first_query(execute_graphql_query) -> None:
    response = execute_graphql_query.execute_query(SPACE_X_CEO_QUERY)
    assert response['data']['company']['ceo'] == 'Elon Musk'
    
    

