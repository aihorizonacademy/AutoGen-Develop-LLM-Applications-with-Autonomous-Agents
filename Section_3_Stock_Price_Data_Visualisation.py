import autogen

config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-4-1106-preview"]
    }
)

llm_config = {
    "temperature": 0,
    "seed": 6,
    "config_list": config_list,
    "timeout": 400
}

assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config=llm_config
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "work_dir": "programs",
        "use_docker": False
    }
)

user_proxy.initiate_chat(
    assistant,
    message="Write a program that will check the current date and will compare the year-to-date gain for META and TESLA using appropriate api"
)