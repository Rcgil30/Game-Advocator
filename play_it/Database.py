""" Initialization and Fetching of Database """

from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

# Select your transport with a defined url endpoint
transport = AIOHTTPTransport(url="https://gamesdt.herokuapp.com/")

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=True)

# Provide a GraphQL query
query = gql(
    """
    query {
	games {
		id
		title
		portada
		developer
		releaseYear
		gender {
			name
		}
		platform {
			name
		}
		shop
		diff
	}
}
"""
)

result = client.execute(query)