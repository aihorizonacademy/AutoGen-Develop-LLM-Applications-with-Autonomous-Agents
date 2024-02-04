import autogen

config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-3.5-turbo-1106"]
    }
)

llm_config_editor = {
    "timeout": 400,
    "seed": 45,
    "config_list": config_list,
    "temperature": 0,
}

llm_config_writer = {
    "timeout": 400,
    "seed": 45,
    "config_list": config_list,
    "temperature": 1,
}

writer = autogen.AssistantAgent(
    name="Writer",
    llm_config=llm_config_writer,
    system_message="Your task is to write an article on a given subject and to rewrite it after receiving feedback from the editor. Reply with TERMINATE after you create a corrected version."
)

editor = autogen.AssistantAgent(
    name="Editor",
    llm_config=llm_config_editor,
    system_message="Your task is to correct the article submitted by the writer. Check if the information is accurate. Do not rewrite the article, instead create a list of adjustments to be made, make it relatively short."
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    system_message="A human admin",
    human_input_mode="ALWAYS",
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
)

groupchat = autogen.GroupChat(
    agents=[user_proxy, writer, editor],
    messages=[],
    max_round=10,
    speaker_selection_method="manual"
)

manager = autogen.GroupChatManager(
    groupchat=groupchat,
    llm_config=llm_config_editor
)

user_proxy.initiate_chat(
    manager,
    message="Write an article about large language models"
)
