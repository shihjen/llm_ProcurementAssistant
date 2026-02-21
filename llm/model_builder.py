from pydantic import Field, create_model

TYPE_MAP = {
    "str": str,
    "int": int,
    "float": float,
    "bool": bool
}


def build_model(schema_json):

    fields = {}

    for field in schema_json["fields"]:
        name = field["name"]
        dtype = TYPE_MAP[field["type"]]
        desc = field["description"]

        fields[name] = (
            dtype,
            Field(description=desc)
        )

    model = create_model(
        schema_json["model_name"],
        **fields
    )

    return model
