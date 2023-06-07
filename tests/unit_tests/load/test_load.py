"""Test for Serializable base class"""

import pytest

from langchain.chains.llm import LLMChain
from langchain.llms.openai import OpenAI
from langchain.load.dump import dumps
from langchain.load.load import loads
from langchain.prompts.prompt import PromptTemplate


def openai_installed() -> bool:
    try:
        import openai  # noqa: F401
    except ImportError:
        return False
    return True


class NotSerializable:
    pass


@pytest.mark.skipif(not openai_installed, reason="openai not installed")
def test_load_openai_llm() -> None:
    llm = OpenAI(model="davinci", temperature=0.5, openai_api_key="hello")
    llm_string = dumps(llm)
    llm2 = loads(llm_string, secrets_map={"OPENAI_API_KEY": "hello"})

    assert llm2 == llm
    assert dumps(llm2) == llm_string
    assert isinstance(llm2, OpenAI)


@pytest.mark.skipif(not openai_installed, reason="openai not installed")
def test_load_llmchain() -> None:
    llm = OpenAI(model="davinci", temperature=0.5, openai_api_key="hello")
    prompt = PromptTemplate.from_template("hello {name}!")
    chain = LLMChain(llm=llm, prompt=prompt)
    chain_string = dumps(chain)
    chain2 = loads(chain_string, secrets_map={"OPENAI_API_KEY": "hello"})

    assert chain2 == chain
    assert dumps(chain2) == chain_string
    assert isinstance(chain2, LLMChain)
    assert isinstance(chain2.llm, OpenAI)
    assert isinstance(chain2.prompt, PromptTemplate)


@pytest.mark.skipif(not openai_installed, reason="openai not installed")
def test_load_llmchain_with_non_serializable_arg() -> None:
    llm = OpenAI(
        model="davinci",
        temperature=0.5,
        openai_api_key="hello",
        client=NotSerializable,
    )
    prompt = PromptTemplate.from_template("hello {name}!")
    chain = LLMChain(llm=llm, prompt=prompt)
    chain_string = dumps(chain, pretty=True)
    with pytest.raises(NotImplementedError):
        loads(chain_string, secrets_map={"OPENAI_API_KEY": "hello"})
