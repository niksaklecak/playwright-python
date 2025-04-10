
# GraphQL query
SPACE_X_CEO_QUERY = """
query Company {
  company {
    ceo
  }
}
"""

# GraphQL mutation
CREATE_USER_MUTATION = """
mutation Mutation($objects: [users_insert_input!]!) {
  insert_users(objects: $objects) {
    affected_rows
    returning {
      id
      name
    }
  }
}
"""