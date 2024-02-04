import autogen

config_list_gpt3 = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-3.5-turbo-16k"]
    }
)

config_list_gpt4 = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-4-1106-preview"]
    }
)

llm_config_gpt3 = {
    "temperature": 0,
    "timeout": 400,
    "seed": 24,
    "config_list": config_list_gpt3
}

llm_config_gpt4 = {
    "temperature": 0,
    "request_timeout": 400,
    "seed": 2,
    "config_list": config_list_gpt4
}

assistant = autogen.AssistantAgent(
    name="Assistant",
    system_message="You are a helpful assistant",
    llm_config=llm_config_gpt3
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="ALWAYS",
    system_message="You are a helpful assistant",
    code_execution_config={
        "work_dir": "programs",
        "use_docker": False
    },
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE")
)

user_proxy.initiate_chat(assistant, message="Write a snake game using pygame")

