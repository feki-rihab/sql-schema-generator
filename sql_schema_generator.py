#################################################################################
#  Licensed to the FIWARE Foundation (FF) under one                             #
#  or more contributor license agreements. The FF licenses this file            #
#  to you under the Apache License, Version 2.0 (the "License")                 #
#  you may not use this file except in compliance with the License.             #
#  You may obtain a copy of the License at                                      #
#                                                                               #
#      http://www.apache.org/licenses/LICENSE-2.0                               #
#                                                                               #
#  Unless required by applicable law or agreed to in writing, software          #
#  distributed under the License is distributed on an "AS IS" BASIS,            #
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.     #
#  See the License for the specific language governing permissions and          #
#  limitations under the License.                                               #
#  Author: Rihab Feki
#################################################################################

#################################################################################
# this script generates a SQL script for PostgreSQL based on the model.yaml     #
# representation defining a data model                                          #
#################################################################################

import requests
import ruamel.yaml as yaml

from utils import open_json, open_yaml


def yaml_to_postgresql_schema(yamlfile)-> dict:
    """ 
    Generate a PostgreSQL schema SQL script from the model.yaml representation of a Smart Data Model.

    This function takes a dictionary representing a model.yaml file, extracts relevant information,
    and creates a PostgreSQL schema SQL script.

    Args:
        yamlfile (dict): A dictionary representing the content of a model.yaml file.

    Returns:
        str: A string containing the PostgreSQL schema SQL script.
    """
    # Get the entity name
    entity = list(yamlfile.keys())[0]

    # Initialize SQL schema statements
    sql_schema_statements = []
    sql_type_statement = []

    sql_data_types= ""

    # Define format mappings for YAML formats to postgreSQL Schema types
    type_mapping = {
        "string": "TEXT",
        "integer": "INTEGER",
        "number": "NUMERIC",
        "boolean": "BOOLEAN",
        "object": "JSON",
        "array": "JSON",
    }

    # Define format mappings for YAML formats to postgreSQL Schema types
    format_mapping = {
        "date-time": "TIMESTAMP",
        "date": "DATE",
        "time": "TIME",
        "uri": "TEXT",
        "email": "TEXT",
        "idn-email": "TEXT",
        "hostname": "TEXT",
        "duration": "TEXT"
    }

    # Start by creating the table
    table_create_statement = f"CREATE TABLE {entity} ("

    for key, value in yamlfile[entity]["properties"].items():
        field_type = "JSON"  # Default to JSON if type is not defined

        # Field type mapping
        if "type" in value:
            if "format" in value:
                # format type mapping (format overrides type)
                field_type = format_mapping.get(value["format"])
                # add attribute to the SQL schema statement
                sql_schema_statements.append(f"{key} {field_type}")

            elif "enum" in value:
                enum_values = value["enum"]
                enum_values = [str(element) for element in enum_values]
                if key == "type":
                    field_type = f"{entity}_type"
                else:
                    field_type = f"{key}_type"
                # create sql create type statment
                sql_type_statement.append(f"CREATE TYPE {field_type} AS ENUM ({','.join(map(repr, enum_values))});")

                sql_data_types += "CREATE TYPE " + field_type + " AS ENUM ("
                sql_data_types += f"{','.join(map(repr, enum_values))}"
                sql_data_types += ");"

                # add attribute to the SQL schema statement
                sql_schema_statements.append(f"{key} {field_type}")

            else:
                field_type = type_mapping.get(value["type"])
                # add attribute to the SQL schema statement
                sql_schema_statements.append(f"{key} {field_type}")

        # Handle the case when "allOf" exists
        if key == "allOf" and isinstance(value, list):
            for values in value:
                for sub_key, sub_value in values.items():
                    if isinstance(sub_value, dict):
                        if "format" in sub_value:
                            sub_field_type = format_mapping.get(sub_value["format"])
                            sql_schema_statements.append(f"{sub_key} {sub_field_type}")
                        if "type" in sub_value:
                            sub_field_type = type_mapping.get(sub_value["type"])
                            sql_schema_statements.append(f"{sub_key} {sub_field_type}")
        if key == "id":
            field_type = "TEXT"

    # Complete the CREATE TABLE statement
    table_create_statement += ", ".join(sql_schema_statements)
    table_create_statement += ");"
    # PostgreSQL schema 
    result = sql_data_types + "\n" + table_create_statement
    #print(result)

    return result


#################################################################################
# Executing the code 
#################################################################################

# Constants
URL_DATA_MODELS_LIST = "https://raw.githubusercontent.com/smart-data-models/data-models/master/specs/AllSubjects/official_list_data_models.json"
CONFIG_FILE = "datamodels_to_publish.json"

# Get data models list
datamodels_list = open_json(URL_DATA_MODELS_LIST)["officialList"]

# Read configuration file
data_models_to_publish = open_json(CONFIG_FILE)
subject = data_models_to_publish["subject"]
data_models = data_models_to_publish["dataModels"]

# Process data models
for datamodel in data_models:
    yaml_source = f"https://raw.githubusercontent.com/smart-data-models/{subject}/master/{datamodel}/model.yaml"
    schema = open_yaml(yaml_source)
    
    content_variable = (
        f"/* (Beta) Export of data model {datamodel} of the subject {subject} "
        "for a PostgreSQL database. Pending translation of enumerations and multityped attributes */" + "\n"
    )
    content_variable += str(yaml_to_postgresql_schema(schema))
    
    print("___________________________________________")
    print(content_variable)
    print("___________________________________________")
