# REST API of the SQL schema generator

from fastapi import FastAPI

from sql_schema_generator import open_yaml, yaml_to_postgresql_schema


app = FastAPI()

@app.post("/sql-schema/{subject}/{datamodel}")
async def generate_schema(subject: str, datamodel:str):
   
    yaml_source = f"https://raw.githubusercontent.com/smart-data-models/dataModel.{subject}/master/{datamodel}/model.yaml"
    try:
        schema = open_yaml(yaml_source)
        sql_schema = yaml_to_postgresql_schema(schema)
        return {"success": True, "sql_schema": sql_schema}
    except Exception as e:
        return {"success": False, "error": str(e)}
    

if __name__ == "__main__":
    import uvicorn

    # Only run this way in testing mode
    uvicorn.run(app, host="0.0.0.0", port=8000)
    print("To test the API, navigate to: http://localhost:8000/docs")




