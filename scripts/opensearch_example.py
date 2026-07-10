from openai import OpenAI
from opensearchpy import OpenSearch
from core.config import settings

client = OpenAI(api_key=settings.openai_api_key)
os_client = OpenSearch(hosts=[{'host': 'localhost', 'port': 9200}])

q = 'graph rag'
vec = client.embeddings.create(
    model=settings.embedding_model,
    input=[q],
    dimensions=settings.embedding_dimensions,
).data[0].embedding

resp = os_client.search(
    index='chunks_code4ai',
    body={
        'size': 5,
        'query': {'knn': {'embedding': {'vector': vec, 'k': 5}}}
    }
)
for hit in resp['hits']['hits']:
    s = hit['_source']
    print(f"{hit['_score']:.3f}  {s['video_id']}  {s['title'][:60]}")
