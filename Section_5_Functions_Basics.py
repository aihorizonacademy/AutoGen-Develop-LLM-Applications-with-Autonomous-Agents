import autogen
from Section_5_App import list_datasets

config_list_gpt3 = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-3.5-turbo-1106"],
    },
)

llm_config={
    "timeout": 600,
    "seed": 3,
    "config_list": config_list_gpt3,
    "temperature": 0,
    "functions": [{
            "name": "list_datasets",
            "description": "print out the titles and URLs of datasets listed on the main dataset catalog page",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "url of the page.",
                    }
                },
                "required": ["url"],
            },
        }]
}

assistant = autogen.AssistantAgent(
    name="assistant",
    system_message="You are a helpful assistant.",
    llm_config=llm_config
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    code_execution_config={"work_dir": "coding", "use_docker": False},
)

user_proxy.register_function(
    function_map={
        "list_datasets": list_datasets
    }
)

user_proxy.initiate_chat(
    assistant,
    message="""Run the 'list_datasets' function and tell me which datasets would be useful for someone who wants
                to write an article about public health 'https://catalog.data.gov/dataset' is the url"""
)