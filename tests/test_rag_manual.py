from src.rag import LearnMateRAG


rag = LearnMateRAG()

query = "My model performs very well on training data but poorly on new data."

results = rag.retrieve(query, top_k=3)

print("\nQuery:")
print(query)

print("\nTop Retrieved Results:")

for i, result in enumerate(results, start=1):
    print(
        f"{i}. {result['topic']} "
        f"| similarity = {result['similarity']}"
    )